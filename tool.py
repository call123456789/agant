#所有可调用的工具在这里，解释在每个工具的代码里面有写
tools =[
    {
        "type":"function",
        "function":{
            "name": "exec_code",  #这是工具名字
            "description":"执行一段python程序，其功能强大，在没有合适工具时使用", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "prompt":{
                        "type":"string",
                        "description":"要执行的python程序字符串，特别注意不要有python代码块标记，而且代码中一定要用'result'存储运行结果"
                    }
                },
                "required": ["prompt"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "paint",  #这是工具名字
            "description":"画一幅场景画", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "prompt":{
                        "type":"string",
                        "description":"画的内容的说明，要说明风格是摄影照"
                    }
                },
                "required": ["prompt"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "extract_text",  #这是工具名字
            "description":"可以从docx或pdf或txt文件中读取文本信息", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "prompt":{
                        "type":"string",
                        "description":"文件的名称"
                    }
                },
                "required": ["prompt"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "watch",  #这是工具名字
            "description":"可以查看一幅图片并分析图片内容", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "prompt":{
                        "type":"list",
                        "description":"一个二元的列表，第一位是图片文件名称，第二位是分析图片的具体任务"
                    }
                },
                "required": ["prompt"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "semantic_search",  #这是工具名字
            "description":"从知识库检索与某个问题相关的知识", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "prompt":{
                        "type":"string",
                        "description":"需要检索的问题"
                    }
                },
                "required": ["prompt"]
            }
        },
        "strict": True
    }
]
