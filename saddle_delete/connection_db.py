import psycopg2
import logging

# Config logging
logging.basicConfig(level=logging.INFO)


def connect_db():
    try:
        host = 'ep-gentle-mode-a4hjun6w-pooler.us-east-1.aws.neon.tech'
        user = 'default'
        password = 'pnQI1h7sNfFK'
        database = 'verceldb'
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        logging.info("Connected to database")
        return conn
    except Exception as e:
        logging.error("Error connecting to database: %s", e)
        raise e


def execute_query(conn, query, data: tuple):
    try:
        # transaction
        conn.autocommit = False

        with conn.cursor() as cur:
            cur.execute(query, data)
            logging.info("Query executed successfully")

            # commit query
            conn.commit()
            result = cur.fetchall()

            return result

    except Exception as e:
        logging.error("Error executing query: %s", e)
        conn.rollback()  # Rollback the transaction on error
        raise e
    finally:
        conn.autocommit = True  # Set autocommit to True


def close_connection(conn):
    try:
        conn.close()
        logging.info("Connection closed")
    except Exception as e:
        logging.error("Error closing connection: %s", e)
        raise e
