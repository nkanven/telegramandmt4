import mysql.connector
from mysql.connector import Error
import logging
from connect import dbconnect
from datetime import datetime

# Enable logging
logging.basicConfig(
    filename="error.log", 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class insert_data:

    def __init__(self, dbconnect) -> None:
        self.dbconnect = dbconnect
        pass

    def insertion(self):
        mySql_insert_query = """INSERT INTO products (name, description, price, d_date) 
                           VALUES (%s, %s, %s, %s) """

        d_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records_to_insert = [('Signaux-30', "Abonnement aux signaux de trading eInvestors pour 30 jours", 40, d_date),
                            ('Signaux-365', "Abonnement aux signaux de trading eInvestors pour un an", 365, d_date),
                            ('Signaux-life', "Abonnement à vie aux signaux de trading eInvestors", 36500, d_date)]

        connection = self.dbconnect.connect()
        cursor = self.dbconnect.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        self.dbconnect.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()