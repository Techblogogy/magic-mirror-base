import decor

from flask import Blueprint, redirect, request, url_for
from cvison.store import clothes

import os, json

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
wrd_api = Blueprint('wrd_api', __name__, url_prefix="/wardrobe")

# Returns Wardrobe items page
@wrd_api.route("/get")
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_get():
    return json.dumps(clothes.get(request.args.get("items"), request.args.get("page")))

# Returns all of the wardrobe items
@wrd_api.route("/get/all")
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_get_all():
    return json.dumps(clothes.get_all())


# Starts camera thumbnail and video recording sequence and saves stuff to database
@wrd_api.route("/add")
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_add():
    #TODO: Camera take a picture and return path and dresscode
    clothes.add("casual", "thum1.jpg")

    return ""
