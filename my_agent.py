from LLM import *
reply = llm("你需要回答用户的问题，并一定一定一定一定用python代码实现用户的一些需求，如：打开网站！打开网站！，打开某软件，写文档，计算复杂算式这些都需要编写程序完成！！",input())
print(reply)
from clean import *
py_text = clean_code(reply)
if not py_text == '没有':
    reply2 = llm("这段代码里面需要安装哪些可能未包含的包，只输出包的名称，如果有多个则用空格隔开，如果没有则仅输出‘无’，没有则仅输出‘无’，没有则仅输出‘无’",py_text)
    print(reply2)
    if reply2 != '无':
        modules = reply2.split()
        from install import *
        for module in modules:
            pip_install(module)
        import time
        time.sleep(1)
    from writer import *
    write(py_text)
