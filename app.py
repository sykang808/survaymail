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

TOPIC_ARN = 'arn:aws:sns:ap-northeast-2:566034038752:survay'
SUBSCRIPTION_ARN = 'arn:aws:sns:ap-northeast-2:566034038752:survay:b21a8f09-cb69-4d28-ac10-b5df980e9f09'

 
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'*': {'origins': '*'}})

def test_publish_message(make_stubber, error_code):
    sns_resource = boto3.resource('sns')
    sns_stubber = make_stubber(sns_resource.meta.client)
    sns_wrapper = SnsWrapper(sns_resource)
    topic = sns_resource.Topic(TOPIC_ARN)
    message = 'test-message'
    attributes = {'test': 'string', 'bintest': b'binary'}
    message_id = 'msg-id'

    sns_stubber.stub_publish(
        message, message_id, topic_arn=topic.arn, message_attributes=attributes,
        error_code=error_code)

    if error_code is None:
        got_message_id = sns_wrapper.publish_message(topic, message, attributes)
        assert got_message_id == message_id
    else:
        with pytest.raises(ClientError) as exc_info:
            sns_wrapper.publish_message(topic, message, attributes)
        assert exc_info.value.response['Error']['Code'] == error_code

 
@api.route('/survay')
@api.response(404, "Could not put survay")
class SurvayPost(Resource):
    def post(self):
        data = request.get_json(force=True)
        client = boto3.client('sns',region_name='us-west-2')
        response = client.publish(
            TopicArn='arn:aws:sns:ap-northeast-2:566034038752:survay',    
            Message= json.dumps(data)
        )
        return "Response: {}".format(response), 200

 
@api.route('/')
class Main(Resource):
    def get(self):
        return 200

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=80, debug=False)
