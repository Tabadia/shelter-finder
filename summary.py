# import boto3
# import os
# from dotenv import load_dotenv
# from aws import get_all_shelters

# load_dotenv()

# def gen_summary(shelter_name, queue, curr_cap, capacity, resources, type):
#     access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
#     secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

#     client = boto3.client(
#         service_name="bedrock-runtime",
#         aws_access_key_id=access_key_id,
#         aws_secret_access_key=secret_access_key,
#         region_name="us-west-2",
#     )

#     input_text = f"""
#     The following is information about the emergency shelter named {shelter_name}:

#     - **Queue** (people waiting/on their way): {queue}
#     - **Current Capacity** (people staying): {curr_cap}/{capacity}
#     - **Available Resources**: {resources}
#     - **Shelter Type**: {type}

#     Generate a concise and actionable summary to help this shelter prepare for incoming residents and optimize its resources for emergency preparedness.
#     """

#     message = {
#         "role": "user",
#         "content": [{"text": input_text}]
#     }

#     messages = [message]
#     model_id = "claude-3-5-haiku-20241022"

#     response = client.converse(
#         modelId=model_id,
#         messages=messages
#     )

#     return response['output']['message']['content']

# name = "Catholic Charities"

# print(gen_summary(name, 10, 50, 100, "food and water", "hospital"))