# Put the use case you chose here. Then justify your database choice:
#   I chose the bikesharing application. I chose mongodb for its geospatial indexing.
#
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
#   Assuming I have a cluster, if the server is a primary, the cluster will elect a new primary from the
#   secondaries to take over. If the server is a secondary, any available server can take over for it.
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
#   You can't lose the last known location of bikes, and you can't lose information about payments.
#   To reduce the risk of lost data you can specify the write concern for a write to the database. 'w' field
#   specifies how many instances the write should go to, and 'j' indicates a request for acknowledgement that
#   the write operation has been written to the journal.

# Imports
import pymongo
from pymongo import MongoClient, GEO2D, ReturnDocument
from bson.son import SON
from pytz import timezone
from datetime import datetime, timedelta

# get some preset times
east = timezone('US/Eastern')
monthly_pass_purchase_date = datetime(2018, 4, 30, 6, 0, 0)
monthly_pass_expire_date = datetime(2018, 5, 30, 6, 0, 0)
card_expire_date = datetime(2020, 9, 10, 0, 0, 0)

daily_pass_purchase_date = datetime(2018, 5, 3, 4, 8, 0)
daily_pass_expire_date = datetime(2018, 5, 4, 4, 8, 0)

x_purchase_date = datetime(2018, 3, 30, 6, 0, 0)
x_expire_date = datetime(2018, 4, 1, 6, 0, 0)

return_deadline = datetime(2018, 5, 4, 1, 8, 0)

# to keep track of unique ids. I want to use simple integers for readability.
next_userid = 1
next_rackid = 1
next_bikeid = 1

# Set up database and connection
client = MongoClient()
database = client.bikeshare

racks = database.racks
users = database.users
bikes = database.bikes

racks.create_index( [ ( "location", GEO2D ) ] )

# insert users
result = users.insert_many([
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
      "billing": { "primary": 666666666666, "accounts":[ { "cardnumber": 666666666666, "expire": card_expire_date, "name": "S KAGEI" } ] },
      "history": [ { "account": 666666666666, "purchase": "daily pass", "date": x_purchase_date, "amount": 30.00 } ],
      "id": 3
    }
])

# check users are inserted. Can do more complex handling of ids if we want to use confirmations/write conern.
if(len(result.inserted_ids) != 3) :
    print("Failed to insert users.")
    next_userid += len(result.inserted_ids)
else :
    print("Inserted 3 users.")
    next_userid += 3

# insert racks
result = racks.insert_many([
    {
        "id": 1,
        "name" : "Broadway@110",
        "location" :  [ 40.804305, -73.967019 ],
        "capacity" : 4,
        "slots": [ { "id" : 1, "bike": 7 }, { "id" : 2, "bike": None }, { "id" : 3, "bike": 2 }, { "id" : 4, "bike": None } ]
    },
    {
        "id": 2,
        "name" : "Broadway@116",
        "location" : [ 40.808269, -73.964549 ],
        "capacity" : 4,
        "slots": [ { "id" : 1, "bike": 5 }, { "id" : 2, "bike": 1}, { "id" : 3, "bike": 5 }, { "id" : 4, "bike": None } ]
    },
    {
        "id": 3,
        "name" : "MalcolmXBlvd@110",
        "location" : [ 40.798513, -73.952187 ],
        "capacity" :6,
        "slots": [ { "id" : 1, "bike": None }, { "id" : 2, "bike": None }, { "id" : 3, "bike": 3 },
                    { "id" : 4, "bike": None }, { "id" : 5, "bike": 4 }, { "id" : 6, "bike": None } ]
    },
    {
        "id": 4,
        "name" : "lakeSt@UpperSaddleRiver",
        "location" : [ 41.059134, -74.096485 ],
        "capacity" :3,
        "slots": [ { "id" : 1, "bike": None }, { "id" : 2, "bike": 8 }, { "id" : 3, "bike": 3 } ]
    },
    {
        "id": 5,
        "name" : "BridgeSt@BatteryPark",
        "location" : [ 40.703604, -74.014404 ],
        "capacity" : 2,
        "slots": [ { "id" : 1, "bike": None }, { "id" : 2, "bike": None } ]
    }
])

# check racks are inserted
if(len(result.inserted_ids) != 5) :
    print("Failed to insert racks.")
    next_rackid += len(result.inserted_ids)
else :
    print("Inserted 5 racks.")
    next_rackid += 5


