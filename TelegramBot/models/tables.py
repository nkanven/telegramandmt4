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

class create_tables:
    def __init__(self) -> None:
        pass

    def create_all_tables(self):
        try:
            connection = dbconnect().connect()
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                
                mySql_Create_Table_Query0 = """CREATE TABLE products ( 
                                    id int(11) NOT NULL,
                                    name varchar(250) NOT NULL,
                                    price float NOT NULL,
                                    d_date Datetime NOT NULL,
                                    PRIMARY KEY (Id)) """
                            
                mySql_Create_Table_Query1 = """CREATE TABLE payments ( 
                                    id int(11) NOT NULL,
                                    product_id int(11) NOT NULL,
                                    name varchar(250) NOT NULL,
                                    price float NOT NULL,
                                    meta_data text,
                                    payment_processor varchar(250) NOT NULL,
                                    purchase_date Datetime NOT NULL,
                                    PRIMARY KEY (Id),
                                    FOREIGN KEY (product_id) REFERENCES products(id)) """

                cursor = connection.cursor()
                result = cursor.execute(mySql_Create_Table_Query0)
                result = cursor.execute(mySql_Create_Table_Query1)
                print("Payments Table created successfully ")

        except Error as e:
            print("Error while connecting to MySQL", e)
            logging.exception('Got exception on {} handler'.format(__file__.split("/")[-1]))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")