//+------------------------------------------------------------------+
//|                                                 MT42TELEGRAM.mq4 |
//|                       Copyright 2022, Nkondog Anselme Venceslas. |
//|                              https://www.linkedin.com/in/nkondog |
//+------------------------------------------------------------------+
#property copyright "Copyright 2022, Nkondog Anselme Venceslas."
#property link      "https://www.linkedin.com/in/nkondog"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+

int totalTrades = 0;
string message = "";

int OnInit()
  {
//---

//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   if(totalTrades != OrdersTotal())
     {
      getMostRecentOrder();
      totalTrades = OrdersTotal();
     }

  }
//+------------------------------------------------------------------+


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void getMostRecentOrder()
  {

   int lastOrderIndex = OrdersTotal()-1, orderChrono = 0;
//Select an open trade
   Print("OrdersTotal() ", OrdersTotal());
   double openPrice =  OrderOpenPrice();
   double  takeProfit = OrderTakeProfit();
   double stopLoss = OrderStopLoss();
   datetime timeDiff;
   MqlDateTime str1;


   if(OrderSelect(lastOrderIndex, SELECT_BY_POS, MODE_TRADES) == true)
     {

      timeDiff = TimeCurrent() - OrderOpenTime();
      TimeToStruct(timeDiff, str1);

      orderChrono = str1.sec + str1.min;

      Print("Time diff ", str1.sec, " Min ", str1.min, " Order chrono ", orderChrono, " if ", (orderChrono < 4));

      if(orderChrono < 4)
        {
         if(OrderType() == OP_BUY)
           {
            message = "🤖 BUY " + OrderSymbol() +" NOW AT "+ OrderOpenPrice() +" 🤖 \t" +"📉TAKE PROFIT AT " + OrderTakeProfit() + "\t 🚫STOP LOSS AT " + OrderStopLoss() + " Order ticket " + OrderTicket();

           }
         if(OrderType() == OP_SELL)
           {
            message = "🤖 SELL " + OrderSymbol() +" NOW AT "+ OrderOpenPrice() +" 🤖 \t" +"📉TAKE PROFIT AT " + OrderTakeProfit() + "\t 🚫STOP LOSS AT " + OrderStopLoss() + " Order ticket " + OrderTicket();

           }
         notifyTelegram(message);
         Print("OrderOpenPrice ", openPrice, " OrderStopLoss ", OrderOpenPrice(), " OrderTakeProfit ",  OrderTakeProfit(), " OrderTicket ", OrderTicket(), " OrderType ", OrderType(), " OrderLots ", OrderLots(), " Order time ", OrderOpenTime());
           Sleep(3000);
         Print("Time difference ", timeDiff);
        }
     }
   else
     {
      Print("OrderSelect returned the error of ",GetLastError());
     }


  }

//🤖SELL USDCAD NOW AT 1.35818🤖
//📉TAKE PROFIT AT 1.35607
//🚫STOP LOSS AT 1.36196

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void notifyTelegram(string text)
  {


   SendNotification(text);

   string headers;
   string url = "https://api.telegram.org/bot1203586996:AAF3GTCy2yVyvXsCjd9pODhJncTUG7NcOKw/sendMessage?chat_id=-1001503862840&text="+text;
   char data[], result[];

   int res = WebRequest("GET", url, NULL, NULL, 3000, data, 0, result, headers);

   if(res == -1)
     {
      Print("Error in Webresquest. Error code = ", GetLastError());
      MessageBox("Add the address '" + url + "' to the list of allowed URLs on tab 'Expert Advisor'", "Error", MB_ICONINFORMATION);
     }
   else
     {
      if(res == 200)
        {
         Print("Message sent to Telegram: ", text);
        }
     }



  }
