#!/usr/bin/python3

from datetime import datetime
from flask import Flask, jsonify, request, abort
from models.city import City
from models.country import Country
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from data import country_data, place_data, amenity_data, place_to_amenity_data, review_data, user_data, city_data

app = Flask(__name__)

@app.route('/')
def hello_world():
    """ Hello world """
    return 'Hello World'

@app.route('/', methods=["POST"])
def hello_world_post():
    """ Hello world endpoint for POST requests """
    # curl -X POST localhost:5000/
    return "hello world\n"


# Examples
@app.route('/example/country_data')
def example_country_data():
    """ Example to show that we can view data loaded in the data module's init """
    return jsonify(country_data)

@app.route('/example/cities')
def example_cities():
    """ Example route to showing usage of the City model class """

    # We will be appending dictionaries to the list instead of City objects
    # This is so we can print them out on the webpage
    # If there is no need to display the data, we can consider storing the City objects themselves
    cities_list = []

    # the 'hello' and 'world' params below will be filtered off in City constructor
    cities_list.append(City(name="Gotham", hello="hello").__dict__)
    cities_list.append(City(name="Metropolis", world="world").__dict__)

    # Validation: The city with the invalid name is not appended to the list
    try:
        cities_list.append(City(name="#$%^&**", country_id=2).__dict__)
    except ValueError as exc:
        # This is printed internally in the server output. Not shown on website.
        print("City creation Error - ", exc)

    # Validation: The city with the invalid country_id is not appended to the list
    try:
        cities_list.append(City(name="Duckburg", country_id=1234).__dict__)
    except ValueError as exc:
        print("City creation Error - ", exc)

    # Note that private attributes have a weird key format. e.g. "_City__country_id"
    # This shows that the output of the City object's built-in __dict__ is not usable as-is

    return cities_list

@app.route('/example/places_amenties_raw')
def example_places_amenities_raw():
    """ Prints out the raw data for relationships between places and their amenities """
    return jsonify(place_to_amenity_data)

@app.route('/example/places_amenties_prettified_example')
def example_places_amenties_prettified():
    """ Prints out the relationships between places and their amenities using names """

    output = {}

    for place_key in place_to_amenity_data:
        place_name = place_data[place_key]['name']
        if place_name not in output:
            output[place_name] = []

        amenities_ids = place_to_amenity_data[place_key]
        for amenity_key in amenities_ids:
            amenity_name = amenity_data[amenity_key]['name']
            output[place_name].append(amenity_name)

    return jsonify(output)

@app.route('/example/places_reviews')
def example_places_reviews():
    """ prints out reviews of places """

    output = {}

    for key in review_data:
        row = review_data[key]
        place_id = row['place_id']
        place_name = place_data[place_id]['name']
        if place_name not in output:
            output[place_name] = []
        
        reviewer = user_data[row['commentor_user_id']]

        output[place_name].append({
            "review": row['feedback'],
            "rating": str(row['rating'] * 5) + " / 5",
            "reviewer": reviewer['first_name'] + " " + reviewer['last_name']
        })

    return jsonify(output)

# Consider adding other test routes to display data for:
# - the places within the countries
# - which places are owned by which users
# - names of the owners of places with toilets

# --- API endpoints ---
# --- USER ---
@app.route('/api/v1/users', methods=["GET"])
def users_get():
    """returns Users"""
    data = []

    for k, v in user_data.items():
        data.append({
            "id": v['id'],
            "first_name": v['first_name'],
            "last_name": v['last_name'],
            "email": v['email'],
            "password": v['password'],
            "created_at": datetime.fromtimestamp(v['created_at']),
            "updated_at": datetime.fromtimestamp(v['updated_at'])
        })

    return jsonify(data)

@app.route('/api/v1/users/<user_id>', methods=["GET"])
def users_specific_get(user_id):
    """returns specified user"""
    data = []

    if user_id not in user_data:
        # raise IndexError("User not found!")
        return "User not found!"

    v = user_data[user_id]
    data.append({
        "id": v['id'],
        "first_name": v['first_name'],
        "last_name": v['last_name'],
        "email": v['email'],
        "password": v['password'],
        "created_at": datetime.fromtimestamp(v['created_at']),
        "updated_at": datetime.fromtimestamp(v['updated_at'])
    })
    return jsonify(data)

