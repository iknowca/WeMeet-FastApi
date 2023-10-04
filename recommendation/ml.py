import json

import requests
import pickle
import numpy as np
import matplotlib.pyplot as plt

spring_url = "http://get-moim.shop:7777"
with open('./recommendation/saved_mean_shift_model', 'rb') as f:
    model = pickle.load(f)
with open("./recommendation/saved_mean_shift_model_range", 'rb') as f:
    clusters = pickle.load(f)


def recommendation(args):
    res = requests.get(spring_url + '/ml/moim/list/v2')
    resJson = res.json()
    label = model.predict(np.array([[float(args['income']), float(args['outcome'])]]))[0]
    print(label)
    major_axis = clusters['major_axis_list'][label]
    minor_axis = clusters['minor_axis_list'][label]
    ellipse_x = clusters['ellipse_x_list'][label]
    ellipse_y = clusters['ellipse_y_list'][label]

    moimIdList = []
    for i in resJson:
        if create_ellipse_equation(i["totalPrice"]/10000, i["numInstallment"], major_axis, minor_axis, ellipse_x, ellipse_y):
            moimIdList.append(i["id"])

    headers = {'Content-Type': 'application/json'}
    idListJson = json.dumps(moimIdList)
    res2 = requests.post(spring_url +'/ml/moim/list/v2',  idListJson, headers=headers)
    print(res2)
    return res2.json()


def create_ellipse_equation(x, y, major_axis, minor_axis, ellipse_x, ellipse_y):
    distance_x = (x - ellipse_x) / major_axis[0]
    distance_y = (y - ellipse_y) / minor_axis[1]
    return (distance_x ** 2 + distance_y ** 2 <= 1).any()
