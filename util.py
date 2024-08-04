import datetime
import pandas as pd
import streamlit as st
from AI71 import call_ai71

def is_valid_date(date_string):
    """Checks if a date string is valid"""
    try:
        if isinstance(date_string, datetime.date):
            return True
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_date_in_format(date_string,AI71_API_KEY):
    """Converts a date string to a formatted date"""
    today = datetime.date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    messages = [{
        "role": "system",
        "content": "date format Y-m-d. If value contains days like Tuesday, calculate next date for that day or if it contains date range like weekends or next week, calculate date range based on date " + formatted_date + ". Revert in JSON format {'date':['']}."
    }]
    messages.append({"role": "user","content": date_string})
    print('messages', messages)
    response = call_ai71(messages,AI71_API_KEY)
    print('get_date_in_format', response)
    return response

def setChatMsg(response):
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

def setResponse(response):
    resp = response.choices[0].message.content
    setChatMsg(resp)

def format_date(date):
    return date.strftime("%Y-%m-%d")

def format_time(time):
    return time.strftime("%H:%M")

def find_doctor_from_list_by_name(doctors, name):
  """Finds doctors whose names contain the search term.

  Args:
    doctors: A list of Doctor objects.
    name: The search term to look for.

  Returns:
    A list of Doctor objects matching the search term.
  """

  results = [doctor for doctor in doctors if name.lower() in doctor['name'].lower()]
  return results

def create_doctor_table(doctors):
    """Creates a Pandas DataFrame from a list of Doctor objects.

    Args:
        doctors: A list of Doctor objects.

    Returns:
        A Pandas DataFrame containing doctor information.
    """

    data = [{'name': doctor.name, 'degree': doctor.degree, 'speciality': doctor.type, 'timings': doctor.time, 'hospital': doctor.hospital, 'location': doctor.location} for doctor in doctors]
    df = pd.DataFrame(data)
    return df

def remove_messages_by_role(messages, role):
  """Removes messages with the specified role from the list.

  Args:
    messages: A list of messages.
    role: The role of the messages to remove.

  Returns:
    A new list of messages without the specified role.
  """

  return [message for message in messages if message['role'] != role]