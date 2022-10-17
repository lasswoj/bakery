from flask import Flask, request, make_response
from http import HTTPStatus
import uuid
from src.db import add_item, setup_envvar_engine, setup_session
from src.logger import rootLogger

app = Flask(__name__)

engine = setup_envvar_engine()

class InvalidRequest(Exception):
    pass


def validate_request(r_json: dict) -> bool:
    if not isinstance(r_json, dict):
        rootLogger.error("no json found in request")
        return False
    if not str(r_json.get("external_id", "")):
        rootLogger.error("no required parameter'external_id'")
        return False
    try:
        str(r_json["external_id"])
        str(r_json["name"])
        int(r_json["value"])
    except Exception as e:
        rootLogger.error(f"schema check failed {r_json} with exception:{e}")
        return False
    return True


@app.route("/item", methods=["POST"])
def post():
    res = make_response("", HTTPStatus.NO_CONTENT)
    try:
        r_json = request.json
        rootLogger.debug(f"item {r_json} processing")
        cookie_dict = request.cookies.to_dict()
        cart_id = cookie_dict.get("cart_id", "")
        if not cart_id:
            cart_id = str(uuid.uuid1())
        res.set_cookie(key="cart_id", value=cart_id, max_age=259200)
        if validate_request(r_json):
            with setup_session(engine).begin() as session:
                add_item(cart_id, r_json, session)
                rootLogger.info(f"item {r_json} added")
    except Exception as e:
        rootLogger.error(e)
    return res


if __name__ == "__main__":
    app.run(debug=True)
