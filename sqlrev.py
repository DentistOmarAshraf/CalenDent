#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine("mysql+mysqldb://omar:9344725054@localhost:3306/newdb")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Clinic(Base):
    __tablename__ = "clinic"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    user_id = Column(Integer, ForeignKey("user.id"))
    address_id = Column(Integer, ForeignKey("address.id"))
    user = relationship("User", back_populates="clinic")
    address = relationship("Address", cascade="all, delete")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address", cascade="all, delete")
    clinic = relationship("Clinic", cascade="all, delete", back_populates="user")

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

Base.metadata.create_all(engine)

cairo = City(id=1, name="Cairo")
place_1 = Neighborhood(id=1, name="Mokattam")
mkan_1 = Address(id=1, name="Nafora")
mkan_2 = Address(id=2, name="Nafora")

cairo.neighborhoods.append(place_1)
place_1.addresses.append(mkan_1)
place_1.addresses.append(mkan_2)

omar = User(id=1, name="omar")
omar.address = mkan_1

dental = Clinic(id=1, name="Fayroz")
dental.user = omar
dental.address = mkan_2

session.add(cairo)
session.add(omar)
session.add(dental)
session.commit()
session.delete(omar)
session.commit()
