def pip_install(module):
    import subprocess
    import sys
    install_cmd = [sys.executable, "-m", "pip", "install", module]
    subprocess.run(install_cmd,capture_output=True,text=True)