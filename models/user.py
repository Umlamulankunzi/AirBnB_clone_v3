#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import hashlib
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship



class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        md5 = hashlib.md5()
        password = kwargs.get('password')
        md5.update(password.encode('utf-8'))
        kwargs['password'] = md5.hexdigest()
        super().__init__(*args, **kwargs)
