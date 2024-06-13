from dotenv import load_dotenv
import os
import pymongo

def main(args):
    collection_name = args.get('collection')

    if not collection_name:
        return {"body": {"message": "collection name needed"}, "statusCode": 401}
    
    try:
        load_dotenv()
        mongodb_uri = os.getenv("MONGODB_URI")
    except Exception as e:
        return {"body": {"message": f"error {e}"}, "statusCode": 401}

    client = pymongo.MongoClient(mongodb_uri)
    db = client.mydb

    session = client.start_session()
    session.start_transaction()

    try:
        collection = db[collection_name]
        result = collection.delete_many({})
        
        session.commit_transaction()
        return {"body": {"message": "success", "deleted_count": result.deleted_count}, "statusCode": 200}
    except Exception as e:
        session.abort_transaction()
        return {"body": {"message": f"transaction failed: {e}"}, "statusCode": 401}
    finally:
        session.end_session()