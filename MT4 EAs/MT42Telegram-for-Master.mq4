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

/** Structure with information on orders */
struct OrderData
  {
   int               ticket;
   string            symbol;
   int               type;
   double            lots;
   datetime          open_time;
   double            open_price;
   double            stoploss;
   double            takeprofit;
   datetime          close_time;
   double            close_price;
   datetime          expiration;
   double            commission;
   double            swap;
   double            profit;
   string            comment;
   int               magic;
  };

/** @var OrderData postions[]  Array to hold ordre information. */
OrderData positions[] = {};

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   setPositions();
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
   Print("checkPositions() ", checkPositions());
   if(!checkPositions())
     {
      setPositions();
     }

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
   string url = "https://api.telegram.org/{TELEGRAM_BOT_ID}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text="+text;
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


/**
 * Check the status about open orders.
 *
 * @return bool  Returns false if order status changed, otherwise true.
 */
bool checkPositions(void)
  {
   int positionSize = ArraySize(positions);
   string message = "";
   
   
   if(positionSize != OrdersTotal())
     {
      //Order close event listener
      if(positionSize > OrdersTotal())
        {
         for(int i = OrdersTotal() - 1; i >= 0; i--)
           {
            if(!OrderSelect(i, SELECT_BY_POS))
               return(false);
            for(int j=0; j<positionSize; j++)
              {
               if(positions[j].ticket != OrderTicket())
                 {
                  Print("Order with ticket ", positions[j].ticket, " had been closed ");
                  //Send close order notification to Telegram
                  message = "🤖 " + positions[j].symbol + " Update: CLOSE order with ticket number " + (string)positions[j].ticket;
                  notifyTelegram(message);
                  break;
                 }
              }
           }
        }
      return(false);
     }

   for(int i = OrdersTotal() - 1; i >= 0; i--)
     {
      if(!OrderSelect(i, SELECT_BY_POS))
         return(false);

      if(positions[i].ticket     != OrderTicket())
        {
         return(false);
        }
      if(positions[i].symbol     != OrderSymbol())
         return(false);
      if(positions[i].type       != OrderType())
         return(false);
      if(positions[i].lots       != OrderLots())
         return(false);
      if(positions[i].open_time  != OrderOpenTime())
         return(false);
      if(positions[i].open_price != OrderOpenPrice())
         return(false);
      if(positions[i].stoploss   != OrderStopLoss())
        {
         Print("Stop loss modified from ", positions[i].stoploss, " to ", OrderStopLoss());
         return(false);
        }
      if(positions[i].takeprofit != OrderTakeProfit())
        {
         Print("Take profit modified from ", positions[i].takeprofit, " to ", OrderTakeProfit());
         return(false);
        }
      if(positions[i].expiration != OrderExpiration())
         return(false);
      if(positions[i].comment    != OrderComment())
         return(false);
      if(positions[i].magic      != OrderMagicNumber())
         return(false);
     }

   return(true);
  }

/** Register the order information to member variable postions. */
void setPositions(void)
  {
   int size = OrdersTotal();
   ArrayResize(positions, size);
   for(int i = size - 1; i >= 0; i--)
     {
      if(!OrderSelect(i, SELECT_BY_POS))
        {
         Print("ng");
         return;
        }
      positions[i].ticket     = OrderTicket();
      positions[i].symbol     = OrderSymbol();
      positions[i].type       = OrderType();
      positions[i].lots       = OrderLots();
      positions[i].open_time  = OrderOpenTime();
      positions[i].open_price = OrderOpenPrice();
      positions[i].stoploss   = OrderStopLoss();
      positions[i].takeprofit = OrderTakeProfit();
      positions[i].expiration = OrderExpiration();
      positions[i].comment    = OrderComment();
      positions[i].magic      = OrderMagicNumber();
     }
  }
//+------------------------------------------------------------------+
