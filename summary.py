import boto3
import os
from dotenv import load_dotenv
# from aws import get_all_shelters

load_dotenv()

def gen_summary(shelter_name, queue, curr_cap, capacity, resources, type):
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    client = boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name="us-west-2",
    )

    # improve
    input_text = f"""
    The following is information about the emergency shelter named {shelter_name}:

    - **Queue** (people waiting/on their way): {queue}
    - **Current Capacity** (people staying): {curr_cap}/{capacity}
    - **Available Resources**: {resources}
    - **Shelter Type**: {type}

    Generate a concise and actionable summary to help this shelter prepare for incoming residents and optimize its resources for emergency preparedness. Provide this summary
    in paragraph form, do not format it in any way. It should only be full sentences.
    """

    message = {
        "role": "user",
        "content": [{"text": input_text}]
    }

    messages = [message]
    model_id = "anthropic.claude-3-5-haiku-20241022-v1:0"

    response = client.converse(
        modelId=model_id,
        messages=messages
    )

    return response['output']['message']['content'][0]['text']