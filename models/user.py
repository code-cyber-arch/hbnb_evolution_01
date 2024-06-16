#!/usr/bin/python
"""
User Module

This module defines the User class, representing a user with attributes such as
first name, last name, email, and password. It includes functionality to save
user data to a JSON file.
"""

from datetime import datetime
import uuid
import re
import json

class User():
    """Representation of user """

    def __init__(self, *_args, **kwargs):
        """ constructor """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__first_name = ""
        self.__last_name = ""
        self.__email = ""
        self.__password = ""

        # Only allow first_name, last_name, email, password.
        # Note that setattr will call the setters for these attribs
        if kwargs:
            for key, value in kwargs.items():
                if key == "first_name" or key == "last_name" or key == "email" or key == "password":
                    setattr(self, key, value)
        self.save()

    def save(self):
        """
        Save the user data to 'data/user.json'.
        
        Returns:
            bool: True if the user was successfully saved, False otherwise.
        """
        user_entry = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        file_path = 'data/user.json'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
            data['User'].append(user_entry)
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving review entry: {e}")
            return False

    @property
    def first_name(self):
        """Getter for private prop first_name"""
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """Setter for private prop first_name"""

        # ensure that the value is alphabets only
        # Note that this won't allow names like Obi-wan or Al'azif
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z]+$", value)
        if is_valid_name:
            self.__first_name = value
        else:
            raise ValueError(f"Invalid first name specified: {value}")

    @property
    def last_name(self):
        """Getter for private prop last_name"""
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """Setter for private prop last_name"""

        # ensure that the value is alphabets only
        # Note that this won't allow names like Obi-wan or Al'azif
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z]+$", value)
        if is_valid_name:
            self.__last_name = value
        else:
            raise ValueError(f"Invalid last name specified: {value}")

    @property
    def email(self):
        """Getter for private prop email"""
        return self.__email

    @email.setter
    def email(self, value):
        """Setter for private prop last_name"""

        # add a simple regex check for email format. Nothing too fancy.
        is_valid = len(value.strip()) > 0 and re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",value)
        if is_valid:
            self.__email = value
        else:
            raise ValueError(f"Invalid email specified: {value}")

    @property
    def password(self):
        """Getter for private prop email"""
        return self.__password

    @password.setter
    def password(self, value):
        """Setter for private prop email"""
        is_valid_password = len(value) >= 6
        if is_valid_password:
            self.__password = value
        else:
            raise ValueError("Password is too short! Min 6 characters required.")
