def llm(task, context):
    from openai import OpenAI
    api = ''
    with open('api.txt', 'r') as f:
        api =  f.readline()
    client = OpenAI(
        api_key=api,
        base_url="https://api.moonshot.cn/v1",
    )
 
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": task},
            {"role": "user", "content": context}
        ],
    temperature = 0.5,
    )
    return completion.choices[0].message.content