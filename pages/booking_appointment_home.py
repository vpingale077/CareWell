import streamlit as st
from ai71 import AI71
import json
import datetime
from appointment_scheduling import book_appointment
from AI71 import call_ai71
from util import setChatMsg

# Constants
AI71_API_KEY = "your_api_key_here"
default_resp = "I can only assist with booking, canceling, or checking hospital appointments."

# Functions
def classify_intent(intent, entities, msg):
    """Classifies an intent and extracts parameters"""

    allowed_intents = ["Booking an appointment","Canceling an appointment","appointment status","doctor information","hospital information"]

    if intent not in allowed_intents:
        setChatMsg(default_resp)
    if "booking an appointment" in intent:
        
        book_appointment(entities, AI71_API_KEY)
    if "Canceling an appointment" in intent:
        setChatMsg(default_resp)
    if "appointment status" in intent:
        setChatMsg(default_resp)
    if "doctor information" in intent:
        setChatMsg(default_resp)
    if "hospital information" in intent:
        setChatMsg(default_resp)

def handle_ai71_response(response):
    try:
        raw_msg = json.loads(response.choices[0].message.content)
        msg = {k.lower(): v for k, v in raw_msg.items()}
        if "intent" in msg:
            intent = str.lower(msg.get("intent"))
            entities = msg.get("entities", {})
            classify_intent(intent, entities, msg)
        else:
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


for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not AI71_API_KEY:
        st.info("Please add your AI71 API key to continue.")
        st.stop()
   # if prompt in st.session_state.messages:

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = call_ai71(st.session_state.messages, AI71_API_KEY)
    print(response)
    handle_ai71_response(response)