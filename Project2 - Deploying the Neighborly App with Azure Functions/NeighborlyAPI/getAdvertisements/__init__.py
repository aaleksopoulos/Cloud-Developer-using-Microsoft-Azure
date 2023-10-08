import azure.functions as func
import pymongo
import json
from bson.json_util import dumps
from key import primary_db_key, database_name

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        url = primary_db_key  # TODO: Update with appropriate MongoDB connection information
        client = pymongo.MongoClient(url)
        database = client[database_name]
        collection = database['advertisements']


        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
    except:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb",
                                 status_code=400)

