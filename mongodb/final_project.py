# Put the use case you chose here. Then justify your database choice:
# I chose the bikesharing application. I chose mongodb for its geospatial indexing.
#
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
#
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
#
#

import pymongo
from pymongo import MongoClient, GEO2D
from bson.son import SON
from pytz import timezone
import datetime
east = timezone('US/Eastern')
monthly_pass_purchase_date = east.localize(datetime.datetime(2018, 4, 30, 6, 0, 0))
monthly_pass_expire_date = east.localize(datetime.datetime(2018, 5, 30, 6, 0, 0))
card_expire_date = east.localize(datetime.datetime(2020, 9, 10, 0, 0, 0))

daily_pass_purchase_date = east.localize(datetime.datetime(2018, 5, 3, 4, 8, 0))
daily_pass_expire_date = east.localize(datetime.datetime(2018, 5, 4, 4, 8, 0))

x_purchase_date = east.localize(datetime.datetime(2018, 3, 30, 6, 0, 0))
x_expire_date = east.localize(datetime.datetime(2018, 4, 1, 6, 0, 0))

return_deadline = east.localize(datetime.datetime(2018, 5, 4, 1, 8, 0))

client = MongoClient()
database = client.bikeshare

racks = database.racks
users = database.users
bikes = database.bikes

racks.create_index( [ ( "location", GEO2D ) ] )

users.insert_many([
    {
      "name": { "first": "Lalka", "last": "Rieger" },
      "pass": { "type": "month", "purchase": monthly_pass_purchase_date, "expire": monthly_pass_expire_date },
      "billing": { "primary": 444444444444, "accounts": [ { "cardnumber": 444444444444, "expire": card_expire_date, "name": "LALKA E" } ] },
      "history": [ { "account": 444444444444, "purchase": "monthly pass", "date": monthly_pass_purchase_date, "amount": 200.00 } ],
      "id": 1
    },
    {
      "name": { "first": "John", "last": "Dean" },
      "pass": { "type": "day", "purchase": daily_pass_purchase_date, "expire": daily_pass_expire_date },
      "billing": { "primary": 555555555555, "accounts":[ { "cardnumber": 555555555555, "expire": card_expire_date, "name": "JOHN DEAN" } ] },
      "history": [ { "account": 555555555555, "purchase": "daily pass", "date": daily_pass_purchase_date, "amount": 30.00 },
                  { "account": 555555555555, "purchase": "overdue return", "date": daily_pass_expire_date, "amount": 4.00 } ],
      "id": 2
    },
    {
      "name": { "first": "Sakura", "last": "Kagei" },
      "pass": { "type": "day", "purchase": x_purchase_date, "expire": x_expire_date },
      "billing": { "primary": 666666666666, "accounts":[{"cardnumber": 666666666666, "expire": card_expire_date, "name": "S KAGEI" } ] },
      "history": [ { "account": 666666666666, "purchase": "daily pass", "date": x_purchase_date, "amount": 30.00 } ],
      "id": 3
    }
    ])

racks.insert_many([
    {
        "id": 1,
        "name" : "Broadway@110",
        "location" :  [ 40.804305, -73.967019 ],
        "capacity" : 4,
        "slots": [ { "id" : 1, "bike": 7 }, { "id" : 2 }, { "id" : 3, "bike": 2 }, { "id" : 4 } ]
    },
    {
        "id": 2,
        "name" : "Broadway@116",
        "location" : [ 40.808269, -73.964549 ],
        "capacity" : 4,
        "slots": [ { "id" : 1, "bike": 5 }, { "id" : 2, "bike": 1}, { "id" : 3, "bike": 5 }, { "id" : 4 } ]
    },
    {
        "id": 3,
        "name" : "MalcolmXBlvd@110",
        "location" : [ 40.798513, -73.952187 ],
        "capacity" :6,
        "slots": [ { "id" : 1 }, { "id" : 2 }, { "id" : 3, "bike": 3 }, { "id" : 4 }, { "id" : 5, "bike": 4 }, { "id" : 6 } ]
    },
    {
        "id": 4,
        "name" : "lakeSt@UpperSaddleRiver",
        "location" : [ 41.059134, -74.096485 ],
        "capacity" :3,
        "slots": [ { "id" : 1 }, { "id" : 2, "bike": 8 }, { "id" : 3, "bike": 3 } ]
    },
    {
        "id": 5,
        "name" : "BridgeSt@BatteryPark",
        "location" : [ 40.703604, -74.014404 ],
        "capacity" : 2,
        "slots": [ { "id" : 1 }, { "id" : 2 } ]
    }
])

bikes.insert_many([
    {
        "id": 1,
        "status" : { "status": "racked", "location": { "rack": 2, "slot": 2 } }
    },
    {
        "id": 2,
        "status" : { "status": "racked", "location": { "rack": 1, "slot": 3 } }
    },
    {
        "id": 3,
        "status" : { "status": "racked", "location": { "rack": 3, "slot": 3 } }
    },
    {
        "id": 4,
        "status" : { "status": "racked", "location": { "rack": 3, "slot": 5 } }
    },
    {
        "id": 5,
        "status" : { "status": "racked", "location": { "rack": 2, "slot": 1 } }
    },
    {
        "id": 6,
        "status" : { "status": "rented", "location": 2, "expire": return_deadline }
    },
    {
        "id": 7,
        "status" : { "status": "racked", "location": { "rack": 1, "slot": 1 } }
    },
    {
        "id": 8,
        "status" : { "status": "racked", "location": { "rack": 4, "slot": 2 } }
    },
    {
        "id": 9,
        "status" : { "status": "repair" }
    },
    {
        "id": 10,
        "status" : { "status": "rented", "location": 3, "return_dealine": x_expire_date }
    }
])

# Action 1: <describe the action here>


# Action 2: <describe the action here>


# Action 3: <describe the action here>


# Action 4: <describe the action here>


# Action 5: <describe the action here>


# Action 6: <describe the action here>


# Action 7: <describe the action here>


# Action 8: <describe the action here>
