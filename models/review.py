#!/usr/bin/python
"""
Review Module

This module defines the Review class, which represents a review with attributes such as 
commentor_user_id, place_id, rating, feedback, created_at, and updated_at. The class includes 
methods for initializing, saving to a JSON file, and setting attribute values with validation.
"""

from datetime import datetime
import uuid
from data import user_data, place_data


class Review():
    """Representation of Review """

    def __init__(self, *_args, **kwargs):
        """
        Initializes a new Review instance with a unique ID, timestamps,
        and optional attributes.

        Args:
            *args: Variable length argument list (not used).
            **kwargs: Arbitrary keyword arguments for setting specific attributes.
        """

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = datetime.now().timestamp()
        self.__commentor_user_id = ""
        self.__place_id = ""
        self.__feedback = ""
        self.__rating = 0

        if kwargs:
            for key, value in kwargs.items():
                if key in ["commentor_user_id", "place_id", "rating", "feedback"]:
                    setattr(self, key, value)

    @property
    def feedback(self):
        """str: The feedback of the review."""
        return self.__feedback

    @feedback.setter
    def feedback(self, value):
        if isinstance(value, str):
            self.__feedback = value
        else:
            raise ValueError(f"Invalid feedback specified: {value}")

    @property
    def rating(self):
        """int: The rating of the review, between 1 and 5."""
        return self.__rating

    @rating.setter
    def rating(self, value):
        if isinstance(value, int) and 1 <= value <= 5:
            self.__rating = value
        else:
            raise ValueError(f"Invalid rating specified: {value}")

    @property
    def commentor_user_id(self):
        """str: The ID of the user who made the comment."""
        return self.__commentor_user_id

    @commentor_user_id.setter
    def commentor_user_id(self, value):
        if isinstance(value, str) and value in user_data:
            self.__commentor_user_id = value
        else:
            raise ValueError(f"Invalid commentor_user_id specified: {value}")

    @property
    def place_id(self):
        """str: The ID of the place being reviewed."""
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        if isinstance(value, str) and value in place_data:
            self.__place_id = value
        else:
            raise ValueError(f"Invalid place_id specified: {value}")
