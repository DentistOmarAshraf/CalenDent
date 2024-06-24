#!/usr/bin/python3


from models.clinic import Clinic
from models.city import City
from models.neighborhood import Neighborhood
from models.address import Address
from models.user import User
from models.service import Service
from models.reservation import Reservation
from models.review import Review
from models import storage
from datetime import time

omar = User(email="oamr@goo", password="1234")
cairo = City(name="Cairo")
mokattam = Neighborhood(name="Mokattam")
mkan = Address(text_address="nafora Square")
mkan_2 = Address(text_address="st 81")

cairo.neighborhoods.append(mokattam)
mokattam.addresses.append(mkan)
mokattam.addresses.append(mkan_2)

omar.address = mkan

fayroz = Clinic(name="fayroz")
fayroz.user = omar
fayroz.address = mkan_2

endo = Service(name="endo")
fayroz.services.append(endo)

print(fayroz.services)
print("______________________")
print(endo.clinics)

storage.new(fayroz)
storage.save()

patent = User(email="nn@nn", password="2323")
visit = Reservation(appointment=time(9, 0))
visit.user = patent
fayroz.reservations.append(visit)
rev = Review(text="Nice Clinic", stars=5)
patent.reviews.append(rev)
fayroz.reviews.append(rev)

print("_______________")
print(fayroz.reviews[0])

storage.new(patent)
storage.new(rev)
storage.save()
