#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kw):
        """Instatntiates a new model"""
        if not kw:
            now = datetime.now()
            self.id = str(uuid.uuid4())
            self.created_at = now
            self.updated_at = now
        else:
            now = datetime.now()
            if 'updated_at' in kw:
                kw['updated_at'] = datetime.strptime(kw['updated_at'], time)
            if 'created_at' in kw:
                kw['created_at'] = datetime.strptime(kw['created_at'], time)
            if 'id' not in kw:
                self.id = str(uuid.uuid4())
            if '__class__' in kw:
                del kw['__class__']
            if 'updated_at' not in kw:
                self.updated_at = now
            if 'created_at' not in kw:
                self.created_at = now
            for key, value in kw.items():
                setattr(self, key, value)
            self.__dict__.update(kw)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        from models import storage
        storage.delete(self)