#!/usr/bin/python3
""" Db storage module """

from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
from models.base_model import Base
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """ This class manages storage of hbnb models in a database"""
    __engine = None
    __session = None

    def __init__(self):
        """ Constructor """
        from models.base_model import Base
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from os import getenv

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        classes = [BaseModel, User, State, City, Place, Amenity, Review]
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            return self.__session.query(cls)
        else:
            obj_list = []
            for c in classes:
                obj_list += self.__session.query(c)
            return obj_list

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