@app.route('/api/v1/users', methods=["POST"])
def users_post():
    """ posts data for new user then returns the user data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # print(request.content_type)

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    try:
        u = User(first_name=data["first_name"],last_name=data["last_name"], email=data["email"], password=data["password"])
    except ValueError as exc:
        return repr(exc) + "\n"

    # add new user data to user_data
    # note that the created_at and updated_at are using timestamps
    user_data[u.id] = {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "created_at": u.created_at,
        "updated_at": u.updated_at
    }

    # note that the created_at and updated_at are using readable datetimes
    attribs = {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "created_at": datetime.fromtimestamp(u.created_at),
        "updated_at": datetime.fromtimestamp(u.updated_at)
    }

    return jsonify(attribs)

@app.route('/api/v1/users/<user_id>', methods=["PUT"])
def users_put(user_id):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()

    if user_id not in user_data:
        abort(400, "User not found for id {}".format(user_id))

    u = user_data[user_id]

    # modify the values
    for k, v in data.items():
        # only first_name and last_name are allowed to be modified
        if k in ["first_name", "last_name"]:
            u[k] = v

    # update user_data with the new name - print user_data out to confirm it if you want
    user_data[user_id] = u

    attribs = {
        "id": u["id"],
        "first_name": u["first_name"],
        "last_name": u["last_name"],
        "email": u["email"],
        "created_at": datetime.fromtimestamp(u["created_at"]),
        "updated_at": datetime.fromtimestamp(u["updated_at"])
    }

    # print out the updated user details
    return jsonify(attribs)


@app.route('/api/v1/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    """ deletes an existing user using specified id """
    # Check if the user exists
    if user_id not in user_data:
        abort(404, "User not found for id {}".format(user_id))

    # Remove the user from the data store
    del user_data[user_id]

    # Return a 204 No Content response to indicate successful deletion
    return '', 204



# --- COUNTRY ---
@app.route('/api/v1/countries', methods=["POST"])
def countries_post():
    """ posts data for new country then returns the country data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    if 'code' not in data:
        abort(400, "Missing country code")

    try:
        c = Country(name=data["name"],code=data["code"])
    except ValueError as exc:
        return repr(exc) + "\n"

    # add new user data to user_data
    # note that the created_at and updated_at are using timestamps
    country_data[c.id] = {
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at": c.created_at,
        "updated_at": c.updated_at
    }

    # note that the created_at and updated_at are using readable datetimes
    attribs = {
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at": datetime.fromtimestamp(c.created_at),
        "updated_at": datetime.fromtimestamp(c.updated_at)
    }

    return jsonify(attribs)

@app.route('/api/v1/countries', methods=["GET"])
def countries_get():
    """ returns countires data """
    data = []

    for k, v in country_data.items():
        data.append({
            "id": v['id'],
            "name": v['name'],
            "code": v['code'],
            "created_at": datetime.fromtimestamp(v['created_at']),
            "updated_at": datetime.fromtimestamp(v['updated_at'])
        })

    return jsonify(data)

@app.route('/api/v1/countries/<country_code>', methods=["GET"])
def countries_specific_get(country_code):
    """ returns specific country data """
    for k, v in country_data.items():
        if v['code'] == country_code:
            data = v

    c = {
        "id": data['id'],
        "name": data['name'],
        "code": data['code'],
        "created_at": datetime.fromtimestamp(data['created_at']),
        "updated_at": datetime.fromtimestamp(data['updated_at'])
    }

    return jsonify(c)

