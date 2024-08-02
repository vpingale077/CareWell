import datetime
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

md_username = st.secrets["MD_USER"]
md_password = st.secrets["MD_PASS"]
md_db = st.secrets["MD_DB"]
md_doc_col= st.secrets["MD_DOC_COL"]
md_ap_col = st.secrets["MD_AP_COL"]

uri = "mongodb+srv://{md_username}:{md_password}@cluster0.tgg39md.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def book_doctors_appointment(doctor_name,date_string,time_string,location_string):
    print("book_doctors_appointment")
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        database = client[md_db]
        doctor_collection = database[md_doc_col]
        appointment_collection = database[md_ap_col]

        doctors = doctor_collection.find({},{"doctor": doctor_name})
        current_date = datetime.now().date()
        if not doctors:
            print(f"Doctors data not present.")
            return False, f"Kindly recheck doctor's name. Looks like we don't have doctor {doctor_name} in our system."
        else:
            for doc in doctors:
                print(doc["_id"])
                appointment = appointment_collection.find({},{"doctor_id":doc,"date":date_string})
                for slots in appointment:
                    print(slots)
            return True, f"Appointment booked"    
            
    except Exception as e:
        print(e)