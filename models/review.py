#!/usr/bin/python

from datetime import datetime
import uuid
import re
import json
from data import review_data, user_data, place_data
from data.file_storage import FileStorage

storage = FileStorage()

class Review():
    """Representation of Review """

    def __init__(self, *args, **kwargs):
        """ constructor """

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

        # Automatically save review_data when a new review is created
        self.save()

    def save(self):
        review_entry = {
            'id': self.id,
            'commentor_user_id': self.commentor_user_id,
            'place_id': self.place_id,
            'rating': self.rating,
            'feedback': self.feedback,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        file_path = 'data/review.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            data['Review'].append(review_entry)
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True  # Indicate success
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving review entry: {e}")
            return False  # Indicate failure
    
    @property
    def feedback(self):
        return self.__feedback
    
    @feedback.setter
    def feedback(self, value):
        if isinstance(value, str):
            self.__feedback = value
        else:
            raise ValueError("Invalid feedback specified: {}".format(value))

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if isinstance(value, int) and 1 <= value <= 5:
            self.__rating = value
        else:
            raise ValueError("Invalid rating specified: {}".format(value))

    @property
    def commentor_user_id(self):
        return self.__commentor_user_id

    @commentor_user_id.setter
    def commentor_user_id(self, value):
        if isinstance(value, str) and value in user_data:
            self.__commentor_user_id = value
        else:
            raise ValueError("Invalid commentor_user_id specified: {}".format(value))

    @property
    def place_id(self):
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        if isinstance(value, str) and value in place_data:
            self.__place_id = value
        else:
            raise ValueError("Invalid place_id specified: {}".format(value))
    
