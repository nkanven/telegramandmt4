#pip install auto-py-to-exe

def OnStartChecks():
    orderTicketFilePath = "orderticket.txt"
    history = client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))

    if not os.path.isfile(orderTicketFilePath):
        f = open(orderTicketFilePath, "w")
        if not history.messages:
            f.write("0")
        else:
            messages = history.messages
            latest_message = messages[0].message.split(" ")
            orderTicket = latest_message[-1]
            f.write(str(orderTicket))


try:
    import os
    import sys
    import time
    import json
    from datetime import datetime
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

    # Setting configuration values
    print("TelegramToMetatrader (version 1.0) Copyright @nkanven " + str(datetime.now().strftime("%Y")))
    
    api_id = 1290118
    api_hash = "204a57ac250f69a3d108ea6bb3857810"

    api_hash = str(api_hash)

    orderTicketFilePath = "orderticket.txt"

    phone = ""

    # Create the client and connect
    client = TelegramClient("me", api_id, api_hash)
    client.start()
    
    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    print("Telegram link Created with account number: +" + str(client.get_me().phone))
    print("Connected to Telegram.")
    print("Telegram signal reader, waiting for message...")


    user_input_channel = "https://t.me/+DO2w2iQvujljNTA0" #input("enter entity(telegram URL or entity id):")

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = client.get_entity(entity)

    offset = 0
    limit = 100
    all_participants = []

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


    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    OnStartChecks()

    while True:
        #print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            continue

        messages = history.messages
        f = open(orderTicketFilePath, "r")
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

        if total_messages != len(messages):
            latest_message = messages[0].message.split(" ")
            orderType = latest_message[1]
            orderSymbol = latest_message[2]
            orderExecution = latest_message[3]
            orderEntryPrice = latest_message[5]
            orderTakeProfit = latest_message[10]
            orderStopLoss = latest_message[14]
            orderTicket = latest_message[-1]

            if previousOrderTicket == "0" or previousOrderTicket != str(latest_message[-1]):
                print("Received trade signal from: " + my_channel.title + " (Received " + messageDate + " " + str(timeZinfo) + ")")
                print("MT4 signal: /open " + orderType + " " + orderSymbol + " " + orderExecution + " " + orderEntryPrice + " " + orderTakeProfit + " " + orderStopLoss + " " + orderTicket)
                f = open("order.bin", "w")
                f.write(orderType + " " + orderSymbol + " " + orderExecution + " " + orderEntryPrice + " " + orderTakeProfit + " " + orderStopLoss)
                f.close()

                f = open("orderticket.txt", "w")
                f.write(str(latest_message[-1]))

            total_messages = len(messages)


        #print("Listening Telegram channel...")
except Exception as e:
    f = open("error.log", "w")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(traceback.extract_tb(exc_tb))
    f.write(str(traceback.extract_tb(exc_tb)))