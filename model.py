class Doctor:
    def __init__(self, id, name, time,type, hospital, degree, location):
        self.id = id
        self.name = name
        self.time = time
        self.hospital = hospital
        self.degree = degree
        self.type =type
        self.location = location
        self.appointments = []

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

class Appointment:
    def __init__(self,doctor_id, status, time, date, hospital):
        self.doctor_id = doctor_id
        self.status = status
        self.time = time
        self.date = date
        self.hospital = hospital