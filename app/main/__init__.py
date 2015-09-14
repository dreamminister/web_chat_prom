from flask import Blueprint
# create main app blueprint
main = Blueprint('main', __name__)
# attach routes and custom error pages
from . import views, errors, events