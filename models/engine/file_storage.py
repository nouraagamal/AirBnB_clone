#!/user/bin/python3

"""recreate a BaseModel from another one by using a dictionary representation
"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class_dict = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "City": City,
    "Review": Review,
    "State": State
}

class FileStorage:
    """serializes instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects."""
        return type(self).__objects

    def new(self obj):
        """sets in __objects the obj with key <obj class name>.id."""
        if obj.id in type(self).__objects:
            print("exists")
            return
        key = "{}.{}".format(obj.__class__.name, obj.id)
        type(self).__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file."""

        new_list = []
        for obj in type(self).__objects.values():
            new_list.append(obj.to_dict())
        with open(type(self).__file_path, "w", encoding='utf-8') as file:
            json.dump(new_list ,file)

    def reload(self):
        """Deserializes the JSON file."""
        try:
            with open(type(self).__file_path, "r", encoding='utf-8' ) as file:
                new_obj = json.load(file)
                    for key, val in new_obj.items():
                        obj = self.class_dict[val['__class__']](**val)
                        type(self).__objects[key] = obj
            except Exception:
                pass