@app.route('/api/v1/countries/<country_code>', methods=["PUT"])
def countries_put(country_code):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    c = {}

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    for k, v in country_data.items():
        if v['code'] == country_code:
            c = v

    if not c:
        abort(400, "Country not found for code {}".format(country_code))

    # modify the values
    # only name is allowed to be modified
    for k, v in data.items():
        if k in ["name"]:
            c[k] = v

    # update country_data with the new name - print country_data out to confirm it if you want
    country_data[c['id']] = c

    attribs = {
        "id": c["id"],
        "name": c["name"],
        "code": c["code"],
        "created_at": datetime.fromtimestamp(c["created_at"]),
        "updated_at": datetime.fromtimestamp(c["updated_at"])
    }

    # print out the updated user details
    return jsonify(attribs)

@app.route('/api/v1/countries/<country_code>/cities', methods=["GET"])
def countries_specific_cities_get(country_code):
    """ returns cities data of specified country """
    data = []
    wanted_country_id = ""

    for k, v in country_data.items():
        if v['code'] == country_code:
            wanted_country_id = v['id']

    for k, v in city_data.items():
        if v['country_id'] == wanted_country_id:
            data.append({
                "id": v['id'],
                "name": v['name'],
                "country_id": v['country_id'],
                "created_at": datetime.fromtimestamp(v['created_at']),
                "updated_at": datetime.fromtimestamp(v['updated_at'])
            })

    return jsonify(data)

# Create the rest of the endpoints for:
#  - City
#  - Amenity
#  - Place
#  - Review







# --- CITY ---
@app.route('/api/v1/cities', methods=["GET"])
def cities_get():
    """returns Cities"""
    data = []

    for k, v in city_data.items():
        data.append({
            "id": v['id'],
            "name": v['name'],
            "country_id": v['country_id'],
            "created_at": datetime.fromtimestamp(v['created_at']),
            "updated_at": datetime.fromtimestamp(v['updated_at'])
        })

    return jsonify(data)

@app.route('/api/v1/cities/<city_id>', methods=["GET"])
def cities_specific_get(city_id):
    """returns specified city"""
    data = []

    if city_id not in city_data:
        return "City not found!"

    v = city_data[city_id]
    data.append({
        "id": v['id'],
        "name": v['name'],
        "country_id": v['country_id'],
        "created_at": datetime.fromtimestamp(v['created_at']),
        "updated_at": datetime.fromtimestamp(v['updated_at'])
    })
    return jsonify(data)


@app.route('/api/v1/cities', methods=["POST"])
def cities_post():
    """ Create a new city """
    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    if 'country_code' not in data:
        abort(400, "Missing country_code")

    # Validate country_code
    country_id = None
    for k, v in country_data.items():
        if v['code'] == data['country_code']:
            country_id = v['id']
            break

    if not country_id:
        abort(400, "Invalid country_code")

    # Ensure city names are unique within the same country
    for _, v in city_data.items():
        if v['country_id'] == country_id and v['name'] == data['name']:
            abort(409, "City name must be unique within the same country")

    try:
        # Create new city using the City class
        new_city = City(name=data["name"], country_id=country_id)
    except ValueError as exc:
        return repr(exc) + "\n"

    # Add new city data to city_data
    city_data[new_city.id] = {
        "id": new_city.id,
        "name": new_city.name,
        "country_id": new_city.country_id,
        "created_at": new_city.created_at,
        "updated_at": new_city.updated_at
    }

    return jsonify({
        "id": new_city.id,
        "name": new_city.name,
        "country_id": new_city.country_id,
        "created_at": datetime.fromtimestamp(new_city.created_at),
        "updated_at": datetime.fromtimestamp(new_city.updated_at)
    }), 201


