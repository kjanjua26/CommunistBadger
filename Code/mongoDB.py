import pymongo
import glob
import csv

# Creates Client Connection and creates the Database
def createDatabase(clientURL, databaseName):
	client = pymongo.MongoClient(clientURL)
	database = client[databaseName]

	return client, database

# Collection is equivalent to Table in RDB
def createCollection(database, collectionName):
	collection = database[collectionName]

	return collection

# Insert Dictionaries into Collections
def dumpDictionary(collection, dictionary):
	collectionID = collection.insert_many(dictionary)

	return collectionID

# Dumps all csv Files into Database
def massDump(database):
	path = "../Data"
	for fname in glob.glob(path + '/News/' + '*.csv'):
		filename = fname[:-4]
		collectionName = filename.split('/')[3]
		collection = createCollection(database, collectionName)

		print ("File Name : ", filename)
		with open(fname , mode='r') as csvRead:
			reader = csv.DictReader(csvRead)
			dictionary = [rows for rows in reader]
		dumpDictionary(collection, dictionary)

	for fname in glob.glob(path + '/Stocks/' + '*.csv'):
		filename = fname[:-4]
		collectionName = filename.split('/')[3]
		collection = createCollection(database, collectionName)

		print ("File Name : ", filename)
		with open(fname , mode='r') as csvRead:
			reader = csv.DictReader(csvRead)
			dictionary = [rows for rows in reader]
		dumpDictionary(collection, dictionary)

	for fname in glob.glob(path + '/Tweets/' + '*.csv'):
		filename = fname[:-4]
		collectionName = filename.split('/')[3]
		collection = createCollection(database, collectionName)

		print ("File Name : ", filename)
		with open(fname , mode='r') as csvRead:
			reader = csv.DictReader(csvRead)
			dictionary = [rows for rows in reader]
		dumpDictionary(collection, dictionary)

# Gets the Stock Price of a Company on a certain Date
def printStockData_dateWise(collection, date):
	dateQuery = {"day" : date}
	rows = collection.find(dateQuery)

	for row in rows:
		print(row)

def sort_priceWise(collection):
	# Closing Stock Price (At the end of the Day)
	rows = collection.find().sort("close")
	for row in rows:
		print(row)

# Returns the Data in the Form of Dictionaries
def retrieveDictionaries(client, database, collectionName):
	print("First Checking the Status of the Database ...")
	databaseStatus(client, database, collectionName)

	rows = database[collectionName].find()
	list_of_dictionaries = list(rows)

	for dictionary in list_of_dictionaries:
		if "_id" in dictionary:
			del dictionary["_id"]

	return list_of_dictionaries

def massRetrieval(client, database):
	collections = listCollections(database)

	for collectionName in collections:
		data = retrieveDictionaries(client, database, collectionName)
		# KAMRAN CODE HERE		data - dictionaries of Stocks

# Drop Collection (Table)
def dropCollection(collection):
	collection.drop()

# Get Database Status (if it's working properly)
def databaseStatus(client, database, collectionName):
	dblist = client.list_database_names()
	if "CommunistBadger" in dblist:
		print("The database exists.")

	col_list = database.list_collection_names()
	if collectionName in col_list:
		print("The Collection exists.")

# View Names of the Collections in a Database
def listCollections(database):
	print(database.list_collection_names())

# View Names of all the Databases for a client
def listDatabases(client):
	print(client.list_database_names())

def main():
	clientURL = "mongodb://localhost:27017/"
	databaseName = "CommunistBadger"

	client, database = createDatabase(clientURL, databaseName)

	listDatabases(client)
	listCollections(database)

	massRetrieval(client, database)

def testCase():
	clientURL = "mongodb://localhost:27017/"
	databaseName = "CommunistBadger"
	collectionName = "Test"

	randomDictionary = [
		{"Name" : "Shahzaib", "Wut" : "Notang"},
		{"Name" : "Shafay", "Wut" : "notang?"},
		{"Name" : "Hasnain", "Wut" : "sometang"},
		{"Name" : "Kamran", "Wut" : "VariMuchSometang"}
	]

if __name__ == '__main__':
	main()