import json
from turtle import st
from operations.hospital_operations import book_doctors_appointment
from util import get_date_in_format, is_valid_date, setChatMsg


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

    # Check if the doctor and location are strings
    if not all(isinstance(parameters[key], str) for key in ["doctor", "location"]):
       resp = "Invalid data types for doctor or location"
       setChatMsg(resp)

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
        return True, f"Please specify date for Appointment with {doctor_name} in {location_string}"

    # Check if the date is not invalid
    if date_updated["date"] != "invalid":
        return True, f"Appointment scheduled for {doctor_name} on {date_updated['date'][0]} in {location_string}"

    # Return an error message if the date is invalid
    return False, "Please provide date of appointment"