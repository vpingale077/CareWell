import datetime
import json

import streamlit as st
from AI71 import call_ai71
from model import Doctor
from operations.hospital_operations import book_doctors_appointment, get_available_slots, get_doctor_details, get_doctor_id, get_doctor_names, get_slots_based_on_date
from util import create_doctor_table, find_doctor_from_list_by_name, get_date_in_format, is_valid_date, setChatMsg, setResponse


def book_appointment(raw_parameters: dict, ai71_api_key: str) -> tuple:
    """
    Books an appointment with a doctor.

    Args:
    - raw_parameters (dict): A dictionary containing the appointment details.
    - ai71_api_key (str): The AI71 API key.

    Returns:
    - tuple: A tuple containing a boolean indicating whether the appointment was booked successfully and a message.
    """

    # Define the required keys for the appointment
    required_keys = ["doctor", "date", "time", "location"]

    # Convert the raw parameters to lowercase
    parameters = {k.lower(): v for k, v in raw_parameters.items()}

    # Check each required key and ask the user to share details if missing
    missing_keys = [key for key in required_keys if key not in parameters]
    if missing_keys:
        resp = f"Please provide the following details for appointment scheduling: {', '.join(missing_keys)}"
        setChatMsg(resp)
        return

    # Check if the doctor and location are strings
    if not all(isinstance(parameters[key], str) for key in ["doctor", "location"]):
       resp = "Invalid data types for doctor or location"
       setChatMsg(resp)
       return

    # Extract the doctor name, date string, time string, and location string
    doctor_name = parameters.get("doctor")
    date_string = parameters.get("date")
    time_string = parameters.get("time")
    location_string = parameters.get("location")

    # Check if the date is valid
    if is_valid_date(date_string):
        # Book the appointment
        is_app_booked, response = book_doctors_appointment(doctor_name, date_string, time_string, location_string)
        if is_app_booked:
            resp=f"Appointment scheduled for {doctor_name} on {date_string} {time_string} in {location_string}"
            setChatMsg(resp)
        else:
            return False, response

    # Get the updated date
    date_updated = json.loads(get_date_in_format(date_string, ai71_api_key).choices[0].message.content)

    # Check if the date is valid
    if len(date_updated["date"]) > 1:
        print("specify date")
        return True, f"Please specify date for Appointment with {doctor_name} in {location_string}"

    # Check if the date is not invalid
    if date_updated["date"] != "invalid":
        # Book the appointment
        is_app_booked, response = book_doctors_appointment(doctor_name, date_string, time_string, location_string)
        if is_app_booked:
            resp=f"Appointment scheduled for {doctor_name} on {date_string} {time_string} in {location_string}"
            setChatMsg(resp)
        else:
            return False, response
    else:
        print("date missing")
        # Return an error message if the date is invalid
        return False, "Please provide date of appointment"

def check_available_doctors(raw_parameters: dict,ai71_api_key: str) -> tuple:
    available_doc = get_doctor_details();
    if raw_parameters is None or not raw_parameters:
        set_doctors_info_table(create_doctor_table(available_doc))
    else:
        available_keys = ["doctor", "date", "time", "location","hospital"]
        # Convert the raw parameters to lowercase
        if isinstance(raw_parameters, dict):
            parameters = {k.lower(): v for k, v in raw_parameters.items()}
            missing_keys = [key for key in available_keys if key not in parameters]
        else:
            missing_keys=available_keys
        for key in missing_keys:
            if 'doctor' in key:
                set_doctors_info_table(create_doctor_table(available_doc))
            else:
                doctor_name =parameters.get("doctor").rstrip() 
                #doc_name_regex = {"$regex": f".*{doctor_name}.*", "$options": "i"} 
                #print("doc_name_regex",doc_name_regex)
                #doc_ids = get_doctor_id(doc_name_regex)
                docs = find_doctor_from_list_by_name(doctor_name)
                print("docs:::::::::::::::",docs)
                if docs.len() == 0:
                    set_doctors_info_table(create_doctor_table(available_doc))
                elif docs.len() == 1:
                    if 'date' in missing_keys:
                        date = datetime.date.today()
                    else:
                        date = parameters["date"]
                    slots = get_available_slots(docs[0].id,date)
                    set_available_slots_details(repr(docs),slots,date,ai71_api_key)
                else:
                    propmt= f"For which doctor you want to book appointment: {', '.join(docs)}"
                    setChatMsg(propmt)


def set_doctors_info_table(available_doc):
    print("set_doctors_info_table::::::::::")
    prompt = f"This is list of available doctors."
    st.session_state.messages.append({"role": "assistant_custom", "content": available_doc.to_string()})
    with st.chat_message("assistant_custom"):
        st.write(prompt)
        st.dataframe(available_doc)

def set_available_slots_details(doctor_name,slots,date,ai71_api_key):
    prompt = f"This are details of available doctor {doctor_name} details for date {date} and time slots {slots} reply like a hospital admin asisstant in 30 words, where slots details can be clubbed."
    st.session_state["messages"] = [
        {"role": "system", "content": prompt},
    ]
    response = call_ai71(st.session_state.messages,ai71_api_key)
    setResponse(response)
    print("set_available_slots_details",response)