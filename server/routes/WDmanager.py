import decor

from flask import Blueprint, redirect, request, url_for, render_template
from cvison.store import clothes

from blogger import Blogger as bl

import os, json

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
wd_manager_api = Blueprint('wd_manager_api', __name__, url_prefix="/manager")

# Returns Wardrobe items page

@wd_manager_api.route('/')
def wardrobe_manager():
    print request.args.get("id")

    if request.args.get('action') == "delete":
        clothes.delete(request.args.get("id"))

    return (render_template('wardrobe.html', items = clothes.get(24,0)))
#
# @wd_manager_api.route('/')
# def smthr():



@wd_manager_api.route("/get", methods=['GET', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_wrd_get():
    return json.dumps(clothes.get(int(request.args.get("items")), int(request.args.get("page"))), indent=JSON_DENT)
