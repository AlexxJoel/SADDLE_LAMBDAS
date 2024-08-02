import json
import logging
from connection_db import connect_db, close_connection, execute_query


def lambda_handler(event, __):
    # Query to get all catalog items
    query = "SELECT * FROM catalogue_saddle"

    # Connect to database
    conn = connect_db()

    if conn:
        try:
            # Execute query
            response = execute_query(conn, query)
            #close connection
            close_connection(conn)

            if response:
                logging.info("Catalog items retrieved successfully")
                for item in response:
                    logging.info(item)

                # return success response
                return {
                    'statusCode': 200,
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
                    "message": "An error occurred while retrieving catalog items",
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


# print(lambda_handler(None, None))
