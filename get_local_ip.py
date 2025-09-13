import socket

def get_local_ip():
    try:
        # 创建一个 UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到外部地址（此处使用 Google 的公共 DNS）
        s.connect(("8.8.8.8", 80))
        # 获取套接字的本地地址
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "127.0.0.1"  # 失败时退回环回地址
    finally:
        s.close()
    return ip

print("本地 IP 地址:", get_local_ip())