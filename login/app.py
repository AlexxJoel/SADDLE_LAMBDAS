import json
import boto3
from botocore.exceptions import ClientError
import logging

# configure the logger
logging.basicConfig(level=logging.ERROR)


def lambda_handler(event, __):
    # configure the cognito client
    client = boto3.client('cognito-idp')
    client_id = "akfc6urniac9vviree6eg98e7"

    try:
        body_parameters = json.loads(event["body"])
        email = body_parameters.get('email')
        password = body_parameters.get('password')

        logging.info(f"Email: {email}")
        logging.info(f"Password: {password}")

        # validate if the data exist
        if not email or not password:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Email and password are required"})
            }
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        logging.info(response)

        if 'ChallengeName' in response and response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            return {
                'statusCode': 401,
                'body': json.dumps({"error": "Access denied. Please, change the temporary password."})
            }

        id_token = response['AuthenticationResult']['IdToken']
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']

        # Get the user group
        user_groups = client.admin_list_groups_for_user(
            Username=email,
            UserPoolId='us-west-1_WUespA4kW'
        )

        # Determine the role based on the group
        role = None
        if user_groups['Groups']:
            role = user_groups['Groups'][0]['GroupName']  # Assuming a user belongs to a single group

        return {
            'statusCode': 200,
            'body': json.dumps({
                'id_token': id_token,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'role': role
            })
        }
    except ClientError as e:
        logging.error(e)
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({"error": e.response['Error']['Message']})
        }
    except Exception as e:
        logging.error(e)
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }


# example of using the function
# if __name__ == "__main__":
#     email = '20213tn019@utez.edu.mx'
#     password = 'Alejandro1.'
#
#     event = {
#         "body": json.dumps({
#             "email": email,
#             "password": password
#         })
#     }
#
#     print(lambda_handler(event, None))
