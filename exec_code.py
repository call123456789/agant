def exec_code(code: str):
    if 'python' in code.split('\n')[0]:
        code = '\n'.join(code.split('\n')[1:-1])
    
    try:
        namespace = {} 
        exec(code, namespace)
        return '程序运行结果是' + str(namespace['result'])
    except Exception as e:
        return "执行失败，原因：%s" % str(e)