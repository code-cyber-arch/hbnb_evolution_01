#!/usr/bin/python
"""
City Module

This module defines the City class, representing a city with attributes such as
name and country_id. It includes functionality to save city data to a JSON file.
"""

from datetime import datetime
import uuid
import re
import json
from data import country_data


class City():
    """Representation of city """

    def __init__(self, *_args, **kwargs):
        """ constructor """
        # super().__init__(*args, **kwargs)

        # defaults
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__name = ""
        self.__country_id = ""

        # Only allow country_id, name.
        # Note that setattr will call the setters for these 2 attribs
        if kwargs:
            for key, value in kwargs.items():
                if key == "country_id" or key == "name":
                    setattr(self, key, value)
        self.save()

    def save(self):
        """
        Save the city data to 'data/city.json'.
        
        Returns:
            bool: True if the city was successfully saved, False otherwise.
        """
        city_entry = {
            'id': self.id,
            'name': self.name,
            'country_id': self.country_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        file_path = 'data/city.json'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
            data['City'].append(city_entry)
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return True  # Indicate success
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving city entry: {e}")
            return False  # Indicate failure

    @property
    def name(self):
        """Getter for private prop name"""
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for private prop name"""

        # ensure that the value is not spaces-only and is alphabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value)
        if is_valid_name:
            self.__name = value
        else:
            raise ValueError(f"Invalid city name specified: {value}")

    @property
    def country_id(self):
        """Getter for private prop country_id"""
        return self.__country_id

    @country_id.setter
    def country_id(self, value):
        """Setter for private prop country_id"""

        # ensure that the specified country id actually exists before setting
        if country_data.get(value) is not None:
            self.__country_id = value
        else:
            raise ValueError(f"Invalid country_id specified: {value}")
