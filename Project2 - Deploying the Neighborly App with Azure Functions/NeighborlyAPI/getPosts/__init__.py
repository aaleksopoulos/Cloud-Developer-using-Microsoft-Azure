import logging
import azure.functions as func
import pymongo
import json
from bson.json_util import dumps
from key import primary_db_key, database_name



def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python getPosts trigger function processed a request.')
    print(primary_db_key)
    try:
        url = primary_db_key  # TODO: Update with appropriate MongoDB connection information
        client = pymongo.MongoClient(url)
        database = client[database_name]
        collection = database['posts']

        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8', status_code=200)
    except:
        return func.HttpResponse("Bad request.", status_code=400)