@app.route('/api/v1/cities/<city_id>', methods=["PUT"])
def cities_put(city_id):
    """ Update an existing city’s information """
    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if city_id not in city_data:
        return jsonify({"message": "City not found"}), 404

    # Validate country_code
    country_id = None
    for k, v in country_data.items():
        if v['code'] == data['country_code']:
            country_id = v['id']
            break

    if not country_id:
        abort(400, "Invalid country_code")

    # Ensure city names are unique within the same country
    for _, v in city_data.items():
        if v['country_id'] == country_id and v['name'] == data['name'] and v['id'] != city_id:
            abort(409, "City name must be unique within the same country")

    city_data[city_id]['name'] = data['name']
    city_data[city_id]['country_id'] = country_id
    city_data[city_id]['updated_at'] = datetime.now().timestamp()

    return jsonify({
        "id": city_data[city_id]['id'],
        "name": city_data[city_id]['name'],
        "country_id": city_data[city_id]['country_id'],
        "created_at": datetime.fromtimestamp(city_data[city_id]['created_at']),
        "updated_at": datetime.fromtimestamp(city_data[city_id]['updated_at'])
    })


@app.route('/api/v1/cities/<city_id>', methods=["DELETE"])
def cities_delete(city_id):
    """ Delete a specific city """
    if city_id not in city_data:
        return jsonify({"message": "City not found"}), 404

    del city_data[city_id]
    return jsonify({"message": "City deleted successfully"}), 200



# --- AMENITY ---
@app.route('/api/v1/amenities', methods=["GET"])
def amenities_get():
    """returns Amenities"""
    data = []

    for k, v in amenity_data.items():
        data.append({
            "id": v['id'],
            "name": v['name'],
            "created_at": datetime.fromtimestamp(v['created_at']),
            "updated_at": datetime.fromtimestamp(v['updated_at'])
        })

    return jsonify(data)

@app.route('/api/v1/amenities/<amenity_id>', methods=["GET"])
def amenities_specific_get(amenity_id):
    """returns specified amenity"""
    data = []

    if amenity_id not in amenity_data:
        return "Amenity not found!"

    v = amenity_data[amenity_id]
    data.append({
        "id": v['id'],
        "name": v['name'],
        "created_at": datetime.fromtimestamp(v['created_at']),
        "updated_at": datetime.fromtimestamp(v['updated_at'])
    })
    return jsonify(data)


@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    if request.get_json() is None:
        abort(400, "Not a JSON")

    if amenity_id not in amenity_data:
        return jsonify({"message": "Amenity not found"}), 404

    data = request.get_json()
    if 'name' not in data or not data['name'].strip():
        abort(400, "Missing or empty name")

    # Ensure amenity name is unique
    for id, amenity in amenity_data.items():
        if amenity['name'] == data['name'] and id != amenity_id:
            abort(409, "Amenity name must be unique")

    amenity_data[amenity_id]['name'] = data['name']
    amenity_data[amenity_id]['updated_at'] = datetime.now().timestamp()

    return jsonify(amenity_data[amenity_id]), 200


@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    if amenity_id not in amenity_data:
        return jsonify({"message": "Amenity not found"}), 404

    del amenity_data[amenity_id]
    return '', 204


# --- PLACE ---
@app.route('/api/v1/places', methods=["GET"])
def places_get():
    """returns Places"""
    data = []

    for k, v in place_data.items():
        try:
            data.append({
                "id": v['id'],
                "name": v['name'],
                "city_id": v['city_id'],
                "price_per_night": v['price_per_night'],
                "max_guests": v['max_guests'],
                "created_at": datetime.fromtimestamp(v['created_at']),
                "updated_at": datetime.fromtimestamp(v['updated_at'])
            })
        except KeyError as e:
            print(f"KeyError: Missing key {e} in place data for place_id {k}")

    return jsonify(data)

@app.route('/api/v1/places/<place_id>', methods=["GET"])
def places_specific_get(place_id):
    """returns specified place"""
    data = []

    if place_id not in place_data:
        return "Place not found!"

    v = place_data[place_id]
    try:
        data.append({
            "id": v['id'],
            "name": v['name'],
            "city_id": v['city_id'],
            "price_per_night": v['price_per_night'],
            "max_guests": v['max_guests'],
            "created_at": datetime.fromtimestamp(v['created_at']),
            "updated_at": datetime.fromtimestamp(v['updated_at'])
        })
    except KeyError as e:
        print(f"KeyError: Missing key {e} in place data for place_id")
    return jsonify(data)


