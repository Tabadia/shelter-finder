import uuid

import boto3
from boto3.dynamodb.conditions import Key

from dotenv import load_dotenv
import os

load_dotenv()

from models import Shelter, ShelterPost, User, Reservation

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
client_table_name = 'clients'
reservation_table_name = 'Reservations'

shelter_table = dynamodb.Table(shelter_table_name)
user_table = dynamodb.Table(client_table_name)
reservation_table = dynamodb.Table(reservation_table_name)

# Shelter Methods
def get_all_shelters():
    response = shelter_table.scan()
    return response.get('Items', [])

def get_my_shelters(owner_id: int):
    response = user_table.get_item(Key={'id': owner_id})
    item = response.get('Item', {})
    if item:
        ret = []
        p = item.get('shelters_ids', [])
        for x in p:
            ret.append(get_shelter_by_id(x))
        return ret
    else:
        return []


def get_shelter_by_id(shelter_id):
    response = shelter_table.get_item(Key={'ShelterID': shelter_id})
    return response.get('Item', {})
    


def post_shelter(shelter: ShelterPost):
    shelter.ShelterID = str(uuid.uuid4())
    shelter_table.put_item(Item=shelter.dict())
    # add shelter.ShelterID to client table
    # user_table.update_item(
    #     Key={'username': clientUsers},
    #     UpdateExpression='SET #shelter_id = :shelter_id',
    #     ExpressionAttributeNames={'#shelter_id': 'ShelterID'},
    #     ExpressionAttributeValues={':shelter_id': shelter.ShelterID}
    # )
    return shelter

def update_shelter(shelter_id, updates):
    update_expression = 'set '
    expression_attribute_values = {}
    attribute_names = {}

    for key, value in updates.items():
        update_expression += f'#{key} = :{key}, '
        expression_attribute_values[f':{key}'] = value
        attribute_names[f'#{key}'] = key

    update_expression = update_expression[:-2]  # Remove trailing comma and space

    shelter_table.update_item(
        Key={'ShelterID': shelter_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=attribute_names
    )
    return get_shelter_by_id(shelter_id)

# def put_shelter_by_id(shelter):
#     shelter_id = shelter['ShelterID']
#     response = table.put_item(
#         Item=shelter
#     )
#     return response


def delete_shelter(shelter_id):
    shelter_table.delete_item(Key={'ShelterID': shelter_id})

# User Methods



def get_all_users():
    response = user_table.scan()
    return response.get('Items', [])

def get_user_by_username(username):
    response = user_table.get_item(Key={'username': username})  
    return response.get('Item', {})

def post_user(user: User):
    user_item = user.model_dump()  
    print("User Item:", user_item)  

    if 'username' not in user_item:
        raise ValueError("Error: 'username' is missing from user_item!")

    existing_user = get_user_by_username(user_item['username'])
    if existing_user:
        raise ValueError(f"User with username {user_item['username']} already exists.")

    user_table.put_item(Item=user_item)
    return user


def update_user(username, updates):
    update_expression = 'SET '
    expression_attribute_values = {}
    expression_attribute_names = {}

    for key, value in updates.items():
        update_expression += f'#{key} = :{key}, '
        expression_attribute_values[f':{key}'] = value
        expression_attribute_names[f'#{key}'] = key

    update_expression = update_expression.rstrip(', ')

    user_table.update_item(
        Key={'username': username},  
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names
    )
    return get_user_by_username(username)

def delete_user(username):
    user_table.delete_item(Key={'username': username}) 

 
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