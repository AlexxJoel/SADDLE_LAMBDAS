import json
import logging
from connection_db import connect_db, close_connection, execute_query

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, __):
    body_parameters = json.loads(event['body'])
    brand = body_parameters.get('brand')
    model = body_parameters.get('model')
    material = body_parameters.get('material')
    size = body_parameters.get('size')

    if not brand or not model or not material or not size:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": "Invalid request. Missing required parameters",
                "statusCode": 400,
                "error": True,
            })
        }

    # Query to get all catalog items
    query = """INSERT INTO catalogue_saddle (brand, model, material, "size") VALUES ( %s, %s, %s, %s) RETURNING *"""
    # same order as the query
    data = (brand, model, material, size)

    # Connect to database
    conn = connect_db()

    if conn:
        try:
            # prepare data to be inserted
            # Execute query
            response = execute_query(conn, query, data)
            #close connection
            close_connection(conn)

            if response:
                logging.info("saddle items retrieved successfully")
                logging.info(response)

                # return success response
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "saddle saved successfully",
                        "data": response,
                        "statusCode": 200,
                        "error": False,
                    })
                }
            else:
                logging.info("Empty response")
                return {
                    'statusCode': 204,
                    'body': json.dumps({
                        "message": "No records found",
                        "statusCode": 204,
                        "error": False,
                    })
                }
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    "message": "An error occurred while saving saddle",
                    "statusCode": 500,
                    "error": True,
                })
            }
    else:
        logging.error("Error connecting to database")
        return {
            'statusCode': 500,
            'body': json.dumps({
                "message": "An error occurred while connecting to the database",
                "statusCode": 500,
                "error": True,
            })
        }

# if __name__ == "__main__":
#     event = {
#         'body': json.dumps({
#             "brand": "brand",
#             "model": "model",
#             "material": "material",
#             "size": "size"
#         })
#     }
#     resp = lambda_handler(event, None)
#     print(resp)

