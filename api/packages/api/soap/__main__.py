import pymongo
import os
from dotenv import load_dotenv


def main(args):
    data = args.get('data')
    id_layanan = args.get('id_layanan')

    if not id_layanan:
        return {"body": {"messages": "id_layanan needed"}, "statusCode": 401}
    
    if not data:
        return {"body": {"messages": "data not provided"}, "statusCode": 401}
    
    db = client.mydb
    try:
        id_layanan = int(id_layanan)
    except:
        return {"body": {"messages": "invalid id_layanan"}, "statusCode": 401}
    
    data["tglDatang"] = data["soapAnc"]["tanggal"]

    if id_layanan == 0:
        collection = db.soap_kb
    elif id_layanan == 1:
        collection = db.soap_kehamilan
    elif id_layanan == 2:
        collection = db.soap_imunisasi
    else:
        return {"body": {"messages": "under construction"}, "statusCode": 401}

    try:
        load_dotenv()
        client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
    except Exception as e:
        print(f"Error: {e}")
        return {"body": {"messages": str(e)}, "statusCode": 401}

    try:
        result = collection.insert_one(data)
        print(f"Inserted document ID: {result.inserted_id}")
        return {"body": {"messages": "success"}, "statusCode": 200}
    except Exception as e:
        print(f"Error: {e}")
        return {"body": {"messages": str(e)}, "statusCode": 401}
