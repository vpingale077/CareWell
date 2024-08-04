from datetime import datetime
import streamlit as st
from pymongo.mongo_client import MongoClient
from bson import ObjectId
from pymongo.server_api import ServerApi

from model import Doctor
from util import format_date, format_time

md_db = st.secrets["MD_DB"]
md_doc_col= st.secrets["MD_DOC_COL"]
md_ap_col = st.secrets["MD_AP_COL"]

def get_doctors_collection(client):
    database = client[md_db]
    doctor_collection = database[md_doc_col]
    return doctor_collection

def get_appointments_collection(client):
    database = client[md_db]
    appointment_collection = database[md_ap_col]
    return appointment_collection

@st.cache_data(ttl=36000)
def get_doctor_names():
    client = MongoClient(st.secrets["mongo_uri"])
    doctor_collection = get_doctors_collection(client)
    doctor_names = doctor_collection.find({})
    print("doctor_id:::::::::",doctor_names)
    doctor_list=[doc["doctor"]+" | "+doc["hospital"] for doc in doctor_names]
    print("doc_list",doctor_list)
    client.close()
    return doctor_list

@st.cache_data(ttl=36000)
def get_doctor_details():
    client = MongoClient(st.secrets["mongo_uri"])
    doctor_collection = get_doctors_collection(client)
    doctor_names = doctor_collection.find({})
    print("doctor_id:::::::::",doctor_names)
    doctor_list=[Doctor(doc["_id"],doc["doctor"],doc["timings"],doc["type"],doc["hospital"],doc["degree"],doc["location"]) for doc in doctor_names]
    print("doc_list",doctor_list)
    client.close()
    return doctor_list

def get_doctor_id(doctor_name):
    client = MongoClient(st.secrets["mongo_uri"])
    print("get_doctor_id:",doctor_name.rstrip())
    doctor_collection = get_doctors_collection(client)
    doctor_id = doctor_collection.find({"doctor":doctor_name.rstrip()})
    print("doctor_id:::::::::",doctor_id.collection.count_documents)
    doc_id = [doc["_id"] for doc in doctor_id]
    print("doc_id:::::::::",doc_id)
    client.close()
    return doc_id

def get_available_slots(doctor,date):
    client = MongoClient(st.secrets["mongo_uri"])
    appointment_collection = get_appointments_collection(client)
    formated_Date= format_date(date)
    if "|" in doctor:
        doctor_id = get_doctor_id(doctor.split("|")[0])
    else:    
        doctor_id =doctor
    print("doctor_id:",doctor_id,"date:",formated_Date)
    slots = appointment_collection.find({"doctor_id":ObjectId(doctor_id[0]),"date":formated_Date,"status":"available"})
    print("slots:::::::",slots)
    available_slots = [slot["time"] for slot in slots]
    print("available_slots",available_slots)
    client.close()
    return available_slots

def book_doctors_appointment(doctor_name,date_string,time_string,location_string):
    print("book_doctors_appointment")
    try:
        client = MongoClient(st.secrets["mongo_uri"])
        doctor_collection = get_doctors_collection(client)
        appointment_collection = get_appointments_collection(client)

        doctors = doctor_collection.find({"doctor": doctor_name})
        current_date = datetime.now().date()
        if not doctors:
            print(f"Doctors data not present.")
            return False, f"Kindly recheck doctor's name. Looks like we don't have doctor {doctor_name} in our system."
        else:
            for doc in doctors:
                print(doc["_id"])
                formated_Date= format_date(date_string)
                formatted_time = format_time(time_string)
                appointment = appointment_collection.find({"doctor_id":doc,"date":formated_Date,"time":formatted_time})
                for slots in appointment:
                    print(slots)
            return True, f"Appointment booked"    
            
    except Exception as e:
        print(e)
    finally:
        client.close()

def update_doctor_date_time(doctor_name,item):
    date=st.session_state.booking_date
    slots = get_available_slots(doctor_name,date)
    print("update_doctor_date_time_item:",item)
    print("update_doctor_date_time_slots:",slots)
    if "booking" in item:
        if(slots.count==0):
            st.session_state.booking_error = "Soryy, Slots are not available"
        else:
            st.session_state.booking_slots_time = slots

def get_slots_based_on_date(doc_id,date):
    print("get_slots_based_on_date:::",doc_id,date)
