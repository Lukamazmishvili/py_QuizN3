import requests
import json
import sqlite3

#Connecting to Website
r = requests.get('https://api.currencyscoop.com/v1/latest?api_key=aa54473fff3c0b7c79191f1a6342932d',
                 auth=('user', 'pass'))
#Response
connectionStatus = str(r.status_code)
if connectionStatus == '200':
    print(f"{connectionStatus} - Connection Status: Connected Successfully")
elif connectionStatus == "301" or '302' or '304':
    print(f"{connectionStatus} - Connection Status: Redirection")
elif connectionStatus == '401' or '403' or '404' or '405':
    print(f"{connectionStatus} - Connection Status: Client Error")
elif connectionStatus == '501' or '502' or '503' or '504':
    print(f"{connectionStatus} - Connection Status: Server Error")

#Getting additional info from server such as server name, content type etc.
header = r.headers['content-type']

#Recieved info written in json as one lined string
res = r.json()

#Getting specific info for user

currency = input("enter currency(example: USD): ")
print("You need " + str(res['response']['rates'][f'{currency}']) + f" {currency} to buy 1 $")

#Writing Recieved info in json style
jsn = json.dumps(res, indent=4)

#writing Recieved info in json file
with open("currency.json", "w") as file:
    json.dump(res, file, indent=4)

#Write Recieved info in SQL DataBase
conn = sqlite3.connect("CurrencyExchange.sqlite")
cursor = conn.cursor()

#Creating table in SQL DataBase

# cursor.execute(''' CREATE TABLE currency (
#              id INTEGER PRIMARY KEY AUTOINCREMENT,
#              currency STRING,
#              price FLOAT)''')

#Putting keys and values apart
dictKeys = (res['response']['rates']).keys()
dictValues = (res['response']['rates']).values()

#Putting again in list as tuples
currencyKeys = []
currencyValues = []
currencyLists = []
for i in dictKeys:
    currencyKeys.append(i)
for i in dictValues:
    currencyValues.append(i)
for i, j in zip(currencyKeys, currencyValues):
    s = (i, j)
    currencyLists.append(s)

#Inserting info in SQL DB Table

# cursor.executemany(f''' INSERT INTO currency (currency, price) VALUES (?, ?)''', currencyLists)

conn.commit()
conn.close()
