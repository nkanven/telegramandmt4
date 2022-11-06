import mysql.connector
from mysql.connector import Error
import logging

# Enable logging
logging.basicConfig(
    filename="error.log", 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class dbconnect:
    def __init__(self) -> None:
        pass

    def connect(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='eInvestors',
                                                user='root',
                                                password='@Meanselme89')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
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