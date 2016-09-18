import decor

from flask import Blueprint, redirect, request, url_for, g

import time

import os, json

def construct_bp(clothes, logger):

    ALLOWED_ORIGIN = "*"
    JSON_DENT = 4
    wrd_api = Blueprint('wrd_api', __name__, url_prefix="/wardrobe")

    @wrd_api.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


    # Returns number of pages
    @wrd_api.route("/pamount", methods=['GET', 'OPTIONS'])
    @decor.crossdomain(origin=ALLOWED_ORIGIN)
    def wrd_p_amount():
        return json.dumps(clothes.page_count(8), indent=JSON_DENT)

    # Returns Wardrobe items page
    @wrd_api.route("/get", methods=['GET', 'OPTIONS'])
    @decor.crossdomain(origin=ALLOWED_ORIGIN)
    def wrd_get():
        rsp = json.dumps(clothes.get(int(request.args.get("items")), int(request.args.get("page"))), indent=JSON_DENT)
        logger.debug("Execution %s", g.request_time())
        return rsp


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


    # Get item by id
    @wrd_api.route("/get/item/<int:id>", methods=['GET', 'OPTIONS'])
    @decor.crossdomain(origin=ALLOWED_ORIGIN)
    def wrd_get_item(id):
        return json.dumps(clothes.get_item(id), indent=JSON_DENT)

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

        logger.debug(tags)

        return json.dumps( clothes.add_tags(c_id, tags['tags']), indent=JSON_DENT)
    #edit dresscode
    @wrd_api.route("/add/dresscode/<int:c_id>", methods=['POST', 'OPTIONS'])
    @decor.crossdomain(origin=ALLOWED_ORIGIN)
    def wrd_dresscode(c_id):
        dresscode = json.loads(request.data)

        logger.debug(dresscode)

        return json.dumps( clothes.edit_dresscode(c_id, dresscode['dresscode']), indent=JSON_DENT)

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

    return wrd_api
