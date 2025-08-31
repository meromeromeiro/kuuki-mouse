# 新建虚拟环境
python -m venv .venv

# 激活环境
.\.venv\Scripts\Activate.ps1

# 安装需要的包
pip install -r requirements.txt

# pyinstaller
# pyinstaller  --onefile --upx-dir=C:\bin\upx-5.0.1-win64 ./server.py