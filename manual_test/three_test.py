#!/usr/bin/python3

from models import storage
from models.user import User, RoleType
from models.city import City
from models.address import Address
from models.neighborhood import Neighborhood


cairo = City(name="cairo")
mokattam = Neighborhood(name="Mokkattam")
mkan = Address(text_address="nafora Square")
omar = User(email="omar@live.com", password="1234")

cairo.neighborhoods.append(mokattam)
mkan.neighborhood = mokattam
omar.address = mkan
omar.role = RoleType.USER

storage.new(omar)
storage.new(cairo)
storage.new(mkan)
storage.new(mokattam)

storage.save()
