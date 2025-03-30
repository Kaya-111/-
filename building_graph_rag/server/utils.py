
import requests
import json
import time

def get_chat_access_token(AK, SK):
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + AK + "&client_secret=" + SK
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.2)

def response_generator_compare(response, type="llm+rag"):
    response = type + "回复:    " + response
    for word in response.split():
        yield word + " "
        time.sleep(0.2)