from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
       # USER = 'aacuser'
        #PASS = 'SNHUgrad2024!'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32413
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
            self.database = self.client['%s' % (DB)]
            self.collection = self.database['%s' % (COL)]
            print("Connection Successful")
        except PyMongoError as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")

# Complete this create method to implement the C in CRUD
    def create(self, data):
        """
        Inserts a document into the specified MongoDB database and collection.

        :param data: A dictionary representing the document to be inserted.
        :return: True if successful insert, False otherwise.
        """
        if data:
            try:
                result = self.collection.insert_one(data)
                return result.acknowledged
            except PyMongoError as e:
                raise Exception(f"Failed to insert document: {e}")
        else:
            raise ValueError("Nothing to save, because data parameter is empty")

    def read(self, query):
        """
        Queries for documents from the specified MongoDB database and collection.

        :param query: A dictionary representing the key/value lookup pair for the query.
        :return: A list of documents matching the query if successful, an empty list otherwise.
        """
        try:
            result = self.collection.find(query)
            return list(result)
        except PyMongoError as e:
            raise Exception(f"Failed to query documents: {e}")

    def update(self, query, data):
        """
        Updates document(s) in the specified MongoDB database and collection.

        :param query: A dictionary representing the key/value lookup pair for the query.
        :param data: A dictionary representing the key/value pairs to update in the document(s).
        :return: The number of objects modified in the collection.
        """
        try:
            result = self.collection.update_many(query, {"$set": data})
            return result.modified_count
        except PyMongoError as e:
            raise Exception(f"Failed to update documents: {e}")

    def delete(self, data):
        """
        Removes document(s) from the specified MongoDB database and collection.

        :param data: A dictionary representing the key/value lookup pair for the query.
        :return: The number of objects removed from the collection.
        """
        try:
            documents = self.read(data)
            if documents:
                print("The following documents will be deleted:")
                for document in documents:
                    print(document)
                confirm = input("Are you sure you want to delete these documents? (y/n): ")
                if confirm.lower() == "y":
                    result = self.collection.delete_many(data)
                    return result.deleted_count
                else:
                    print("Deletion canceled.")
                    return 0
            else:
                print("No documents found matching the query.")
                return 0
        except PyMongoError as e:
            raise Exception(f"Failed to delete documents: {e}")