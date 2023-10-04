import openai
import requests

spring_url = "http://get-moim.shop:7777"

def recommendation(message):

    res = requests.get(spring_url+'/ml/moim/list')

    resJson = res.json()
    for i in range(len(res.json())):
        resJson[i]["link"] = "<a href="'http://get-moim.shop:8080/moim/'+str(resJson[i]['id'])+"> 링크</a>"

    f = open("./aikey", 'r')
    openai.api_key = f.readline()
    completion = openai.ChatCompletion.create(
        stream=False,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 유저에게 여행 모임을 추천하는 서비스 get moim의 모임 추천 봇 M이야."},

            {"role": "user", "content": message},
            {
                "role": "assistant", "content": "현재 생성되어 있는 여행 모임: " + str(resJson)
            },
            {
                "role": "system", "content": "installment를 할부금이 아니라 월 납부금으로 표현해줘"
            },
            {
                "role": "system", "content": "입력받은 객체는 각각 여행 모임이야"
            },
            {
                "role": "system", "content": "먼저 사용자의 질문에 해당하는 여행지를 추천해주고 그 다음으로 해당 여행지의 정보를 소개해주고 해당 여행지를 도착지로 하는 모임을 최대 3개만 추천해줘"
            },
            {
                "role": "system", "content": "출발날짜는 제공된 모임의 정보를 토대로 추천해줘"
            },
            {
                "role": "system", "content": "모임의 여행지는 제공된 데이터의 country, city야"
            },
            {
                "role": "system", "content": "존대말로 대답해줘"
            },
            {
                "role": "system", "content": "추천 해줄 여행 모임이 존재하지 않는다면, link: http://get-moim.shop:8080/moim/form 페이지에서 직접 모임을 생성하도록 제안해줘"
            },
            {
                "role": "system", "content": "할부라는 표현을 사용하지 말고 월 납부금이라고 표현해줘 "
            },
            {
                "role": "system", "content": "현재 생성되어 있는 모임 안에서만 추천해주고, 만약 추천해주는 지역을 떠나는 모임이 존재하지 않는다면 http://get-moim.shop:8080/moim/form 에서 직접 모임을 생성할 수 있다고 추천해줘"
            },
            {
                "role": "system", "content": "모임을 추천해 줄때는 반드시 마지막에 링크를 포함해줘 모임의 링크는 http://get-moim.shop:8080/moim/[moimId] 의 형식이야"
            },
        ]
    )
    return completion["choices"][0]["message"]["content"]


