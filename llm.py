from openai import OpenAI
import json
class LLM:
    def __init__(self, temprature = 0.3, task = "你是个好助手", tools = []):
        self.temprature = temprature
        self.task = task
        self.tools = tools
        self.messages = [ {"role": "system", "content": task} ]

        # 加载 JSON 文件
        with open('set.json', 'r') as file:
            config = json.load(file)

        # 获取 API 密钥
        self.model = config.get('talk-model')
        self.api = config.get('api_key')
        self.base_url = config.get('base_url')
        self.model = config.get('vision-model')
        
    def add(self, content, role = "user"):
        self.messages.append({"role": role, "content": content})
    def response(self, context = "None"):
        # 记忆功能，通过不断往self.messages里面append信息实现
        if context != "None":
            self.messages.append({"role": "user", "content": context})
        try:
            client = OpenAI(
                api_key=self.api,
                base_url=self.base_url,
            )
            completion = client.chat.completions.create(
                model = self.model,
                messages = self.messages,
                temperature = self.temprature,
                tools = self.tools
            )
            #得到回复
            self.messages.append(completion.choices[0].message)
            return completion.choices[0].message.content
        except Exception as e:
            print(str(e))
            return str(e)