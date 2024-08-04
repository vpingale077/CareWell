import streamlit as st
import json
from appointment_scheduling import book_appointment, check_available_doctors
from AI71 import call_ai71
from operations.hospital_operations import get_doctor_names, update_doctor_date_time
from util import setChatMsg

# Constants
AI71_API_KEY = "your_api_key_here"
default_resp = "I can only assist with booking, canceling, or checking hospital appointments."

if 'booking_slots_time' not in st.session_state:
    st.session_state.booking_slots_time = None

if 'booking_error' not in st.session_state:
    st.session_state.booking_error=None

if 'booking_slots_time_disable' not in st.session_state:
    st.session_state.booking_slots_time_disable=True

# Functions
def classify_intent(intent, entities):
    """Classifies an intent and extracts parameters"""

    allowed_intents = ["Booking an appointment","Canceling an appointment","appointment status","doctor information","hospital information"]
    print("entities",entities)
    if intent not in allowed_intents:
        setChatMsg(default_resp)
    if "booking an appointment" in intent:
        book_appointment(entities, AI71_API_KEY)
    if "Canceling an appointment" in intent:
        setChatMsg(default_resp)
    if "appointment status" in intent:
        setChatMsg(default_resp)
    if "doctor information" in intent:
        check_available_doctors(entities,AI71_API_KEY)
    if "hospital information" in intent:
        setChatMsg(default_resp)

def handle_ai71_response(response):
    try:
        raw_msg = json.loads(response.choices[0].message.content)
        msg = {k.lower(): v for k, v in raw_msg.items()}
        print("handle_ai71_response_msg",msg)
        if "intent" in msg:
            intent = str.lower(msg.get("intent"))
            entities = msg.get("entities", {})
            classify_intent(intent, entities)
        else:
            print("else intent")
            setChatMsg(msg)
    except (json.JSONDecodeError, IndexError):
        setChatMsg(default_resp)

# Streamlit App
st.title("CareWell Chatbot")
st.caption("Chatbot powered by AI71 for Hospital Administartion")

# Sidebar
with st.sidebar:
    AI71_API_KEY = st.text_input("AI71 API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an AI71 API key](https://marketplace.ai71.ai/api-keys)")
    """
    I can help you for:\n
    """
    st.page_link("streamlit_app.py", label="Home", icon="🏥")
    st.page_link("pages/booking_appointment_home.py", label="Booking an appointment", icon="🧑‍⚕️")
    #st.page_link("operations/booking_appoitment_home.py", label="Canceling an appointment", icon="🚫")
    #st.page_link("operations/booking_appoitment_home.py", label="Appointment status", icon="✅")
    
    #Booking an appointment\n
    #Canceling an appointment\n
    #Appointment status\n
    #Doctor information\n
    #Hospital information
    #"""

# Chat Interface
@st.dialog("How can I help you?")
def vote(item):
    if "Booking" in item:
        doctor_names = get_doctor_names()
        st.write(f"Enter details below?")
        name = st.text_input("What's your name?")
        doctor=st.selectbox("Doctors name?",options=doctor_names)
        date=st.date_input("Appointment Date?",key="booking_date", value=None,on_change=update_doctor_date_time,args=(doctor,item))
        time=st.time_input("Time?",value=st.session_state.booking_slots_time)
        st.session_state.book_appt = {"item":item,"doctor":doctor, "user":name,"date":date, "time":time, "location":"dallas"}
        st.session_state.booking_error
        st.button("Submit",on_click=book_appointment,args=(st.session_state.book_appt,AI71_API_KEY))
    if "Canceling" in item:
        print("Inside cancellation")
        appoitment_no = st.text_input("Appointment Number?")
        st.write("Appointment number not available? Enter details below")
        c_name = st.text_input("What's your name?",key="c_name")
        c_doctor=st.text_input("Doctors name?",key="c_doctor")
        c_name=st.date_input("Appointment Date?", value=None,key="c_date")
        c_time=st.time_input("Time?",value=None,key="c_time")
        if st.button("Submit"):
            st.session_state.cancel_apt = {'item':item,"appt_id":appoitment_no,"doctor":c_doctor,"user":c_name,"date":c_name,"time":c_time}

if "vote" not in st.session_state:
    if st.button("Booking an appointment"):
        print("Booking selected")
        vote("Booking")
    if st.button("Canceling an appointment"):
        vote("Canceling")
    if st.button("Appointment status"):
        vote("Status")    
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Exctract and Identify intent and entities from the following query in a structured JSON format :Intent: Entities:. Intent must be one of Booking an appointment,Canceling an appointment,appointment status,doctor information,hospital information."},
        {"role": "assistant", "content": "How can i help you?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not AI71_API_KEY:
        st.info("Please add your AI71 API key to continue.")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = call_ai71(st.session_state.messages, AI71_API_KEY)
    print(response)
    #print(st.session_state.book_appt)
    handle_ai71_response(response)