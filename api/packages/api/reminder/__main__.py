from dotenv import load_dotenv
import os
import pymongo
import datetime

def calculate_reminder_time(hari_reservasi):
    hari_reservasi_datetime = datetime.datetime.strptime(hari_reservasi, '%Y-%m-%d')
    try:
        timestamp = hari_reservasi_datetime.timestamp()
    except Exception as e:
        return e
    
    return int(timestamp)
    

def main(args):
    id_pasien = args.get('idPasien')
    text = args.get('isiPesan')
    hari_reservasi = args.get('tglKirim')[:10]

    if not id_pasien:
        return {"body": {"message": "idPasien needed"}, "statusCode": 401}

    try:
        id_pasien = int(id_pasien)
    except ValueError:
        return {"body": {"message": "invalid idPasien"}, "statusCode": 401}

    if not text:
        return {"body": {"message": "isiPesan needed"}, "statusCode": 401}
    
    if not hari_reservasi:
        return {"body": {"message": "tglKirim needed"}, "statusCode": 401}
    
    try:
        load_dotenv()
        mongodb_uri = os.getenv("MONGODB_URI")
    except Exception as e:
        return {"body": {"message": f"error {e}"}, "statusCode": 401}

    client = pymongo.MongoClient(mongodb_uri)
    db = client.mydb
    reminder_collection = db.reminder
    pasien_collection = db.pasien

    timestamp = calculate_reminder_time(hari_reservasi)
    pasien = pasien_collection.find_one({"id_pasien": id_pasien})
    if not pasien:
        return {"body": {"message": "pasien not found"}, "statusCode": 401}

    if type(timestamp) != int:
        return {"body": {"message": f"error {timestamp}"}, "statusCode": 401}

    nama = pasien.get("nama_pasien", "Unknown")

    phone_number = None
    if pasien.get("data_kb"):
        phone_number = pasien.get("no_hp", None)
    elif pasien.get("data_imunisasi"):
        phone_number = pasien.get("no_hp", None)
    elif pasien.get("data_kehamilan"):
        phone_number = pasien.get("data_kehamilan", {}).get("section2", {}).get("noTelp", None)

    if not phone_number:
        return {"body": {"message": "phone_number data not found"}, "statusCode": 401}
    
    json_data = {
        "nama": nama,
        "noHP": phone_number,
        "text": text,
        "remind_timestamp": timestamp,
        "status": "reminder layanan"
    }
    session = client.start_session()
    session.start_transaction()

    try:
        reminder_collection.insert_one(json_data, session=session)
        
        session.commit_transaction()
        return {"body": {"message": "success"}, "statusCode": 200}
    except Exception as e:
        session.abort_transaction()
        return {"body": {"message": f"create reminder failed: {e}"}, "statusCode": 401}
    finally:
        session.end_session()
