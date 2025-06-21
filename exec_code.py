def exec_code(code: str):
    print("执行代码:")
    print(code) # 打印代码便于调试
    try:
        namespace = {} 
        exec(code, namespace)
        return '程序运行结果是' + str(namespace['result'])
    except Exception as e:
        return "执行失败，原因：%s" % str(e)