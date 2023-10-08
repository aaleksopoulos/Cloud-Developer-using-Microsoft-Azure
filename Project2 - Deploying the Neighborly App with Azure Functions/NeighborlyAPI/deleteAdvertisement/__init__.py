import azure.functions as func
import pymongo
from bson.objectid import ObjectId
from key import primary_db_key, database_name


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get('id')

    if id:
        try:
            url = primary_db_key  # TODO: Update with appropriate MongoDB connection information
            client = pymongo.MongoClient(url)
            database = client[database_name]
            collection = database['advertisements']
            
            query = {'_id': ObjectId(id)}
            result = collection.delete_one(query)
            return func.HttpResponse("")

        except:
            print("could not connect to mongodb")
            return func.HttpResponse("could not connect to mongodb", status_code=500)

    else:
        return func.HttpResponse("Please pass an id in the query string",
                                 status_code=400)
