# server.py
import asyncio
import ssl
import websockets
import http.server
import os
import json
from pathlib import Path

from cert import generate_self_signed_cert

from app import get_data, mouse_event, text_event, key_event

# from data_logger import get_data


# --- 服务器配置 ---
HOST = "0.0.0.0"
HTTP_PORT = 8443
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
WWW_DIRECTORY = "www"


# --- WebSocket 处理器 ---
async def websocket_handler(websocket, path):
    """处理WebSocket连接的异步函数。"""
    print(f"WebSocket 连接已建立：{path}")
    try:
        async for message in websocket:
            # print(message)
            try:
                data_dict = json.loads(message)
                if data_dict.get("mouse"):
                    mouse_event(data_dict.get("mouse"))
                elif data_dict.get("text"):
                    text_event(data_dict.get("text"))
                elif data_dict.get("key"):
                    key_event(data_dict.get("key"))
                else:
                    get_data(
                        data_dict["x"],
                        data_dict["y"],
                        data_dict["z"],
                        data_dict["alpha"],
                        data_dict["beta"],
                        data_dict["gamma"],
                    )
            except Exception as e:
                print("error:", e)
            # print(f"{time.time()}收到消息: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket 连接已关闭: {e}")
    except Exception as e:
        print(f"WebSocket 处理中发生错误: {e}")


# --- HTTP 文件服务处理器 ---
class FileHandler(http.server.SimpleHTTPRequestHandler):
    """处理HTTP请求并提供文件的处理器。"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WWW_DIRECTORY, **kwargs)


# --- 主函数 ---
async def main():
    """主函数，用于启动服务器。"""
    # 检查证书文件是否存在
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        generate_self_signed_cert()
        print("未找到证书文件，正在生成自签名证书...")
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("错误：找不到 'cert.pem' 或 'key.pem' 文件。")
        print("请先运行 'generate_cert.py' 来生成证书。")
        return

    # 配置SSL上下文
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(CERT_FILE, KEY_FILE)
    print("SSL 上下文已配置。")

    # 创建并运行WebSocket服务器
    async with websockets.serve(
        websocket_handler,
        HOST,
        HTTP_PORT,
        ssl=ssl_context,
        # 当请求不是WebSocket升级请求时，回退到HTTP处理器
        process_request=http_server_handler,
    ):
        print(f"HTTPS 和 WebSocket 服务器正在运行在 wss://{HOST}:{HTTP_PORT}")
        await asyncio.Future()  # 永远运行


def http_server_handler(path, request_headers):
    """
    一个回退函数，用于处理非WebSocket的HTTP请求。
    """

    if "Upgrade" in request_headers and request_headers["Upgrade"] == "websocket":
        return  # 让 `websockets` 库处理它

    # 这是一个变通方法，因为 `websockets` 库本身不直接提供文件服务。
    # 对于生产环境，建议使用更强大的框架如 aiohttp, Sanic, 或 FastAPI。
    # 这里我们只提供一个基本的演示。
    if path == "/":
        path = "/index.html"

    file_path = os.path.abspath(os.path.join(WWW_DIRECTORY, path.lstrip("/")))

    if os.path.commonpath(
        [file_path, os.path.abspath(WWW_DIRECTORY)]
    ) != os.path.abspath(WWW_DIRECTORY):
        return (http.HTTPStatus.FORBIDDEN, [], b"Forbidden")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        content_type = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".json": "application/json",
        }.get(Path(file_path).suffix, "application/octet-stream")
        with open(file_path, "rb") as f:
            content = f.read()
        return (http.HTTPStatus.OK, [("Content-Type", content_type)], content)
    else:
        return (http.HTTPStatus.NOT_FOUND, [], b"Not Found")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器正在关闭。")
