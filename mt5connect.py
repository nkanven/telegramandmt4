import MetaTrader5 as mt5
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish MetaTrader 5 connection to a specified trading account

#48133080 0N)JKN7s 48133064 Meanselme89
login=48133080
server="HFMarketsGlobal-Demo"
password="0N)JKN7s"

mt5.initialize()

authorized=mt5.login(login, password, server)
if authorized:
    # display trading account data 'as is'
    print(mt5.account_info())
    # display trading account data in the form of a list
    print("Show account_info()._asdict():")
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(login, mt5.last_error()))

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
