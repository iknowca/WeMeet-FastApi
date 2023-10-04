import openai
import requests

spring_url = "http://localhost:7777"

def recommendation(message):

    res = requests.get(spring_url+'/ml/moim/list')

    resJson = res.json()
    for i in range(len(res.json())):
        resJson[i]["link"] = "http://localhost:8080/moim/"+str(resJson[i]['id'])

    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "유저에게 여행 모임을 추천하는 서비스 get moim의 한국어 상담사 봇"},

            {"role": "user", "content": "여행지 추천해줘"},
            {
                "role": "assistant", "content": str(resJson)
            },
            {
                "role": "assistant", "content": "installment를 할부금이 아니라 월 납부금으로 표현해줘"
            },
            {
                "role": "assistant", "content": "입력받은 객체는 각각 여행 모임이야"
            },
            {
                "role": "assistant", "content": "먼저 여행지를 추천해주고 그 다음으로 해당 여행지의 정보를 소개해주고 해당 여행지를 도착지로 하는 모임을 최대 3개씩만 추천해줘"
            },
            {
                "role": "assistant", "content": "시기는 제공된 모임의 정보를 토대로 추천해줘"
            },
            {
                "role": "assistant", "content": "모임의 여행지는 제공된 데이터의 country, city야"
            }]
    )
    print(completion["choices"][0]["message"]["content"])

