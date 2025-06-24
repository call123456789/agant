import subprocess
import sys
import os

def install(package):
    # 检查是否已安装
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        print(f"{package} 已存在，跳过安装")
        return f"{package} 已存在，跳过安装"
    
    try:
        #使用这些命令安装库
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "--trusted-host", "files.pythonhosted.org",
            "--trusted-host", "pypi.org",
            "--trusted-host", "pypi.python.org",
            "--trusted-host", "files.pythonhosted.org:443",
            "--trusted-host", "pypi.org:443",
            "--trusted-host", "pypi.python.org:443",
            "--trusted-host", "mirrors.aliyun.com",
            "--trusted-host", "mirrors.aliyun.com:443",
            package
        ], check=True)
        print(f"{package} 已成功安装")
        return f"{package} 已成功安装"
    except subprocess.CalledProcessError as e:
        print(f"安装 {package} 时出错: {e}")
        return f"安装 {package} 时出错: {e}"
def prepare():
    install("openai")
    install("requests")
    install("python-docx")
    install("speech_recognition")
    install("pyaudio")
    os.makedirs("resources", exist_ok=True)
    os.makedirs("resources/knowledge",exist_ok=True)
    os.makedirs("resources/knowledge/data",exist_ok=True)
    os.makedirs("resources/knowledge/user",exist_ok=True)
    os.makedirs("resources/uploads",exist_ok=True)
    os.makedirs("user", exist_ok=True)
if __name__ == '__main__':
    prepare()