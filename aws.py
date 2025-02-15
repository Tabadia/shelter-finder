import boto3
from dotenv import load_dotenv
import os

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('Shelters')

def get_all_shelters():
    response = table.scan()
    shelters = response['Items']
    return shelters


def get_shelter_by_id(shelter_id):
    response = table.get_item(
        Key={
            'ShelterID': shelter_id
        }
    )
    return response.get('Item', None)

def put_shelter_by_id(shelter):
    shelter_id = shelter['ShelterID']
    response = table.put_item(
        Item=shelter
    )
    return response

def delete_shelter_by_id(shelter_id):
    response = table.delete_item(
        Key={
            'ShelterID': shelter_id
        }
    )
    return response

def post_shelter(shelter):
    response = table.put_item(
        shelter
    )
    return response

def add_client():
    userlist = []
    username = input('Enter Your Username: ')
    userlist.append(username)
    for i in userlist(0,len(userlist),1):
        if userlist[i] == username:
            print('Username Already Taken')
            username = input('Enter Your Username: ')
    password = input('Enter Your Password: ')
    if username = 