#!/usr/bin/python3
"""
Data Base Storage Engine
"""


from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.address import Address
from models.city import City
from models.neighborhood import Neighborhood
from models.review import Review
from models.clinic import Clinic
from models.reservation import Reservation
from models.service import Service


classes = [User, Address, City, Neighborhood, Review,
           Clinic, Reservation, Service]


class DBstorage:
    """Data Base Engine"""
    __session = None
    __engine = None

    def __init__(self):
        """Start Data Base engine"""
        usr = getenv("CALEN_USR")
        pwd = getenv("CALEN_PWD")
        host = getenv("CALEN_HOST")
        db = getenv("CALEN_DB")

        eng_string = f"mysql+mysqldb://{usr}:{pwd}@{host}:3306/{db}"

        DBstorage.__engine = create_engine(eng_string, pool_pre_ping=True)

        if getenv("CALEN_ENV") == "test":
            metadata = MetaData()
            metadata.reflect(bind=DBstorage.__engine)
            metadata.drop_all(bind=DBstorage.__engine)

    def new(self, obj):
        """Add instance to table"""
        DBstorage.__session.add(obj)

    def save(self):
        """saving after adding table"""
        DBstorage.__session.commit()

    def delete(self, obj=None):
        """Delete instance from table"""
        if obj:
            DBstorage.__session.delete(obj)
            DBstorage.__session.commit()

    def all(self, cls=None):
        """Return A query of table (class)"""
        if cls:
            arrOfInstance = DBstorage.__session.query(cls).all()
        else:
            arrOfInstance = []
            for cl in classes:
                arrOfInstance += DBstorage.__session.query(cl).all()

        to_ret = {}
        for instance in arrOfInstance:
            key = f"{instance.__class__.__name__}.{instance.id}"
            to_ret[key] = instance
        return to_ret

    def reload(self):
        """Creating DataBase Table and start a scoped Session"""
        Base.metadata.create_all(DBstorage.__engine)
        Session = sessionmaker(bind=DBstorage.__engine, expire_on_commit=False)
        DBstorage.__session = scoped_session(Session)

    def close(self):
        """Remove Current Session"""
        DBstorage.__session.remove()
