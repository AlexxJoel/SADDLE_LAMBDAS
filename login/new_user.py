import json
import boto3
import logging
from botocore.exceptions import ClientError

def login_user(email, password):
    # Inicializar el cliente de Cognito
    client = boto3.client('cognito-idp')
    client_id = "akfc6urniac9vviree6eg98e7"

    try:
        # Llamar a initiate_auth para autenticar al usuario
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return response
    except ClientError as e:
        # Manejar posibles errores de autenticación
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            return 'Incorrect username or password.'
        elif e.response['Error']['Code'] == 'UserNotFoundException':
            return 'User does not exist.'
        else:
            return f'An error occurred: {e.response["Error"]["Message"]}'

def new_password_challenge(email, new_password, session):
    #  initialize the cognito client
    client = boto3.client('cognito-idp')
    client_id = "akfc6urniac9vviree6eg98e7"

    try:
        response = client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            Session=session,
            ChallengeResponses={
                'NEW_PASSWORD': new_password,
                'USERNAME': email
            }
        )
        logging.info('New password set: %s', response)
        return response
    except ClientError as e:
        logging.error('Error setting new password: %s', e)
        return f'An error occurred: {e}'

    except Exception as e:
        logging.error('Error setting new password: %s', e)
        return f'An error occurred: {e}'


# example of using the function
if __name__ == "__main__":
    email = '20213tn019@utez.edu.mx'
    password = 'Alejandro1.'
    new_password = 'Alejandro1.'

    event = {
        "body": json.dumps({
            "email": email,
            "password": password
        })
    }

    auth_response = login_user(email, password)
    print(auth_response)

    # verify if the user needs to change the password
    if 'ChallengeName' in auth_response and auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
        session = auth_response['Session']
        new_password_response = new_password_challenge(email, new_password, session)
        print(new_password_response)
    else:
        print('User does not need to change the password.')
