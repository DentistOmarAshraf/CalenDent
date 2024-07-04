#!/usr/bin/python3

from models import storage
from models.service import Service

ser = ["Braces",
        "Cosmetic Dentistry",
        "Crowns",
        "Dental Implants",
        "Dentures",
        "Endodontics",
 "Fillings",
"Gum Treatment",
"Oral Surgery",
"Orthodontics",
"Pediatric Dentistry",
"Periodontics",
"Root Canal Treatment",
"Teeth Cleaning",
"Teeth Whitening",
"Tooth Extraction"]

for x in ser:
    storage.new(Service(name=x))

storage.save()
