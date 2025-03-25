from install import *
pip_install('openai')
with open('api.txt','w') as f:
    f.write(input('请输入你的kimi api:'))