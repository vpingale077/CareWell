import json
from util import get_date_in_format, is_valid_date


def book_appointment(raw_parameters,AI71_API_KEY):
    required_keys = ["doctor", "date"]
    parameters= {k.lower(): v for k, v in raw_parameters.items()}
    doctor_name = parameters.get("doctor")
    date_string = parameters.get("date")
    time_string = parameters.get("time")
    location_string = parameters.get("location")

    if not all(key in parameters for key in required_keys):
        return False, "Please provide details for appointment scheduling"

    if not all(isinstance(parameters[key], str) for key in ["doctor", "location"]):
        return False, "Invalid data types for doctor or location"

    #date = parameters["date"]
    if is_valid_date(date_string):
        return True, f"Appointment scheduled for {doctor_name} on {date_string} {time_string} in {location_string}"

    date_updated = json.loads(get_date_in_format(date_string,AI71_API_KEY).choices[0].message.content)
    print(date_updated["date"])
    if (len(date_updated["date"])) > 1:
        return True, f"Please specify date for Appointment with {doctor_name} in {location_string}"

    if date_updated["date"] != "invalid":
        return True, f"Appointment scheduled for {doctor_name} on {date_updated['date'][0]} in {location_string}"

    return False, "Please provide date of appointment"