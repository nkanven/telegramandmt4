import logging
import os
import mysql.connector
from mysql.connector import Error

# Enable logging
logging.basicConfig(
    filename="error.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def connect():
    try:
        connection = mysql.connector.connect(host=os.getenv('DATABASE_HOST'),
                                             database=os.getenv('DATABASE'),
                                             user=os.getenv('DATABASE_USER'),
                                             password=os.getenv('DATABASE_PASSWORD'))
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        logging.exception('Got exception on {} handler'.format(__file__.split("/")[-1]))
    """finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")"""
