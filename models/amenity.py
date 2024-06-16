#!/usr/bin/python
"""
Amenity Module

This module defines the Amenity class, representing an amenity with attributes such as
name. It includes functionality to save amenity data to a JSON file.
"""

from datetime import datetime
import uuid
import json


class Amenity:
    """Representation of an Amenity"""

    def __init__(self, *_args, **kwargs):
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
        self.save()

    def save(self):
        """
        Save the amenity data to 'data/amenity.json'.
        
        Returns:
            bool: True if the amenity was successfully saved, False otherwise.
        """
        amenity_entry = {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        file_path = 'data/amenity.json'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
            data['Amenity'].append(amenity_entry)
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving amenity entry: {e}")
            return False

    @property
    def name(self):
        """Get or set the amenity's name."""
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self.__name = value
        else:
            raise ValueError(f"Invalid name specified: {value}")
