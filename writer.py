def write(data):
    import subprocess
    import os
    import sys
    file_path = "new.py"
# 将字符串写入文件
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as file:
        file.write(data)
    subprocess.run([sys.executable, file_path])