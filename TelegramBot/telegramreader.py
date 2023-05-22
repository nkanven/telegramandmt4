# pip install auto-py-to-exe

import logging
from datetime import datetime
import socket
import os

from TelegramBot.utils.message_parser import Parse

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import telethon.sync

from telethon.tl.types import (
    PeerChannel
)

from telethon.tl.functions.messages import (GetHistoryRequest)


class Reader:
    """
    Telegram reader class to do fetch new trade order and store it on user devise.

    This class have one principal function

    Main() handle te connection with Telegram server and logged user.
    """

    def __init__(self) -> None:
        self.api_id = int(os.getenv('TELEGRAMCLIENT_API_ID'))
        self.api_hash = os.getenv('TELEGRAMCLIENT_API_HASH')

        self.api_hash = str(self.api_hash)

        self.orderTicketFilePath = "orderticket.txt"

        self.phone = ""
        self.offset = 0
        self.limit = int(os.getenv('HISTORY_LIMIT'))
        self.all_participants = []
        self.offset_id = 0
        self.all_messages = []
        self.total_messages = 0
        self.total_count_limit = 0

        print("TelegramToMetatrader (version " + os.getenv('VERSION') + ") Copyright @" + os.getenv(
            'AUTHOR_USERNAME') + " " + str(datetime.now().strftime("%Y")))

        # Create the client and connect
        self.client = TelegramClient("me", self.api_id, self.api_hash)

        while True:
            try:
                self.client.start()
                break
            except ConnectionError:
                print("Cannot send requests while disconnected. Please check your Internet connexion")

        self.my_channel = ""

        self.orderTicketFilePath = "orderticket.txt"

        logging.basicConfig(filename="../error.log", format="%(asctime)s %(clientip)-15s %(user)-8s %(message)s")

        # Delete stored order ticket.
        if os.path.isfile(self.orderTicketFilePath):
            os.remove(self.orderTicketFilePath)
        pass

    """
    OnStartChecks handles the basic checks for the program successfull launch. Store 0 as order ticket
    if file does not exist. Get the last order ticket and store it.
    """

    def onstartchecks(self):
        history = self.client(GetHistoryRequest(
            peer=self.my_channel,
            offset_id=self.offset_id,
            offset_date=None,
            add_offset=0,
            limit=self.limit,
            max_id=0,
            min_id=0,
            hash=0
        ))

        if not os.path.isfile(self.orderTicketFilePath):
            f = open(self.orderTicketFilePath, "w")
            if not history.messages:
                f.write("0")
            else:
                messages = history.messages
                latest_message = messages[0].message.split(" ")
                order_ticket = latest_message[-1]
                f.write(str(order_ticket))

    def main(self):

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        d = {'clientip': ip_address, hostname: 'telegramreader'}

        try:
            # Setting configuration values

            # Ensure you're authorized
            if not self.client.is_user_authorized():
                self.client.send_code_request(self.phone)
                try:
                    self.client.sign_in(self.phone, input('Enter the code: '))
                except SessionPasswordNeededError:
                    self.client.sign_in(password=input('Password: '))

            print("Telegram link Created with account number: +" + str(self.client.get_me().phone))
            print("Connected to Telegram.")
            print("Telegram signal reader, waiting for trading signal...")

            user_input_channel = os.getenv('TELEGRAM_USER_URL')  # input("enter entity(telegram URL or entity id):")

            if user_input_channel.isdigit():
                entity = PeerChannel(int(user_input_channel))
            else:
                entity = user_input_channel

            self.my_channel = self.client.get_entity(entity)

            """while True:
                participants = client(GetParticipantsRequest(
                    my_channel, ChannelParticipantsSearch(''), offset, limit,
                    hash=0
                ))
                if not participants.users:
                    break
                all_participants.extend(participants.users)
                offset += len(participants.users)

            all_user_details = []
            for participant in all_participants:
                all_user_details.append(
                    {"id": participant.id, "first_name": participant.first_name, "last_name": participant.last_name,
                    "user": participant.username, "phone": participant.phone, "is_bot": participant.bot})

            with open('user_data.json', 'w') as outfile:
                json.dump(all_user_details, outfile)"""

            self.onstartchecks()

            while True:
                # print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)

                # Get channel history
                history = self.client(GetHistoryRequest(
                    peer=self.my_channel,
                    offset_id=self.offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=self.limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))

                # Check for messages
                if not history.messages:
                    continue

                messages = history.messages

                # Message doesn't exist
                if not messages[0].message:
                    continue

                f = open(self.orderTicketFilePath, "r")
                previous_order_ticket = f.read()

                # Get message time difference to store the most recent trade signal
                """dt_obj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nowtimestamp = time.mktime(time.strptime(dt_obj, '%Y-%m-%d %H:%M:%S'))
                message_date = messages[0].date.strftime("%Y-%m-%d %H:%M:%S")
                timestamp = time.mktime(time.strptime(message_date, '%Y-%m-%d %H:%M:%S'))
                latest_message_timediff = nowtimestamp - timestamp

                print(latest_message_timediff)
                print(nowtimestamp, timestamp)
                print(dt_obj, message_date)
                print(messages[0].date.tzinfo)"""

                message_date = messages[0].date.strftime("%Y-%m-%d %H:%M:%S")

                time_zinfo = messages[0].date.tzinfo

                # There is a new message if total stored messages count is different from total messages

                if self.total_messages != len(messages):
                    latest_message = messages[0].message.split(" ")

                    print(len(latest_message))

                    # Try to catch IndexError to verify if history.messages has sent messages
                    try:
                        Parse(latest_message, previous_order_ticket, message_date, time_zinfo, self.my_channel.title)

                        self.total_messages = len(messages)
                    except IndexError as e:
                        print(e)

                # print("Listening Telegram channel...")

        except ConnectionError as e:
            print(e)
            logging.exception('Got OSError on main handler', extra=d)
        except Exception:
            logging.exception('Got exception on main handler', extra=d)
