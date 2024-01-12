#!/user/bin/python3

"""recreate a BaseModel from another one by using a dictionary representation
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """serializes instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id."""
        class_nm = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(class_nm, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file."""
        odict = FileStorage.__objects
        obj_dict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file"""
        try:
            with open(FileStorage.__file_path) as f:
                obj_dict = json.load(f)
                for o in obj_dict.values():
                    class_nm = o["__class__"]
                    del o["__class__"]
                    self.new(eval(class_nm)(**o))
        except FileNotFoundError:
            return
