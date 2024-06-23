#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from os import getenv

pwd = getenv("PWD")
engine = create_engine(f"mysql+mysqldb://omar:{pwd}@localhost:3306/newdb")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    clinic = relationship("Clinic", secondary="clinic_service",
            back_populates="services")


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    user_id = Column(Integer, ForeignKey("user.id"))
    clinic_id = Column(Integer, ForeignKey("clinic.id"))
    user = relationship("User", back_populates="reservation")
    clinic = relationship("Clinic", back_populates="reservations")

class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    text = Column(String(1024))
    clinic_id = Column(Integer, ForeignKey("clinic.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    clinic = relationship("Clinic", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


clinic_service = Table("clinic_service", Base.metadata,
        Column("service_id", Integer, ForeignKey("service.id"), primary_key=True),
        Column("clinic_id", Integer, ForeignKey("clinic.id"), primary_key=True))


class Clinic(Base):
    __tablename__ = "clinic"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    user_id = Column(Integer, ForeignKey("user.id"))
    address_id = Column(Integer, ForeignKey("address.id"))
    user = relationship("User", back_populates="clinic")
    address = relationship("Address", cascade="all, delete", back_populates="clinics")
    reviews = relationship("Review", cascade="all, delete", back_populates="clinic")
    reservations = relationship("Reservation", back_populates="clinic",
                cascade="all, delete")
    services = relationship("Service", secondary="clinic_service",
            back_populates="clinic")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address", cascade="all, delete", back_populates="users")
    clinic = relationship("Clinic", cascade="all, delete", back_populates="user")
    reviews = relationship("Review", cascade="all, delete", back_populates="user")
    reservation = relationship("Reservation", cascade="all, delete",
            back_populates="user")
    role = relationship("Role", secondary="user_role", back_populates="user")

user_role = Table("user_role", Base.metadata,
        Column("user_id", ForeignKey("user.id"), primary_key=True),
        Column("role_id", ForeignKey("role.id"), primary_key=True))

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    user = relationship("User", secondary="user_role", back_populates="role")

class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    neighborhoods = relationship("Neighborhood", cascade="all, delete",
                                back_populates="city")

class Neighborhood(Base):
    __tablename__ = "neighborhood"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship("City", back_populates="neighborhoods")
    addresses = relationship("Address", back_populates="neighborhood", cascade="all, delete")

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    neighborhood_id = Column(Integer, ForeignKey("neighborhood.id"))
    neighborhood = relationship("Neighborhood", back_populates="addresses")
    users = relationship("User", back_populates="address")
    clinics = relationship("Clinic", back_populates="address")

Base.metadata.create_all(engine)

cairo = City(id=1, name="Cairo")
place_1 = Neighborhood(id=1, name="Mokattam")
mkan_1 = Address(id=1, name="Nafora")
mkan_2 = Address(id=2, name="Nafora")
mkan_3 = Address(id=3, name="st 81")

cairo.neighborhoods.append(place_1)
place_1.addresses.append(mkan_1)
place_1.addresses.append(mkan_2)
place_1.addresses.append(mkan_3)

normal_user = Role(id=1, name="Normal")
doctor_user = Role(id=2, name="Doctor")

omar = User(id=1, name="omar")
omar.role.append(normal_user)
omar.role.append(doctor_user)
nada = User(id=2, name="nada")
nada.role.append(normal_user)
omar.address = mkan_1
nada.address = mkan_3

dental = Clinic(id=1, name="Fayroz")
dental.user = omar
dental.address = mkan_2

review = Review(id=1, text="Good_clinic")
review.user = omar
review.clinic = dental

new_res = Reservation(id=1, name="Endo")
new_res.clinic = dental
new_res.user = nada

endo = Service(id=1, name="Endo")
opt = Service(id=2, name="OPT")
dental.services.append(endo)
dental.services.append(opt)

session.add(cairo)
session.add(omar)
session.add(dental)
session.add(review)
session.add(new_res)
session.add(endo)
session.add(opt)
print(new_res.user.name)
print(new_res.clinic.name)
print(dental.services[0].name)
print(dental.services[1].name)
print(mkan_2.clinics)
print(mkan_1.users)
print(omar.role)
print(nada.role)
session.commit()
