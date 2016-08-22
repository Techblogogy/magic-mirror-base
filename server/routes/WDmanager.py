
import decor

from flask import Blueprint, redirect, request, url_for, render_template
from cvison.store import clothes

import os, json

import logging
logger = logging.getLogger("TB")

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
wd_manager_api = Blueprint('wd_manager_api', __name__, url_prefix="/manager")

# Returns Wardrobe items page
page_counter = 0
@wd_manager_api.route('/')
def wardrobe_manager():
    global page_counter

    logger.debug(request.args.get("id"))

    if request.args.get('action') == "delete":
        clothes.delete(request.args.get("id"))
    if request.args.get('action') == "nextpage":
        if page_counter < clothes.page_count(24) - 1 :
           page_counter += 1
           print page_counter
    if request.args.get('action') == "prevpage":
        if page_counter > 0:
           page_counter -= 1


    return (render_template('wardrobe.html', items = clothes.get(24,page_counter), page_counter = page_counter))
    

@wd_manager_api.route("/get", methods=['GET', 'OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def wrd_wrd_get():
    return json.dumps(clothes.get(int(request.args.get("items")), int(request.args.get("page"))), indent=JSON_DENT)
