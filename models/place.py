#!/usr/bin/python
"""
Place Module

Defines the Place class representing a rental property with various attributes.
"""

from datetime import datetime
import uuid
import re
import json

class Place():
    """Representation of place """

    def __init__(self, *_args, **kwargs):
        """
        Initialize a new Place instance.

        Args:
            *_args: Variable length argument list (not used).
            **kwargs: Arbitrary keyword arguments for setting attributes.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = datetime.now().timestamp()
        self.__name = ""
        self.__description = ""
        self.__address = ""
        self.__latitude = 0.0
        self.__longitude = 0.0
        self.__number_of_rooms = 0
        self.__bathrooms = 0
        self.__price_per_night = 0.0
        self.__max_guests = 0
        self.city_id = ""
        self.host_user_id = ""
        self.amenities = []

        for key, value in kwargs.items():
            if key in ["name", "description", "address", "latitude", "longitude",
                       "number_of_rooms", "bathrooms", "price_per_night", 
                       "max_guests", "city_id", "host_user_id", "amenities"]:
                setattr(self, key, value)
        self.save()

    def save(self):
        """
        Save the pace data to 'data/place.json'.
        
        Returns:
            bool: True if the place was successfully saved, False otherwise.
        """
        place_entry = {
            "id": self.id,
            "host_user_id": self.host_user_id,
            "city_id": self.city_id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "number_of_rooms": self.number_of_rooms,
            "bathrooms": self.bathrooms,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        file_path = 'data/place.json'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
            data['Place'].append(place_entry)
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving place entry: {e}")
            return False

    @property
    def name(self):
        """str: The name of the place."""
        return self.__name

    @name.setter
    def name(self, value):
        """Set the name of the place."""
        if len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value):
            self.__name = value
        else:
            raise ValueError(f"Invalid place name specified: {value}")

    @property
    def description(self):
        """str: The description of the place."""
        return self.__description

    @description.setter
    def description(self, value):
        """Set the description of the place."""
        if isinstance(value, str):
            self.__description = value
        else:
            raise ValueError(f"Invalid description specified: {value}")

    @property
    def address(self):
        """str: The address of the place."""
        return self.__address

    @address.setter
    def address(self, value):
        """Set the address of the place."""
        if isinstance(value, str):
            self.__address = value
        else:
            raise ValueError(f"Invalid address specified: {value}")

    @property
    def latitude(self):
        """float: The latitude of the place."""
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Set the latitude of the place."""
        if isinstance(value, (int, float)) and -90 <= value <= 90:
            self.__latitude = value
        else:
            raise ValueError(f"Invalid latitude specified: {value}")

    @property
    def longitude(self):
        """float: The longitude of the place."""
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Set the longitude of the place."""
        if isinstance(value, (int, float)) and -180 <= value <= 180:
            self.__longitude = value
        else:
            raise ValueError(f"Invalid longitude specified: {value}")

    @property
    def number_of_rooms(self):
        """int: The number of rooms in the place."""
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        """Set the number of rooms in the place."""
        if isinstance(value, int) and value > 0:
            self.__number_of_rooms = value
        else:
            raise ValueError(f"Invalid number of rooms specified: {value}")

    @property
    def bathrooms(self):
        """int: The number of bathrooms in the place."""
        return self.__bathrooms

    @bathrooms.setter
    def bathrooms(self, value):
        """Set the number of bathrooms in the place."""
        if isinstance(value, int) and value > 0:
            self.__bathrooms = value
        else:
            raise ValueError(f"Invalid number of bathrooms specified: {value}")

    @property
    def price_per_night(self):
        """float: The price per night to stay at the place."""
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        """Set the price per night."""
        if isinstance(value, (int, float)) and value >= 0:
            self.__price_per_night = value
        else:
            raise ValueError(f"Invalid price per night specified: {value}")

    @property
    def max_guests(self):
        """int: The maximum number of guests."""
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, value):
        """Set the maximum number of guests."""
        if isinstance(value, int) and value > 0:
            self.__max_guests = value
        else:
            raise ValueError(f"Invalid number of max guests specified: {value}")