@app.route('/api/v1/places', methods=['POST'])
def create_place():
    """Create a new place"""
    data = request.get_json()

    if 'name' not in data:
        abort(400, "Missing name")
    if 'description' not in data:
        abort(400, "Missing description")
    if 'address' not in data:
        abort(400, "Missing address")
    if 'latitude' not in data:
        abort(400, "Missing latitude")
    if 'longitude' not in data:
        abort(400, "Missing longitude")
    if 'number_of_rooms' not in data:
        abort(400, "Missing number_of_rooms")
    if 'bathrooms' not in data:
        abort(400, "Missing bathrooms")
    if 'price_per_night' not in data:
        abort(400, "Missing price_per_night")
    if 'max_guests' not in data:
        abort(400, "Missing max_guests")
    if 'city_id' not in data:
        abort(400, "Missing city_id")
    if 'host_id' not in data:
        abort(400, "Missing host_id")
    if 'amenities' not in data:
        abort(400, "Missing amenity_ids")

    try:
        place = Place(name=data["name"],
                      description=data["description"],
                      address=data["address"],
                      latitude=data["latitude"],
                      longitude=data["longitude"],
                      number_of_rooms=data["number_of_rooms"],
                      bathrooms=data["bathrooms"],
                      price_per_night=data["price_per_night"],
                      max_guests=data["max_guests"],
                      city_id=data["city_id"],
                      host_id=data["host_id"],
                      amenities=data["amenities"])
        place_data[place.id] = place
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    return jsonify(place.__dict__), 201

@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    if place_id not in place_data:
        return jsonify({"message": "Place not found"}), 404

    place = place_data[place_id]

    data = request.get_json()
    if not data:
        abort(400, "No data provided")

    # Update the place attributes
    if 'name' in data:
        place.name = data['name']
    if 'description' in data:
        place.description = data['description']
    if 'address' in data:
        place.address = data['address']
    if 'latitude' in data:
        place.latitude = data['latitude']
    if 'longitude' in data:
        place.longitude = data['longitude']
    if 'number_of_rooms' in data:
        place.number_of_rooms = data['number_of_rooms']
    if 'bathrooms' in data:
        place.bathrooms = data['bathrooms']
    if 'price_per_night' in data:
        place.price_per_night = data['price_per_night']
    if 'max_guests' in data:
        place.max_guests = data['max_guests']
    if 'city_id' in data:
        place.city_id = data['city_id']
    if 'host_user_id' in data:
        place.host_user_id = data['host_user_id']
    if 'amenities' in data:
        place.amenities = data['amenities']

    # Update the timestamp
    place.updated_at = datetime.now().timestamp()

    # Return the updated place
    return jsonify({
        "id": place.id,
        "name": place.name,
        "description": place.description,
        "address": place.address,
        "latitude": place.latitud,
        "longitude": place.longitude,
        "number_of_rooms": place.number_of_rooms,
        "bathrooms": place.bathrooms,
        "price_per_night": place.price_per_night,
        "max_guests": place.max_guests,
        "city_id": place.city_id,
        "host_user_id": place.host_user_id,
        "amenities": place.amenities,
        "created_at": datetime.fromtimestamp(place.created_at),
        "updated_at": datetime.fromtimestamp(place.updated_at)
    }), 200


# --- REVIEW ---
@app.route('/api/v1/users/<user_id>/reviews', methods=["GET"])
def get_reviews_by_user(user_id):
    """Retrieve all reviews written by a specific user"""
    data = []

    if user_id not in user_data:
        return "User not found!"

    user_reviews = [review for review in review_data.values() if review['commentor_user_id'] == user_id]
    for review in user_reviews:
        try:
            data.append({
                "id": review['id'],
                "commentor_user_id": review['commentor_user_id'],
                "place_id": review['place_id'],
                "rating": review['rating'],
                "feedback": review['feedback'],
                "created_at": datetime.fromtimestamp(review['created_at']),
                "updated_at": datetime.fromtimestamp(review['updated_at'])
            })
        except KeyError as e:
            print(f"KeyError: Missing key {e} in review data for review_id {review['id']}")

    return jsonify(data)


