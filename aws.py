import uuid

import boto3
from dotenv import load_dotenv
import os

load_dotenv()

from models import Shelter, User, Reservation

# Initialize DynamoDB resource
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

dynamodb = session.resource('dynamodb')

# Specify the table names
shelter_table_name = 'Shelters'
user_table_name = 'Users'
reservation_table_name = 'Reservations'

shelter_table = dynamodb.Table(shelter_table_name)
user_table = dynamodb.Table(user_table_name)
reservation_table = dynamodb.Table(reservation_table_name)

# Shelter Methods
def get_all_shelters():
    response = shelter_table.scan()
    return response.get('Items', [])

def get_shelter_by_id(shelter_id):
    response = shelter_table.get_item(Key={'ShelterID': shelter_id})
    return response.get('Item', {})

def post_shelter(shelter: Shelter):
    shelter_table.put_item(Item=shelter.dict())
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

def delete_shelter(shelter_id):
    shelter_table.delete_item(Key={'ShelterID': shelter_id})

# User Methods
def get_all_users():
    response = user_table.scan()
    return response.get('Items', [])

def get_user_by_id(user_id):
    response = user_table.get_item(Key={'id': user_id})
    return response.get('Item', {})

def post_user(user: User):
    user_table.put_item(Item=user.dict())
    return user

def update_user(user_id, updates):
    update_expression = 'set '
    expression_attribute_values = {}
    attribute_names = {}

    for key, value in updates.items():
        update_expression += f'#{key} = :{key}, '
        expression_attribute_values[f':{key}'] = value
        attribute_names[f'#{key}'] = key

    update_expression = update_expression[:-2]  # Remove trailing comma and space

    user_table.update_item(
        Key={'id': user_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=attribute_names
    )
    return get_user_by_id(user_id)

def delete_user(user_id):
    user_table.delete_item(Key={'id': user_id})

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