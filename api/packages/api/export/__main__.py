import pymongo
import os
from dotenv import load_dotenv

def main(args):
    load_dotenv()
    try:
        client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
    except Exception as e:
        return {"body": {"messages": str(e)}, "statusCode": 401}

    db = client.mydb
    id_layanan = args.get('id_layanan')
    date_range = args.get('date')

    if id_layanan is None:
        return {"body": {"messages": "id_layanan needed"}, "statusCode": 401}
    
    if date_range is None:
        return {"body": {"messages": "date not provided"}, "statusCode": 401}

    try:
        id_layanan = int(id_layanan)
    except ValueError:
        return {"body": {"messages": "invalid id_layanan"}, "statusCode": 401}

    date_from = date_range.get('from')
    date_to = date_range.get('to')

    if not date_from or not date_to:
        return {"body": {"messages": "invalid date range"}, "statusCode": 401}

    query = {"tanggal_register": {"$gte": date_from, "$lte": date_to}}

    if id_layanan == 0:
        query["data_kb"] = {"$exists": True}
    elif id_layanan == 1:
        query["data_kehamilan"] = {"$exists": True}
    elif id_layanan == 2:
        query["data_imunisasi"] = {"$exists": True}
    else:
        return {"body": {"messages": "id_layanan not supported"}, "statusCode": 401}

    try:
        documents = list(db.pasien.find(query))
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return {"body": documents, "statusCode": 200}
    except Exception as e:
        return {"body": {"messages": str(e)}, "statusCode": 500}