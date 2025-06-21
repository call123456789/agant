from openai import OpenAI
import json
from tool import tools
from prompt import planner_prompt
from painter import paint
from exec_code import exec_code
from reader import extract_text
from watcher import watch
from knowledge import *
class LLM:
    def __init__(self, task = "你是个好助手", tools = []):
        self.task = task
        self.tools = tools
        self.messages = [ {"role": "system", "content": task} ]

        # 加载 JSON 文件
        with open('API.json', 'r') as file:
            config = json.load(file)

        # 获取 API 密钥
        self.model = config.get('talk-model')
        self.api = config.get('api_key')
        self.base_url = config.get('base_url')
        self.temprature = config.get('temprature')
    def add(self, content, role = "user"):
        self.messages.append({"role": role, "content": content})
    def response(self, context="None"):
        if context != "None":
            self.messages.append({"role": "user", "content": context})
        
        try:
            client = OpenAI(
                api_key=self.api,
                base_url=self.base_url,
            )
            while True:
                stream = client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    temperature=self.temprature,
                    tools=self.tools,
                    stream=True
                )
                
                full_content = ""
                tool_calls = []  # 存储完整的工具调用信息
                current_tool_call = None  # 当前正在处理的工具调用
                
                for chunk in stream:
                    choice = chunk.choices[0]
                    delta = choice.delta
                    
                    # 处理工具调用块
                    if delta.tool_calls:
                        for tool_call_delta in delta.tool_calls:
                            # 新的工具调用开始
                            if tool_call_delta.index >= len(tool_calls):
                                tool_calls.append({
                                    "id": tool_call_delta.id or "",
                                    "type": "function",
                                    "function": {
                                        "name": "",
                                        "arguments": ""
                                    }
                                })
                                current_tool_call = tool_calls[-1]
                            
                            # 更新工具调用信息
                            if tool_call_delta.function:
                                if tool_call_delta.function.name:
                                    current_tool_call["function"]["name"] = tool_call_delta.function.name
                                if tool_call_delta.function.arguments:
                                    current_tool_call["function"]["arguments"] += tool_call_delta.function.arguments
                                    # 处理内容块
                    
                    if delta.content is not None:
                        content_chunk = delta.content
                        full_content += content_chunk
                        yield content_chunk  
                
                # 添加完整响应到历史记录
                assistant_message = {"role": "assistant", "content": full_content}
                if tool_calls:
                    assistant_message["tool_calls"] = tool_calls
                self.messages.append(assistant_message)

                if tool_calls == None or tool_calls == []:
                    break

                for tool_call in tool_calls:
                    yield '正在调用工具%s\n' % tool_call['function']['name']
                    args = tool_call['function']['arguments']
                    if isinstance(args,str):
                        args = eval(args)
                    result = eval(tool_call['function']['name'])(list(args.values())[0])
                    self.messages.append({"role":"tool","tool_call_id": tool_call['id'],"content": result})
                    yield '工具%s调用结果为：%s\n' % (tool_call['function']['name'],result)
            
        except Exception as e:
            print(f"请求失败: {e}")
            yield '出现错误'+str(e)

if __name__ == '__main__':
    llm = LLM(tools=tools, task= planner_prompt)
    llm.add("画一幅山水画")

    for data in llm.response():
        print(data, end='', flush=True)