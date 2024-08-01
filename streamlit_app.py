from AI71 import call_ai71
from appointment_scheduling import book_appointment
import streamlit as st
import json

# Constants
AI71_API_KEY = "your_api_key_here"

# Functions
def intent_classify(msg):
    """Classifies an intent and extracts parameters"""
    msg_json = json.loads(msg)
    intent = msg_json["intent"]
    parameters = msg_json["parameters"]
    
    if "appointment_scheduling" not in intent:
        return True, msg
    if "appointment_scheduling" in intent:
        return book_appointment(parameters,AI71_API_KEY)
# Streamlit App
st.title("CareWell Chatbot")
st.caption("Chatbot powered by AI71")

# Sidebar
with st.sidebar:
    AI71_API_KEY = st.text_input("AI71 API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an AI71 API key](https://marketplace.ai71.ai/api-keys)")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """Classify the following text into a hospital administration intent and extract relevant parameters. Strictly follow intent mentioned below. If user is asking about any medical condition or healthcare information ask to take dr appoitment. Guide user for using mentioned intent only and available features for users.
Output the results in JSON format with the following structure.
Intent must be from one of the below this appointment_scheduling,appointment_cancellation,patient_records,staff_management,billing_and_insurance,facility_management,supply_management,quality_control,financial_management.
If intent is not one of them respond with unknow_intent.
Example:Prompt: "Schedule an appointment for Dr. Smith on Tuesday at 2 PM"
Output:{"intent": "appointment_scheduling","parameters": {"doctor": "","date": "","time": ""}}"""},
        {"role": "assistant", "content": "How can I help you?"}
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
    response = call_ai71(st.session_state.messages,AI71_API_KEY)
    print(response)
    msg = response.choices[0].message.content
    if "intent" in msg:
        print(msg)
        isValid, resp = intent_classify(msg)
        st.session_state.messages.append({"role": "assistant", "content": resp})
        st.chat_message("assistant").write(resp)
    else:
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)