@app.route('/api/v1/places/<place_id>/reviews', methods=["GET"])
def get_reviews_by_place(place_id):
    """Retrieve all reviews for a specific place"""
    data = []

    if place_id not in place_data:
        return jsonify({"message": "Place not found!"}), 404

    # Filter reviews to find those that match the given place_id
    place_reviews = [review for review in review_data.values() if review['place_id'] == place_id]

    for review in place_reviews:
        try:
            data.append({
                "id": review['id'],
                "commentor_user_id": review['commentor_user_id'],
                "place_id": review['place_id'],
                "rating": review['rating'],
                "feedback": review['feedback'],
                "created_at": datetime.fromtimestamp(review['created_at']),
                "updated_at": datetime.fromtimestamp(review['updated_at'])
            })
        except KeyError as e:
            print(f"KeyError: Missing key {e} in review data for review_id {review['id']}")

    return jsonify(data)

@app.route('/api/v1/reviews/<review_id>', methods=["GET"])
def get_review(review_id):
    """Retrieve detailed information about a specific review"""
    data = []

    if review_id not in review_data:
        return "Review not found!"

    review = review_data[review_id]
    try:
        data.append({
            "id": review['id'],
            "commentor_user_id": review['commentor_user_id'],
            "place_id": review['place_id'],
            "rating": review['rating'],
            "feedback": review['feedback'],
            "created_at": datetime.fromtimestamp(review['created_at']),
            "updated_at": datetime.fromtimestamp(review['updated_at'])
        })
    except KeyError as e:
        print(f"KeyError: Missing key {e} in review data for review_id {review['id']}")

    return jsonify(data)


@app.route('/api/v1/reviews/<review_id>', methods=["PUT"])
def update_review(review_id):
    """Update an existing review"""
    if review_id not in review_data:
        return jsonify({"message": "Review not found!"}), 404

    if request.get_json() is None:
        return jsonify({"message": "Not a JSON"}), 400

    data = request.get_json()
    
    review = review_data[review_id]

    # Update the review data
    try:
        if 'commentor_user_id' in data:
            review['commentor_user_id'] = data['commentor_user_id']
        if 'place_id' in data:
            review['place_id'] = data['place_id']
        if 'rating' in data:
            rating = data['rating']
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
            review['rating'] = rating
        if 'feedback' in data:
            review['feedback'] = data['feedback']
        
        review['updated_at'] = datetime.now().timestamp()
        
        return jsonify(review), 200
    except KeyError as e:
        return jsonify({"message": f"Missing key {e} in review data"}), 400
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/api/v1/reviews/<review_id>', methods=["DELETE"])
def delete_review(review_id):
    """Delete a specific review"""
    if review_id not in review_data:
        return jsonify({"message": "Review not found!"}), 404

    del review_data[review_id]
    return '', 204

@app.route('/api/v1/places/<place_id>/reviews', methods=["POST"])
def create_review(place_id):
    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'commentor_user_id' not in data:
        abort(400, "Missing commentor_user_id")
    if 'rating' not in data:
        abort(400, "Missing rating")
    if 'feedback' not in data or not data['feedback'].strip():
        abort(400, "Missing or empty feedback")
    if place_id not in place_data:
        abort(404, "Place not found")

    # Ensure commentor_user_id is valid
    if data['commentor_user_id'] not in user_data:
        abort(404, "User not found")

    # Create a new review
    try:
        review = Review(
            commentor_user_id=data['commentor_user_id'],
            place_id=place_id,
            rating=data['rating'],
            feedback=data['feedback']
        )
    except ValueError as exc:
        return repr(exc) + "\n"

    # Add the new review to review_data
    review_data[review.id] = {
        'id': review.id,
        'commentor_user_id': review.commentor_user_id,
        'place_id': review.place_id,
        'rating': review.rating,
        'feedback': review.feedback,
        'created_at': review.created_at,
        'updated_at': review.updated_at
    }

    return jsonify(review_data[review.id]), 201

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
