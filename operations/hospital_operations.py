from datetime import datetime
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from util import format_date, format_time

md_db = st.secrets["MD_DB"]
md_doc_col= st.secrets["MD_DOC_COL"]
md_ap_col = st.secrets["MD_AP_COL"]

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongo_uri"])

client = init_connection()

def get_doctors_collection():
    database = client[md_db]
    doctor_collection = database[md_doc_col]
    return doctor_collection

def get_appointments_collection():
    database = client[md_db]
    appointment_collection = database[md_ap_col]
    return appointment_collection

def get_doctor_names():
    doctor_collection = get_doctors_collection()
    doctor_names = doctor_collection.find({"doctor"},{})
    print("doctor_id:::::::::",doctor_names)
    return doctor_names

def get_doctor_id(doctor_name):
    doctor_collection = get_doctors_collection()
    doctor_id = doctor_collection.find_one({"_id"},{"doctor":doctor_name})
    print("doctor_id:::::::::",doctor_id)
    return doctor_id

def get_available_slots(doctor,date):
    appointment_collection = get_appointments_collection()
    formated_Date= format_date(date)
    doctor_id = get_doctor_id(doctor)
    slots = appointment_collection.find({"time"},{"doctor_id":doctor_id,"date":formated_Date,"status":"available"})
    print("slots:::::::",slots)
    return slots

def book_doctors_appointment(doctor_name,date_string,time_string,location_string):
    print("book_doctors_appointment")
    try:
        doctor_collection = get_doctors_collection()
        appointment_collection = get_appointments_collection()

        doctors = doctor_collection.find({},{"doctor": doctor_name})
        current_date = datetime.now().date()
        if not doctors:
            print(f"Doctors data not present.")
            return False, f"Kindly recheck doctor's name. Looks like we don't have doctor {doctor_name} in our system."
        else:
            for doc in doctors:
                print(doc["_id"])
                formated_Date= format_date(date_string)
                formatted_time = format_time(time_string)
                appointment = appointment_collection.find({},{"doctor_id":doc,"date":formated_Date,"time":formatted_time})
                for slots in appointment:
                    print(slots)
            return True, f"Appointment booked"    
            
    except Exception as e:
        print(e)

def update_doctor_date_time(doctor_name,date,item):
    slots = get_available_slots(doctor_name,date)
    if "booking" in item:
        st.session_state.booking_slots_time = slots

client.close()