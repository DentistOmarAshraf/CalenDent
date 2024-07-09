#!/usr/bin/python3

from models.clinic import Clinic
from models.reservation import Reservation
from datetime import time

calen = Clinic(name="omar", opening_time=time(17, 0), closing_time=time(22, 0), visit_duration=time(0,30))

res = Reservation(appointment=time(17,0))
print(calen.visits_avaliable)
calen.reservations.append(res)
print(calen.visits_avaliable)
