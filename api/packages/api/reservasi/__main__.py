from dotenv import load_dotenv
import os
import pymongo
import requests

def input_reminder():
    pass
    
def main(args):
    nama = args.get('nama')
    phone_number = args.get('noHP')
    id_layanan = args.get('id_layanan')
    hari_reservasi = args.get('hariReservasi')
    waktu = args.get('waktuTersedia')

    if not nama:
        return {"body" : {"message" : "nama needed"}, "statusCode" : 401}
    
    if not phone_number:
        return {"body" : {"message" : "phone number needed"}, "statusCode" : 401}
    
    if not id_layanan:
        return {"body" : {"message" : "id_layanan needed"}, "statusCode" : 401}
    
    if not hari_reservasi:
        return {"body" : {"message" : "hari reservasi needed"}, "statusCode" : 401}
    
    if not waktu:
        return {"body" : {"message" : "waktu tersedia needed"}, "statusCode" : 401}
    
    try:
        id_layanan = int(id_layanan)
    except:
        return {"body" : {"message" : "invalid id_layanan"}, "statusCode" : 401}

    json_data = {
        "nama" : nama,
        "noHP" : phone_number,
        "id_layanan" : id_layanan,
        "hariReservasi" : hari_reservasi,
        "waktuTersedia" : waktu
    }
    
    try:
        load_dotenv()
        mongodb_uri = os.getenv("MONGODB_URI")
    except Exception as e:
        return {"body" : {"message" : f"error {e}"}, "statusCode" : 401}

    client = pymongo.MongoClient(mongodb_uri)
    db = client.mydb
    collection = db.reservasi_layanan

    try:
        collection.insert_one(json_data)
    except:
        return {"body" : {"message" : "error insert data"}, "statusCode" : 401}

    return {"body" : {"message" : "success"}, "statusCode" : 200}