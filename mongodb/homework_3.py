import pymongo
from pymongo import MongoClient

client = MongoClient()
database = client.test

collection = database.movies
collection.update_many({"genres": "Short", "rated": "NOT RATED"}, {"$set": {"rated": "Pending rating"}})

collection.insert({"title": "Cargo", "year": 2013, "countries": ["Australia"],
                "genres": ["Short", "Drama", "Fantasy","Horror"],
                "directors":["Ben Howling", "Yolanda Ramke"],
                "imdb": {"id":  2842128, "rating": 7.8, "votes": 1781}})
pipe = [{"$unwind": "$genres"}, {"$match": {"genres": "Short"}}, {"$group": {"_id": "$genres", "count": {"$sum": 1}}}]
total = collection.aggregate(pipe)
print(list(total))

birthplace_pipe = [{"$unwind": "$genres"}, {"$unwind": "$countries"}, {"$match": {"genres": "Short", "countries": "USA", "rated": "Pending rating"}},
                    {"$group": {"_id": {"Country": "$countries", "rating": "$rated"}, "count": {"$sum": 1}}}]
total2 = collection.aggregate(birthplace_pipe)
print(list(total2))

database.orders.insert([
   { "item" : "almonds", "price" : 12, "quantity" : 2 },
   { "item" : "pecans", "price" : 20, "quantity" : 1 }
])

database.items.insert([
  { "item" : "almonds", "description": "almond clusters", "instock" : 120 },
  { "item" : "bread", "description": "raisin and nut bread", "instock" : 80 },
  { "item" : "pecans", "description": "candied pecans", "instock" : 60 }
])

lookup = database.orders.aggregate([
   {
      "$lookup": {
         "from": "items",
         "localField": "item",
         "foreignField": "item",
         "as": "fromItems"
      }
   }])

print(list(lookup))
