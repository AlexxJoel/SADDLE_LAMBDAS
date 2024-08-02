import json
import logging
from connection_db import connect_db, close_connection, execute_query

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, __):
    path_parameters = event['pathParameters']
    id_request = path_parameters.get('id')

    if not id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": "Invalid request. Missing required parameters",
                "statusCode": 400,
                "error": True,
            })
        }

    # Query to get all catalog items
    query = """DELETE FROM catalogue_saddle WHERE id = %s RETURNING id"""
    data = (id_request,)  # same order as the query

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
                logging.info("saddle item deleted successfully")
                logging.info(response)

                # return success response
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "saddle deleted successfully",
                        "data": {
                            "id": response[0][0],
                        },
                        "statusCode": 200,
                        "error": False,
                    })
                }
            else:
                logging.info("No record deleted")
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        "message": "No record found to delete",
                        "statusCode": 404,
                        "error": False,
                    })
                }
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    "message": "An error occurred while deleting catalog items",
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
#         'pathParameters': {
#             'id': 8
#         }
#     }
#
#     resp = lambda_handler(event, None)
#
#     print(resp)
