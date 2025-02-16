import uuid
import json
from summary import gen_summary

import boto3
from boto3.dynamodb.conditions import Key

from dotenv import load_dotenv
import os

load_dotenv()

from models import Shelter, ShelterPost, User, Reservation, ClientPost, ClientLogin

# Initialize DynamoDB resource
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

dynamodb = session.resource('dynamodb')

# Specify the table names
shelter_table_name = 'Shelters'
# user_table_name = 'Users'
client_table_name = 'Clients'
reservation_table_name = 'Reservations'

shelter_table = dynamodb.Table(shelter_table_name)
client_table = dynamodb.Table(client_table_name)
reservation_table = dynamodb.Table(reservation_table_name)

# Shelter Methods
def get_all_shelters():
    response = shelter_table.scan()
    return response.get('Items', [])

def get_my_shelters(owner_username: str):
    response = client_table.get_item(Key={'username': owner_username})
    print('cc', response)
    item = response.get('Item', {})
    if item:
        ret = []
        p = item.get('shelters_ids', [])
        for x in p:
            c = get_shelter_by_id(x)
            print('c', c)
            ret.append(c)
        return ret
    else:
        return []


def get_shelter_by_id(shelter_id):
    response = shelter_table.get_item(Key={'ShelterID': shelter_id})
    return response.get('Item', {})
    
def verify(s: ShelterPost):
    with open("santa_clara_shelters.json", "r") as file:
        verified_shelters = set(json.load(file)["shelters"])

    if s.name in verified_shelters:
        print("changed verification")
        return True

    else:
        return False

def post_shelter(shelter: ShelterPost):
    shelter.ShelterID = str(uuid.uuid4())
    shelter.verif = verify(shelter)
    shelter.summary = gen_summary(shelter.name, shelter.queue, shelter.curr_cap, shelter.capacity, shelter.resources, shelter.type)
    
    # owner_username = shelter.owner_username
    owner_username = 'bobjoe'
    del shelter.owner_username
    # print('shelter', shelter)
    shelter_table.put_item(Item=shelter.dict())
    # add shelter.ShelterID to client table
    client = get_user_by_username(owner_username)
    if 'shelters_ids' not in client:
        client['shelters_ids'] = []
    user = update_user(owner_username, {'shelters_ids': client['shelters_ids'] + [shelter.ShelterID]})
    # client_table.update_item(
    #     Key={'username': clientUsers},
    #     UpdateExpression='SET #shelter_id = :shelter_id',
    #     ExpressionAttributeNames={'#shelter_id': 'ShelterID'},
    #     ExpressionAttributeValues={':shelter_id': shelter.ShelterID}
    # )
    print('user', user)
    return shelter

def update_shelter(shelter):
    shelter.summary = gen_summary(shelter.name, shelter.queue, shelter.curr_cap, shelter.capacity, shelter.resources, shelter.type)
    response = shelter_table.put_item(
        Item=shelter.dict()
    )
    return response

# def put_shelter_by_id(shelter):
#     


def delete_shelter(shelter_id):
    shelter_table.delete_item(Key={'ShelterID': shelter_id})

# User Methods



def get_all_users():
    response = client_table.scan()
    return response.get('Items', [])

def get_user_by_username(username):
    response = client_table.get_item(Key={'username': username})  
    return response.get('Item', {})

def post_user(user: ClientPost):
    user.id = str(uuid.uuid4())
    client_table.put_item(Item=user.dict())
    return user

def check_client_login(user: ClientLogin):
    response = client_table.get_item(Key={'username': user.username})  
    item = response.get('Item', {})
    if item:
        if item['password'] == user.password:
            return 0 # passowrd true, forward user to client dashbaord
        return 1 # password false, ask user to re-enter password
    return 2 # user not found, ask user to sign up


def update_user(username, updates):
    update_expression = 'SET '
    expression_attribute_values = {}
    expression_attribute_names = {}

    for key, value in updates.items():
        update_expression += f'#{key} = :{key}, '
        expression_attribute_values[f':{key}'] = value
        expression_attribute_names[f'#{key}'] = key

    update_expression = update_expression.rstrip(', ')

    client_table.update_item(
        Key={'username': username},  
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names
    )
    return get_user_by_username(username)

def delete_user(username):
    client_table.delete_item(Key={'username': username}) 

 
# print(get_all_users())
# Reservation Methods
def get_all_reservations():
    response = reservation_table.scan()
    return response.get('Items', [])

def get_reservation_by_id(reservation_id):
    response = reservation_table.get_item(Key={'id': reservation_id})
    return response.get('Item', {})

def post_reservation(reservation: Reservation):
    reservation_table.put_item(Item=reservation.dict())
    return reservation

def update_reservation(reservation_id, updates):
    update_expression = 'set '
    expression_attribute_values = {}
    attribute_names = {}

    for key, value in updates.items():
        update_expression += f'#{key} = :{key}, '
        expression_attribute_values[f':{key}'] = value
        attribute_names[f'#{key}'] = key

    update_expression = update_expression[:-2]  # Remove trailing comma and space

    reservation_table.update_item(
        Key={'id': reservation_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=attribute_names
    )
    return get_reservation_by_id(reservation_id)

def delete_reservation(reservation_id):
    reservation_table.delete_item(Key={'id': reservation_id})