# Put the use case you chose here. Then justify your database choice:
#
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

client = MongoClient()
database = client.bikeshare

racks = database.racks
users = database.users
bikes = database.bikes

active = users.find(
   {
      "pass.expire": {"$gte": datetime.datetime.utcnow()}
   },
   { "name.first": 1, "pass.expire": 1, "_id": 0 }
)

for doc in active:
    print('{} pass exp: {}'.format(doc['name']['first'], doc['pass']['expire']))

query = {"location": SON([("$near", [ 40.804761, -73.966283 ]), ("$maxDistance", 0.01)])}

closeracks = racks.find(query, {"name":1, "_id": 0})

print(list(closeracks))

rentalsout = bikes.find( { "status.status": "rented" }, { "id": 1, "location.rack": 1 } )

print(list(rentalsout))

# Action 1: <describe the action here>


# Action 2: <describe the action here>


# Action 3: <describe the action here>


# Action 4: <describe the action here>


# Action 5: <describe the action here>


# Action 6: <describe the action here>


# Action 7: <describe the action here>


# Action 8: <describe the action here>
