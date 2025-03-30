from openai import OpenAI


client = OpenAI(
    api_key="******************",
    base_url="https://api.deepseek.com"
)


prompt = "请你以两会为主题，写一篇有关科技创新的文章，围绕最新的大模型技术展开，要求贴近中国发展国情，可以将焦点定位为教育改革上去，要求字数不低于2000字"
# 调用模型
response = client.chat.completions.create(
    model="deepseek-chat",
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ],
    temperature=0.1,
    stream = False
)
print(response.choices[0].message.content)