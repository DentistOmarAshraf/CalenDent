#!/usr/bin/python3

from models import storage
from models.city import City
from models.neighborhood import Neighborhood
from models.address import Address
from models.user import User

cairo = City(name="cairo")
mokattam = Neighborhood(name="mokattam")
manial = Neighborhood(name="Manial")
nafora_sq = Address(text_address="Nafora Square near to Abo hanafy")

mokattam.addresses.append(nafora_sq)
cairo.neighborhoods.append(mokattam)
cairo.neighborhoods.append(manial)
storage.new(cairo)
storage.save()

print(cairo)
print("---------------------------")
for x in cairo.neighborhoods:
    print(x)

print("------------------------")
for x in mokattam.addresses:
    print(x)

omar = User(email="omar_ashraf@live.com", password="98762")
omar_address = Address(text_address="Mokattam St.81")
omar_address.neighborhood = mokattam
omar.address = omar_address
print("-----------------------------")
print(omar.address.to_dict())

storage.new(omar)
storage.save()
