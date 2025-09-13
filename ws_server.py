# server.py
import asyncio
import websockets
import json
import os
import sys
import traceback

from app import get_data, mouse_event, text_event, key_event, key_up, key_down
from get_local_ip import get_local_ip

# --- 服务器配置 ---
HOST = "0.0.0.0"
WS_PORT = 8765  # WS 默认常用端口是 80，也可自定义其他端口（如 8080）


# --- WebSocket 处理器 (保持不变) ---
async def websocket_handler(websocket, path):
    """处理WebSocket连接的异步函数。"""
    print(f"WebSocket 连接已建立：{path}")
    try:
        async for message in websocket:
            try:
                # print(message)
                data_dict = json.loads(message)
                if data_dict.get("mouse"):
                    mouse_event(data_dict.get("mouse"))
                elif data_dict.get("text"):
                    text_event(data_dict.get("text"))
                elif data_dict.get("key"):
                    key_event(data_dict.get("key"))
                elif data_dict.get("keyup"):
                    key_up(data_dict.get("keyup"))
                elif data_dict.get("keydown"):
                    key_down(data_dict.get("keydown"))
                else:
                    get_data(
                        0,
                        0,
                        0,
                        data_dict["alpha"],
                        data_dict["beta"],
                        data_dict["gamma"],
                    )
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print("JSON 解析或事件处理错误:")
                # 使用 print_tb 只打印回溯堆栈（不含异常类型和值信息）
                traceback.print_tb(exc_traceback)
                # 或者使用 print_exception 打印完整的异常信息（等同于 print_exc()）
                traceback.print_exception(exc_type, exc_value, exc_traceback)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket 连接已关闭: {e}")
    except Exception as e:
        print(f"WebSocket 处理中发生未知错误: {e}")


# --- 主函数 (移除了SSL相关代码) ---
async def main():
    """主函数，用于启动纯WebSocket服务器 (无SSL)。"""

    # 创建并运行纯WebSocket服务器，不再使用 ssl_context
    async with websockets.serve(websocket_handler, HOST, WS_PORT):
        print(f"WebSocket 服务器正在运行在 ws://{HOST}:{WS_PORT}")
        # 保持服务器运行
        await asyncio.Future()


if __name__ == "__main__":
    print("请填入", f"ws://{get_local_ip()}:{WS_PORT}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器正在关闭。")
