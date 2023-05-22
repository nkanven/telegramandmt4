from TelegramBot.models.db import connect
from tables import create_tables
from populate_tables import insert_data

class run:
    def __init__(self) -> None:
        #Create all necessary tables
        #Connect to database
        connexion = connect()

        ct = create_tables(connexion)
        ct.create_all_tables()

        #Populate the tables with default data
        pt = insert_data(connexion)
        pt.insertion()
        pass