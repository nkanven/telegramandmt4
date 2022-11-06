import mysql.connector
from mysql.connector import Error
import logging
from connect import dbconnect

# Enable logging
logging.basicConfig(
    filename="error.log", 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class insert_data:

    def __init__(self) -> None:
        pass

    def insertion(self):
        mySql_insert_query = """INSERT INTO products (name, price, d_date) 
                           VALUES (%s, %s, %s, %s) """

        records_to_insert = [('Signaux-30', 40, '2019-01-11'),
                            ('Signaux-365', 365, '2019-02-27'),
                            ('Signaux à vie', 2330, '2019-07-23')]


        connection = dbconnect().connect()
        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()