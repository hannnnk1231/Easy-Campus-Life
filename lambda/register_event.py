import json
import boto3
import requests
import uuid
from requests_aws4auth import AWS4Auth
from boto3.dynamodb.conditions import Attr

region = 'us-east-1'
service = 'es'
HOST = "https://search-easycampuslife-7s3grzsfhmyzcg4l7rfht23onu.us-east-1.es.amazonaws.com/"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


def pull_info(username):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Profile-zvvjx5wqajabjkac7tm6ise3qu-dev')
    try:
        response = table.scan(FilterExpression=Attr('id').eq(username))
        info = response["Items"]
        while('LastEvaluatedKey' in response):
            LastEvaluatedKey = response['LastEvaluatedKey']
            response = table.scan(FilterExpression=Attr('id').eq(username), ExclusiveStartKey=LastEvaluatedKey)
            info += response["Items"]
        info = info[0]
    except IndexError:
        logger.debug("Error pull user {} info from dynamodb".format(username))
        return
    return info
    
def send_email(e_id, username):
    userinfo = pull_info(username)
    email = userinfo['email'] if ("email" in userinfo and ['email'] != "") else "mh6069@nyu.edu"
    response = requests.post(HOST+"events/_search?q=_id:{}&size=10000".format(e_id), auth=awsauth, headers={"Content-Type":"application/json"})
    event = json.loads(response.text)['hits']['hits'][0]["_source"]
    ses_client = boto3.client('ses', region_name= 'us-east-1')
    msg = """Hi {},
You've successfully registered for the event: "{}"
Following is the event details:
Host: {}
Date: {}
Time: {}
Location: {}
Contact: {}
Cost: {}

Looking forward to see you there!

Best,
Easy Campus Life""".format(userinfo["displayName"], event["name"], event["host"], event["date"], event["time"], event["location"], event["contact"], event["cost"])
    ses_client.send_email(
        Destination = {
            "ToAddresses": [email],
        },
        Message = {
            "Body": {
                "Text": {
                    "Charset": "UTF-8",
                    "Data": msg,
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": "Easy Campus Lift: Your Event Registration",
            },
        },
        Source="mh6069@nyu.edu",
    )

def registerEvent(e_id, username):
    response = requests.get(HOST+'event_user/_search?q=username:{}&size=10000'.format(username), auth=awsauth, headers={'Content-type': 'application/json'})
    events = [e["_source"] for e in json.loads(response.text)['hits']['hits'] if e["_source"]['e_id']==e_id]
    if not events:
        body = {
            'e_id': e_id,
            'username': username
        }
        response = requests.post(HOST+'event_user/_doc/', auth=awsauth, data=json.dumps(body), headers={'Content-type': 'application/json'})
        send_email(e_id, username)
        return "success register for the event"
    else:
        return "You have already registered for this event"
    
def lambda_handler(event, context):
    # TODO implement

    response = registerEvent(event["e_id"], event["username"])
        
    return {
        'statusCode': 200,
        'body': response,
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
    }
