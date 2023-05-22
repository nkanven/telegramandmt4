from TelegramBot.utils import *


class Parse:
    def __init__(self, message: list, previous_ticket: str, m_date, time_zone, channel_title) -> None:
        self._message = message
        self._previous_ticket = previous_ticket
        self._m_date = m_date
        self._time_zone = time_zone
        self._channel_title = channel_title
        self._count_message_content = len(message)

        self.__func_dict = {
            0: self.open_order_message,
            9: self.close_order_message
        }

        self.__func = str(self.__func_dict[self._count_message_content]())
        eval(self.__func + "== 1")

    def open_order_message(self) -> str:
        res = "1"
        try:
            order_type = self._message[1]
            order_symbol = self._message[2]
            order_execution = self._message[3]
            order_entry_price = self._message[5]
            order_take_profit = self._message[10]
            order_stop_loss = self._message[14]
            order_ticket = self._message[-1]

            if self._previous_ticket == "0" or self._previous_ticket != str(self._message[-1]):
                print(f"Received trade signal from: {self._channel_title} \
                        (Received {self._m_date} {str(self._time_zone)} ")
                print(f"MT4 signal: /open {order_type} {order_symbol} {order_execution}\
                         {order_entry_price} {order_take_profit} {order_stop_loss} {order_ticket}")

                f = open("order.bin", "w")
                f.write(
                    order_type + " " + order_symbol + " " + order_execution + " " + order_entry_price +
                    " " + order_take_profit + " " + order_stop_loss)
                f.close()

                f = open("orderticket.txt", "w")
                f.write(str(self._message[-1]))
        except Exception:
            res = "0"

        return res

    def close_order_message(self) -> str:
        order_symbol = self._message[1]
        order_type = self._message[3]
        order_ticket = self._message[-1]

        if self._previous_ticket == "0" or self._previous_ticket != str(self._message[-1]):
            print(f"Received trade signal from: {self._channel_title} \
            (Received {self._m_date} {str(self._time_zone)} ")
            print(f"MT4 signal: /close {order_symbol} with ticket number {order_ticket}")

            f = open("order.bin", "w")
            f.write(
                order_type + " " + order_symbol + " " + order_ticket + " ")
            f.close()

            f = open("orderticket.txt", "w")
            f.write(str(self._message[-1]))
        return "1"
