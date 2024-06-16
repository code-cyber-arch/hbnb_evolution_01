#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb evolution"""

import json
from pathlib import Path

class FileStorage():
    """ Class for reading from files """

    def load_model_data(self, filename):
        """ Load JSON data from file and returns as dictionary """

        data = {}

        if not Path(filename).is_file():
            raise FileNotFoundError("Data file '{}' missing".format(filename))

        try:
            with open(filename, 'r') as f:
                rows = json.load(f)
            for key in rows:
                data[key] = rows[key]
        except ValueError as exc:
            raise ValueError("Unable to load data from file '{}'".format(filename)) from exc

        # The data at this point is not directly usable. It needs to be cleaned up
        data = self.reorganise_model_data(data)

        return data

    def reorganise_model_data(self, data):
        """ Parse and reorganise the data so that the id is the key """
        output = {}

        # To make it easier to look for certain ids in the loaded data
        # we are going to rebuild the dictionary so that the row id (uuid)
        # is also the key for the record

        for key in data:
            # key's value is 'Place', 'Country', etc. since the JSON's key is the model name
            # print("Rebuilding loaded data for {}...".format(key))
            # print(data[key])
            for row in data[key]:
                # now we interate inside the JSON data...
                output[row['id']] = row

        return output

    def load_many_to_many_data(self, filename):
        """ many to many data is loaded by this function """

        data = {}
        grouped_data = {}

        if not Path(filename).is_file():
            raise FileNotFoundError("Data file '{}' missing".format(filename))

        try:
            with open(filename, 'r') as f:
                rows = json.load(f)
            for key in rows:
                data[key] = rows[key]
        except ValueError as exc:
            raise ValueError("Unable to load data from file '{}'".format(filename)) from exc

        # print(data.items())

        for key in data:
            # key's value is 'Place_to_Amenity'
            for row in data[key]:
                place_id = row['place_id']
                amenity_id = row['amenity_id']

                if place_id not in grouped_data:
                    grouped_data[place_id] = []
                grouped_data[place_id].append(amenity_id)

        return grouped_data
    
    def save_model_data(self, filename, data):
        """Save data to JSON file"""

        try:
            with open(filename, 'a') as f:
                json.dump(data, f)
        except IOError as exc:
            raise IOError(f"Unable to save data to file '{filename}'") from exc

