import json
import logging
from connection_db import connect_db, close_connection, execute_query


def lambda_handler(event, __):
    # Query to get all catalog items
    query = "SELECT * FROM catalogue_saddle"

    # Connect to database
    conn = connect_db()

    # Handle CORS preflight request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,PUT'
            },
            'body': ''
        }

    headers_response = {
        'Access-Control-Allow-Origin': '*'
    }

    if conn:
        try:
            # Execute query
            response = execute_query(conn, query)
            # Close connection
            close_connection(conn)

            if response:
                logging.info("Catalog items retrieved successfully")
                for item in response:
                    logging.info(item)

                # Return success response
                return {
                    'statusCode': 200,
                    'headers': headers_response,
                    'body': json.dumps({
                        "message": "Catalog items retrieved successfully",
                        "data": {
                            "items": response,
                            "total_items": len(response)
                        },
                        "statusCode": 200,
                        "error": False,
                    })
                }
            else:
                logging.info("Empty response")
                return {
                    'statusCode': 204,
                    'headers': headers_response,
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
                'headers': headers_response,
                'body': json.dumps({
                    "message": "An error occurred while retrieving catalog items",
                    "statusCode": 500,
                    "error": True,
                })
            }
    else:
        logging.error("Error connecting to database")
        return {
            'statusCode': 500,
            'headers': headers_response,
            'body': json.dumps({
                "message": "An error occurred while connecting to the database",
                "statusCode": 500,
                "error": True,
            })
        }


# Uncomment the following line for local testing
# print(lambda_handler(None, None))
if __name__ == "__main__":
    event = {
        'httpMethod': 'GET',
    }
    print(lambda_handler(event, None))
