import requests
import time

# Get you free api key https://app.hyperbolic.xyz/
my_gpt_api = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ6aGFzaDIzMDhAbWFpbC5ydSIsImlhdCI6MTczMzkzNzM1NX0.bL4Fp-C-k3gObuKpNFH4oz68vo4IFdND0RpCHPbMYRs"


url = "https://api.hyperbolic.xyz/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ6aGFzaDIzMDhAbWFpbC5ydSIsImlhdCI6MTczMzkzNzM1NX0.bL4Fp-C-k3gObuKpNFH4oz68vo4IFdND0RpCHPbMYRs"
}
data = {
    "messages": [
        {
            "role": "user",
            "content": "Расскажи кратко как не откладывать на завтра?"
        }
    ],
    "model": "meta-llama/Llama-3.3-70B-Instruct",
    "max_tokens": 8192,
    "temperature": 0.1,
    "top_p": 0.9
}


def getAnswer(message):
    while True:
        try:
            data['messages'][0]['content'] = message
            response = requests.post(url, headers=headers, json=data)
            response = response.json()
            return response
        except Exception:
            try:
                ## Обновление контекста в случае неудачного получения ответа от api
                data['messages'][0]['content'] = "Расскажи о картошке"
                response = requests.post(url, headers=headers, json=data)
            except Exception:
                print("decode error")
            print("decode error")
            time.sleep(5)

