#!/usr/bin/python
"""
Country Module

This module defines the Country class, representing a country with attributes such as
name and code. It includes functionality to save country data to a JSON file.
"""

from datetime import datetime
import uuid
import re
import json


class Country():
    """Representation of country """

    def __init__(self, *_args, **kwargs):
        """ constructor """
        # super().__init__(*args, **kwargs)

        # defaults
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__name = ""
        self.__code = ""

        # Only allow name, code.
        # Note that setattr will call the setters for these attribs
        if kwargs:
            for key, value in kwargs.items():
                if key == "name" or key == "code":
                    setattr(self, key, value)
        self.save()

    def save(self):
        """
        Save the country data to 'data/country.json'.
        
        Returns:
            bool: True if the country was successfully saved, False otherwise.
        """
        country_entry = {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        file_path = 'data/country.json'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
            data['Country'].append(country_entry)
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving country entry: {e}")
            return False

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
            raise ValueError(f"Invalid country name specified: {value}")

    @property
    def code(self):
        """Getter for private prop code"""
        return self.__code

    @code.setter
    def code(self, value):
        """Setter for private prop code"""

        # ensure that the value is not spaces-only and is two uppercase alphabets only
        is_valid_code = len(value.strip()) > 0 and re.search("^[A-Z][A-Z]$", value)
        if is_valid_code:
            self.__code = value
        else:
            raise ValueError(f"Invalid country code specified: {value}")