# insert bikes
result = bikes.insert_many([
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

# check insert worked
if(len(result.inserted_ids) != 10) :
    print("Failed to insert bikes.")
    next_bikeid += len(result.inserted_ids)
else :
    print("Inserted 10 bikes.")
    next_bikeid += 10


# Action 1: User signs up
users.insert_one(
    {
      "name": { "first": "Jacob", "last": "Jacob" },
      "id": next_userid
    }
)

newusr = users.find_one(
   {
      "id": next_userid
   },
   { "name.first": 1, "name.last": 1, "id": 1, "_id": 0 }
)

print('Added user {} {}, id={}'.format(newusr['name']['first'], newusr['name']['last'], newusr['id']))
jacobid = newusr['id']
next_userid += 1

# Action 2: User enters payment information later
users.find_one_and_update(
    { "id": jacobid }, { '$set': { "billing.primary": 333333333333 },
                        '$push': { "billing.accounts" : { "cardnumber": 333333333333, "expire": card_expire_date, "name": "JACOB JACOB" } } }
)

newusr = users.find_one(
   {
      "id": jacobid
   },
   { "name.first": 1, "name.last": 1, "billing.primary": 1, "_id": 0 }
)

print('Added payment info to {} {}, cardnumber={}'.format(newusr['name']['first'], newusr['name']['last'], newusr['billing']['primary']))

# Action 3: User purchases a pass
# Leaving everything in UTC time for now. We can also store timezones and do the conversion if we want.
purchse_time = datetime.utcnow()
expire_time = datetime.utcnow()+ timedelta(hours=24)
users.find_one_and_update(
    { "id": jacobid }, { '$push': { "history" : { "account": newusr['billing']['primary'], "purchase": "day pass", "date": purchse_time, "amount": 30.00 } },
                        '$set': { "pass" : { "type": "day", "purchase": purchse_time, "expire": expire_time } } }
)

active = users.find_one(
   {
        "id" : jacobid,
      "pass.expire": {"$gte": datetime.utcnow()}
   },
   { "name.first": 1, "pass.expire": 1, "_id": 0 }
)
print('{}\'s pass expires {}'.format(active['name']['first'], active['pass']['expire']))

# Action 4: User looks up bike within 1 mile

closeracks = database.command(SON([('geoNear', 'racks'), ('near', [ 40.804761, -73.966283 ]), ('maxDistance', 0.01)]))
# get racks that are close, show which are empty and which have bikes
for doc in closeracks['results']:
    available_bikes = []
    for slot in doc['obj']['slots']:
        if(slot['bike']):
            available_bikes.append(slot['bike'])
    if(len(available_bikes) > 0):
        print('{} bikes avaiable {}'.format(len(available_bikes), doc['obj']['name']))
    else :
        print('{} empty'.format(doc['obj']['name']))

# Action 5: Takes out a bike
return_time = datetime.utcnow()+timedelta(hours=2)
removed = bikes.find_one_and_update(
   { "status.status" : "racked", "status.location.rack": 2 },
   { "$set": { "status": { "status": "rented", "location": jacobid, "expire": return_time } } }
)

remove = racks.find_one_and_update(
   { "id" : removed['status']['location']['rack'], "slots.id": removed['status']['location']['slot'] },
   { "$set": { 'slots.$.bike': None } }
)

print('bike {} rented from {} slot {}'.format(removed['id'], remove['name'], removed['status']['location']['slot']))

# Action 6: Checks time rental expires
rental = bikes.find_one(
    { "id": removed['id'] },
    { "status.expire": 1, "_id": 0 }
)

print('rental expires {}'.format(rental['status']['expire']))

# Action 7: looks up racks with an empty slot within 2 miles
closeracks = database.command(SON([('geoNear', 'racks'), ('near', [ 40.708004, -73.999089 ]), ('maxDistance', 0.02)]))
# get racks that are close, show which are full and which have open slots
for doc in closeracks['results']:
    available_slots = []
    for slot in doc['obj']['slots']:
        if( not slot['bike']):
            available_slots.append(slot['id'])
    if(len(available_slots) > 0):
        print('{} slots avaiable {}'.format(len(available_slots), doc['obj']['name']))
    else:
        print('{} full'.format(doc['obj']['name']))

# Action 8: returns bike
return_rack = racks.find_one_and_update(
   { "id" : 5, "slots.bike": None },
   { "$set": { 'slots.$.bike': removed['id'] } },
   return_document=ReturnDocument.AFTER
  )

return_slot = 1
for slot in return_rack['slots']:
    if slot['bike'] == removed['id']:
        return_slot = slot['id']

removed = bikes.find_one_and_update(
   { "status.status" : "rented", "status.location": jacobid },
   { "$set": { "status": { "status": "racked", "location": { "rack": return_rack['id'], "slot": return_slot}, "expire": None } } }
)

print('bike {} returned to {} slot {}'.format(removed['id'], return_rack['name'], return_slot))
