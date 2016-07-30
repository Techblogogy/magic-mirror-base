import decor

from flask import Blueprint, redirect, request, url_for
from cvison.store import clothes

# from cvison.cam import My_Cam

import os, json

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
wrd_api = Blueprint('wrd_api', __name__, url_prefix="/wardrobe")

# Returns Wardrobe items page
@wrd_api.route("/get", methods=['GET', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_get():
    return json.dumps(clothes.get(int(request.args.get("items")), int(request.args.get("page"))), indent=JSON_DENT)


# NOTE: Returns smartly wardrobe items page
@wrd_api.route("/get/smart", methods=['GET', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_get_smart():
    return json.dumps(clothes.get_smart(request.args.get("q"), int(request.args.get("items")), int(request.args.get("page"))), indent=JSON_DENT)

# Returns all of the wardrobe items
@wrd_api.route("/get/all", methods=['GET', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_get_all():
    return json.dumps(clothes.get_all(), indent=JSON_DENT)

# Returns wardrobe items meta tags
@wrd_api.route("/get/meta", methods=['GET', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_get_meta():
    return json.dumps(clothes.get_meta(), indent=JSON_DENT)


# Starts camera thumbnail and video recording sequence and saves stuff to database
@wrd_api.route("/add", methods=['POST', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_add():
    #TODO: Camera take a picture and return path and dresscode

    print "[DEBUG wdobe]: Add request"
    fl = 0 #My_Cam.rec()
    clothes.add("casual", fl+".jpg")

    return ""

# Generates random testing data
@wrd_api.route("/add/test", methods=['POST', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_add_test():
    # print request.form.get("tags")
    return json.dumps( clothes.fill_junk(), indent=JSON_DENT)

# Adds tag to wardrobe item
@wrd_api.route("/add/tags/<int:c_id>", methods=['POST', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_add_tags(c_id):
    tags = json.loads(request.data)
    return json.dumps( clothes.add_tags(c_id, tags['tags']), indent=JSON_DENT)

# Mark clothes as worn
@wrd_api.route("/wear/<int:c_id>", methods=['POST', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_worn(c_id):
    return json.dumps(clothes.worn(c_id), indent=JSON_DENT)

# Like clothes item
@wrd_api.route("/like/<int:c_id>", methods=['POST', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_like(c_id):
    return json.dumps(clothes.like(c_id), indent=JSON_DENT)
