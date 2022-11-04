#pip install auto-py-to-exe

import logging
from datetime import datetime
import socket

import os
import sys
import time
import json

import traceback

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import telethon.sync

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
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
        self.api_id = 1290118
        self.api_hash = "204a57ac250f69a3d108ea6bb3857810"

        self.api_hash = str(self.api_hash)

        self.orderTicketFilePath = "orderticket.txt"

        self.phone = ""
        self.offset = 0
        self.limit = 100
        self.all_participants = []
        self.offset_id = 0
        self.all_messages = []
        self.total_messages = 0
        self.total_count_limit = 0

        # Create the client and connect
        self.client = TelegramClient("me", self.api_id, self.api_hash)
        self.client.start()
        self.my_channel = ""

        self.orderTicketFilePath = "orderticket.txt"

        logging.basicConfig(filename="error.log", format="%(asctime)s %(clientip)-15s %(user)-8s %(message)s")

        #Delete stored order ticket. 
        if os.path.isfile(self.orderTicketFilePath):
            os.remove(self.orderTicketFilePath)
        pass

    """
    OnStartChecks handles the basic checks for the program successfull launch. Store 0 as order ticket
    if file does not exist. Get the last order ticket and store it.
    """
    def OnStartChecks(self):
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
                orderTicket = latest_message[-1]
                f.write(str(orderTicket))

    def main(self):

        try:
            # Setting configuration values
            print("TelegramToMetatrader (version 1.0) Copyright @nkanven " + str(datetime.now().strftime("%Y")))
            
            # Ensure you're authorized
            if not self.client.is_user_authorized():
                self.client.send_code_request(self.phone)
                try:
                    self.client.sign_in(self.phone, input('Enter the code: '))
                except SessionPasswordNeededError:
                    self.client.sign_in(password=input('Password: '))

            print("Telegram link Created with account number: +" + str(self.client.get_me().phone))
            print("Connected to Telegram.")
            print("Telegram signal reader, waiting for message...")


            user_input_channel = "https://t.me/+DO2w2iQvujljNTA0" #input("enter entity(telegram URL or entity id):")

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

            self.OnStartChecks()

            while True:
                #print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)

                #Get channel history
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

                #Check for messages
                if not history.messages:
                    continue

                messages = history.messages

                #Message doesn't exist
                if not messages[0].message:
                    continue

                f = open(self.orderTicketFilePath, "r")
                previousOrderTicket = f.read()

                #Get message time difference to store the most recent trade signal
                """dt_obj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nowtimestamp = time.mktime(time.strptime(dt_obj, '%Y-%m-%d %H:%M:%S'))
                messageDate = messages[0].date.strftime("%Y-%m-%d %H:%M:%S")
                timestamp = time.mktime(time.strptime(messageDate, '%Y-%m-%d %H:%M:%S'))
                latest_message_timediff = nowtimestamp - timestamp

                print(latest_message_timediff)
                print(nowtimestamp, timestamp)
                print(dt_obj, messageDate)
                print(messages[0].date.tzinfo)"""

                messageDate = messages[0].date.strftime("%Y-%m-%d %H:%M:%S")
                timeZinfo = messages[0].date.tzinfo

                #There is a new message if total stored messages count is different from total messages
                if self.total_messages != len(messages):
                    latest_message = messages[0].message.split(" ")

                    #Try to catch IndexError to verify if history.messages has sent messages
                    try:
                        orderType = latest_message[1]
                        orderSymbol = latest_message[2]
                        orderExecution = latest_message[3]
                        orderEntryPrice = latest_message[5]
                        orderTakeProfit = latest_message[10]
                        orderStopLoss = latest_message[14]
                        orderTicket = latest_message[-1]

                        if previousOrderTicket == "0" or previousOrderTicket != str(latest_message[-1]):
                            print("Received trade signal from: " + self.my_channel.title + " (Received " + messageDate + " " + str(timeZinfo) + ")")
                            print("MT4 signal: /open " + orderType + " " + orderSymbol + " " + orderExecution + " " + orderEntryPrice + " " + orderTakeProfit + " " + orderStopLoss + " " + orderTicket)
                            
                            f = open("order.bin", "w")
                            f.write(orderType + " " + orderSymbol + " " + orderExecution + " " + orderEntryPrice + " " + orderTakeProfit + " " + orderStopLoss)
                            f.close()

                            f = open("orderticket.txt", "w")
                            f.write(str(latest_message[-1]))

                        self.total_messages = len(messages)
                    except IndexError:
                        pass


                #print("Listening Telegram channel...")
        except Exception as e:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            d = {'clientip': ip_address, hostname: 'telegramreader'}
            logging.exception('Got exception on main handler', extra=d)
            raise