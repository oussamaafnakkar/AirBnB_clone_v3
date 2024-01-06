#!/usr/bin/python3
"""
Initializes the blueprint instance for the RESTful API views
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import your new view
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_amenities import  # Add this line to import the new view

__all__ = ['app_views']

