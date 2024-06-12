#!/usr/bin/python

from datetime import datetime
import uuid
import re
from data import user_data, city_data, amenity_data

class Place():
    """Representation of place """

    def __init__(self, *args, **kwargs):
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


    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value):
            self.__name = value
        else:
            raise ValueError("Invalid place name specified: {}".format(value))
    
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self.__description = value
        else:
            raise ValueError("Invalid description specified: {}".format(value))
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, value):
        if isinstance(value, str):
            self.__address = value
        else:
            raise ValueError("Invalid address specified: {}".format(value))
    
    @property
    def latitude(self):
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        if isinstance(value, (int, float)) and -90 <= value <= 90:
            self.__latitude = value
        else:
            raise ValueError("Invalid latitude specified: {}".format(value))
    
    @property
    def longitude(self):
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        if isinstance(value, (int, float)) and -180 <= value <= 180:
            self.__longitude = value
        else:
            raise ValueError("Invalid longitude specified: {}".format(value))
    
    @property
    def number_of_rooms(self):
        return self.__number_of_rooms
    
    @number_of_rooms.setter
    def number_of_rooms(self, value):
        if isinstance(value, int) and value > 0:
            self.__number_of_rooms = value
        else:
            raise ValueError("Invalid number of rooms specified: {}".format(value))
    
    @property
    def bathrooms(self):
        return self.__bathrooms
    
    @bathrooms.setter
    def bathrooms(self, value):
        if isinstance(value, int) and value > 0:
            self.__bathrooms = value
        else:
            raise ValueError("Invalid number of bathrooms specified: {}".format(value))
    
    @property
    def price_per_night(self):
        return self.__price_per_night
    
    @price_per_night.setter
    def price_per_night(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self.__price_per_night = value
        else:
            raise ValueError("Invalid price per night specified: {}".format(value))
    
    @property
    def max_guests(self):
        return self.__max_guests
    
    @max_guests.setter
    def max_guests(self, value):
        if isinstance(value, int) and value > 0:
            self.__max_guests = value
        else:
            raise ValueError("Invalid number of max guests specified: {}".format(value))
