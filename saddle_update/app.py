import json
import logging
from connection_db import connect_db, close_connection, execute_query

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, __):
    body_parameters = json.loads(event['body'])
    id_request = body_parameters.get('id')
    brand = body_parameters.get('brand')
    model = body_parameters.get('model')
    material = body_parameters.get('material')
    size = body_parameters.get('size')

    if not id_request or not brand or not model or not material or not size:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": "Invalid request. Missing required parameters",
                "statusCode": 400,
                "error": True,
            })
        }

    # Query to get all catalog items
    query = """UPDATE catalogue_saddle
               SET brand = %s, model = %s, material = %s, "size" = %s 
               WHERE id = %s 
               RETURNING id"""
    data = (brand, model, material, size, id_request)  # same order as the query

    # Connect to database
    conn = connect_db()

    if conn:
        try:
            # prepare data to be inserted
            # Execute query
            response = execute_query(conn, query, data)
            # close connection
            close_connection(conn)

            if response:
                logging.info("saddle item updated successfully")
                logging.info(response)

                # return success response
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "saddle updated successfully",
                        "data": {
                            "id": response[0][0],
                        },
                        "statusCode": 200,
                        "error": False,
                    })
                }
            else:
                logging.info("No records updated")
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        "message": "No record found to update",
                        "statusCode": 404,
                        "error": False,
                    })
                }
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    "message": "An error occurred while updating catalog items",
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
#             "id": 6,
#             "brand": "TOYOTA",
#             "model": "model",
#             "material": "material",
#             "size": "size"
#         })
#     }
#     resp = lambda_handler(event, None)
#     print(resp)
