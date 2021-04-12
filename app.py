import os
import json
from flask import Flask
from flask_restx import Resource, Api
from flask import Flask, request # change
from flask_cors import CORS, cross_origin
import boto3
from botocore.exceptions import ClientError
from sns_basics import SnsWrapper
import pytest

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'*': {'origins': '*'}})

 
@api.route('/survay')
@api.response(404, "Could not put survay")
class SurvayPost(Resource):
    def post(self):
        t_data = request.get_json(force=True)
        client = boto3.client('sns',region_name='us-west-2')
        response = client.publish(
            TopicArn='arn:aws:sns:us-west-2:566034038752:survay',    
            Message= json.dumps(data=t_data, ensure_ascii = False )
        )
        return "Response: {}".format(response), 200

 
@api.route('/')
class Main(Resource):
    def get(self):
        return 200

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=80, debug=False)
