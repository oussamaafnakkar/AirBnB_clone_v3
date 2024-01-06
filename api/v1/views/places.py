#!/usr/bin/python3

""" Module for handling Place objects that handles all default RestFul API actions """

from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from flasgger.utils import swag_from
import json


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place_search/post_place_search.yml', methods=['POST'])
def places_search():
    """
    Search for places based on the JSON in the request body
    """
    try:
        data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places_result = []

    if not states and not cities and not amenities:
        # If all lists are empty, retrieve all Place objects
        places_result = [place.to_dict() for place in storage.all(Place).values()]
    else:
        # If states list is not empty
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    cities += [city.id for city in state.cities]

        # Include all cities individually in cities list
        cities += [city_id for city_id in cities if city_id not in storage.all(City)]

        # Retrieve places based on states and cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places_result += [place.to_dict() for place in city.places]

    # If amenities list is not empty
    if amenities:
        amenities_set = set(amenities)
        places_result = [place for place in places_result if amenities_set.issubset(set(place['amenities']))]

    return jsonify(places_result)


if __name__ == "__main__":
    pass

