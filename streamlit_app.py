import streamlit as st
from ai71 import AI71
import json
import datetime
from appointment_scheduling import book_appointment
from AI71 import call_ai71

# Constants
AI71_API_KEY = "your_api_key_here"

# Functions
def classify_intent(intent, entities, msg):
    """Classifies an intent and extracts parameters"""
    if "Booking an appointment" not in intent:
        return True, msg
    if "Booking an appointment" in intent:
        return book_appointment(entities, AI71_API_KEY)

def handle_ai71_response(response):
    try:
        raw_msg = json.loads(response.choices[0].message.content)
        msg = {k.lower(): v for k, v in raw_msg.items()}
        if "intent" in msg:
            intent = msg.get("intent")
            entities = msg.get("entities", {})
            is_valid, resp = classify_intent(intent, entities, msg)
            return resp
        else:
            return msg
    except (json.JSONDecodeError, IndexError):
        return response.choices[0].message.content

# Streamlit App
st.title("CareWell Chatbot")
st.caption("Chatbot powered by AI71 for Hospital Administartion")

# Sidebar
with st.sidebar:
    AI71_API_KEY = st.text_input("AI71 API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an AI71 API key](https://marketplace.ai71.ai/api-keys)")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Extract only hospital administration intent and entities from the following query in a structured JSON format :Intent: Entities:. Intent must be one of Booking an appointment,Canceling an appointment,appointment status,doctor information,hospital information. All other request must be politly refused. "},
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
    response = handle_ai71_response(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)