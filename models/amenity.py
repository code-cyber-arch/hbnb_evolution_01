#!/usr/bin/python

from datetime import datetime
import uuid

class Amenity:
    """Representation of an Amenity"""

    def __init__(self, *args, **kwargs):
        """Constructor"""

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = datetime.now().timestamp()
        self.__name = ""

        # Set attributes from kwargs
        if kwargs:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self.__name = value
        else:
            raise ValueError("Invalid name specified: {}".format(value))