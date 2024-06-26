#!/usr/bin/python3

from models import storage
from models.city import City
from models.neighborhood import Neighborhood


cairo = City(name="Cairo")

neighborhoods = [
    "Mokattam", "Manial", "Zamalek", "Heliopolis", "Maadi", "Nasr City", 
    "Garden City", "Dokki", "Mohandiseen", "Shubra", "New Cairo", 
    "Hadayek El-Kobba", "Ain Shams", "El-Marg", "Sayeda Zeinab", 
    "Abbasia", "Bab El-Louk", "Bulaq", "Faisal", "Giza", "Imbaba", 
    "Kit Kat", "El-Haram", "El-Agouza", "Masr El-Gedida", "Mokkatam Heights"
]

for n in neighborhoods:
    cairo.neighborhoods.append(Neighborhood(name=n))


alex = City(name="Alexandiria")

neighborhoods = [
    "Al-Montazah", "Smouha", "Sidi Gaber", "Gleem", "Stanley", 
    "Roushdy", "San Stefano", "Kafr Abdu", "Al-Shatby", "Bab Sharq", 
    "El Raml Station", "El Azarita", "El Ibrahimiya", "El Anfoushy", 
    "El Mansheya", "Sidi Bishr", "Miami", "Victoria", "Asafra", 
    "Mandara", "Al Agamy", "Borg El Arab", "Amreya", "El Soyof", 
    "Moharam Bek"
]

for n in neighborhoods:
    alex.neighborhoods.append(Neighborhood(name=n))


storage.new(cairo)
storage.new(alex)
storage.save()
