# GET
# Reading records from ServiceNow and saving them into local mongo database

from pymongo import MongoClient
import pymongo


client = MongoClient('localhost', 27017)
db = client['recipes_db']
recipes = db['recipes']

#GET request w/ database table fields specified

#Need to install requests package for python
#easy_install requests

import requests, json

# Set the request parameters
'''
Use sysparm_fields=field_name => field_name is the field you want to read
separate fields using commas in case you want to read more than one field from a table
'''

url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe?sysparm_limit=1'

#Use IST440 for both user and pwd
user = 'kasper440'
pwd = 'kasper440'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
# GET is the request to read data
response = requests.get(url, auth=(user, pwd), headers=headers )


# Decode the JSON response into a dictionary and use the data
data = response.json()
print(type(data))
print()
print("This is a json dictionary: ", data, "Type: ", type(data))


# Now we need to get the list of key value pairs from our dict
print()
recipe_names_pairs = data['result']
print("This is a list: ", recipe_names_pairs)
print()

# Check type
print("Recipe_names_pairs is of the list type and can now be used to create documents in mongddb: " , type(recipe_names_pairs))
print()
#db.collection_recipe.insert(recipe_names_pairs)


# For loop to iterate through the key value pairs obtained from the json response
# and check if any has previously been inserted in the collection

for doc in recipe_names_pairs:
    try:
        # insert into db collection
        # print("Inserting ",  doc, " into db...")
        message = "Inserting  into db..."
        db.recipes.insert_one(doc)
    except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in the local db collection
        continue