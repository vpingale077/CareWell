import datetime
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
    formatted_date = today.strftime("%d/%m/%Y")
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

def format_date(date):
    return date.strftime("%d/%m/%Y")

def format_time(time):
    return time.strftime("%H:%M")