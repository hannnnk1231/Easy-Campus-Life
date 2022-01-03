import json
import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
HOST = "https://search-easycampuslife-7s3grzsfhmyzcg4l7rfht23onu.us-east-1.es.amazonaws.com/"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
def uploadES(w_id, channel, username, time, content):
    body = {
        'w_id': w_id,
        'channel': channel,
        'time': time,
        'username': username,
        'content': content
    }
    query = HOST + 'feeds/_doc/'
    response = requests.post(query, auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
    return response.text

def lambda_handler(event, context):
    # TODO implement
    response = uploadES(event["w_id"], event["channel"], event["username"], event["time"], event["content"])
    print(response)
    return {
        'statusCode': 200,
        'body': response,
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
