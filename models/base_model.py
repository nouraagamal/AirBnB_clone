#!/usr/bin/python3
"""Defines all common attributes/methods for other classes.
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Base class for models."""

    def __init__(self, *args, **kwargs):
        """Initialization of a BaseModel instance.
        Args:
            **kwargs: dict of key-values arguments
        """
        if kwargs:
            form = '%Y-%m-%dT%H:%M:%S.%f'
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == 'created_at':
                    self.created_at = datetime.strptime(
                        kwargs['created_at'], form)
                elif key == 'updated_at':
                    self.updated_at = datetime.strptime(
                        kwargs['updated_at'], form)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """print: [<class name>] (<self.id>) <self.__dict__>"""

        name = self.__class__.__name__
        return "[{}] ({}) {}".format(name, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary that contains all
        keys/values of the instance"""
        my_dict = self.__dict__.copy()
        my_dict['updated_at'] = self.updated_at.isoformat()
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['__class__'] = self.__class__.__name__
        return my_dict
