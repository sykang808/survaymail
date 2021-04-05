import os
import json
from flask import Flask
from flask_restx import Resource, Api
from flask import Flask, request # change
from flask_cors import CORS, cross_origin
import boto3
from botocore.exceptions import ClientError
from sns_basics import SnsWrapper

TOPIC_ARN = 'arn:aws:sns:ap-northeast-2:566034038752:survay'
SUBSCRIPTION_ARN = 'arn:aws:sns:ap-northeast-2:566034038752:survay:b21a8f09-cb69-4d28-ac10-b5df980e9f09'

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'*': {'origins': '*'}})
     
 
@api.route('/survay')
@api.response(404, "Could not put user")
class SurvayPost(Resource):
    def post(self):
        data = request.get_json(force=True)
        return {}, 200

 
@api.route('/')
class Main(Resource):
    def get(self):
        return 200

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=80, debug=False)
