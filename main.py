# -*- coding: utf8 -*-
import flask
from flask import Flask
import recommendation.ml as ml
import recommendation.llm as llm
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {"origin": "*"}
})


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/recommendation/ml', methods=["get"])
def recommendationML():
    args = flask.request.args
    args = args.to_dict()
    return ml.recommendation(args)


@app.route("/recommendation/gpt", methods=["POST", "OPTIONS"])
def recommendationLLM():
    if (flask.request.method == "OPTIONS"):
        print("PreFlight")
        return {"success": True}

    requestJson = flask.request.get_json()
    return llm.recommendation(requestJson["message"])


if __name__ == '__main__':
    app.run(port=8001)
