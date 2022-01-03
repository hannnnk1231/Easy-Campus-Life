import json
import boto3
import requests
import uuid
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
HOST = "https://search-easycampuslife-7s3grzsfhmyzcg4l7rfht23onu.us-east-1.es.amazonaws.com/"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
def createEvent(e_name, e_img, e_content, e_host, e_date, e_time, e_location, e_contact, e_cost):
    body = {
        'name': e_name,
        'img': e_img,
        'content': e_content,
        'host': e_host,
        'date': e_date,
        'time': e_time,
        'location': e_location,
        'contact': e_contact,
        'cost': e_cost
    }
    response = requests.post(HOST+'events/_doc/', auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
    e_id = json.loads(response.text)['_id']
    return e_id

def lambda_handler(event, context):
    # TODO implement
    response = createEvent(event["e_name"], event["e_img"], event["e_content"], event["e_host"], event["e_date"], event["e_time"], event["e_location"], event["e_contact"], event["e_cost"])
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
