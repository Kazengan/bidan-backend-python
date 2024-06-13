from dotenv import load_dotenv
import os
import pymongo
import requests
import datetime

def calculate_reminder_time(hari_reservasi):
    hari_reservasi_datetime = datetime.datetime.strptime(hari_reservasi, '%Y-%m-%d')
    try:
        timestamp = hari_reservasi_datetime.timestamp()
    except Exception as e:
        return e
    
    return timestamp

def sender(nomor, text):
    nomor = int(nomor)
    api_key = os.getenv("TEXTMEBOT_API_KEY")
    url = f"http://api.textmebot.com/send.php?recipient=+62{nomor}&apikey={api_key}&text={text}"
    print(url)
    try:
        requests.get(url)
        return "Success"
    except Exception as e:
        return e

def main(args):
    nama = args.get('nama')
    phone_number = args.get('noHP')
    id_layanan = args.get('id_layanan')
    hari_reservasi = args.get('hariReservasi')[:10]
    waktu = args.get('waktuTersedia')

    if not nama:
        return {"body": {"message": "nama needed"}, "statusCode": 401}
    
    if not phone_number:
        return {"body": {"message": "phone number needed"}, "statusCode": 401}
    
    if not id_layanan:
        return {"body": {"message": "id_layanan needed"}, "statusCode": 401}
    
    if not hari_reservasi:
        return {"body": {"message": "hari reservasi needed"}, "statusCode": 401}
    
    if not waktu:
        return {"body": {"message": "waktu tersedia needed"}, "statusCode": 401}
    
    try:
        id_layanan = int(id_layanan)
    except ValueError:
        return {"body": {"message": "invalid id_layanan"}, "statusCode": 401}
    
    try:
        load_dotenv()
        mongodb_uri = os.getenv("MONGODB_URI")
    except Exception as e:
        return {"body": {"message": f"error {e}"}, "statusCode": 401}

    client = pymongo.MongoClient(mongodb_uri)
    db = client.mydb
    reservasi_collection = db.reservasi_layanan
    reminder_collection = db.reminder

    json_data1 = {
        "nama": nama,
        "noHP": phone_number,
        "id_layanan": id_layanan,
        "hariReservasi": hari_reservasi,
        "waktuTersedia": waktu,
    }

    json_data2 = {
        "nama": nama,
        "noHP": phone_number,
        "id_layanan": id_layanan,
        "remind_timestamp": calculate_reminder_time(hari_reservasi),
        "status": "reminder reservasi",
    }

    session = client.start_session()
    session.start_transaction()

    try:
        reservasi_collection.insert_one(json_data1, session=session)
        reminder_collection.insert_one(json_data2, session=session)
        
        session.commit_transaction()
        return {"body": {"message": "success"}, "statusCode": 200}
    except Exception as e:
        session.abort_transaction()
        return {"body": {"message": f"transaction failed: {e}"}, "statusCode": 401}
    finally:
        session.end_session()