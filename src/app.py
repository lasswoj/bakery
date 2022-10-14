from flask import Flask, request, make_response
from http import HTTPStatus
import uuid
from src.db import add_item, setup_envvar_engine, setup_session
import os
import logging

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
rootLogger = logging.getLogger()

logPath = os.getenv("logPath", "logs")
fileName = os.getenv("fileName", "logs")
fileHandler = logging.FileHandler(f"{logPath}/{fileName}.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
app = Flask(__name__)


# cool logic i will use later
#
# def deserialise_cookie(cookie:str) -> dict:
#     if not cookie:
#         return None
#     byte_cookie = cookie.encode()
#     pickled_cookie = binascii.unhexlify(byte_cookie)
#     return pickle.loads(pickled_cookie)

# def serialise_cookie(cookie_dict:dict) -> str:
#     pickled_cookie = pickle.dumps(cookie_dict)
#     byte_cookie = binascii.hexlify(pickled_cookie)
#     return byte_cookie.decode()


class InvalidRequest(Exception):
    pass


def validate_request(r_json) -> None:
    if not isinstance(r_json, dict):
        return "no json found in request", HTTPStatus.BAD_REQUEST
    if not r_json.get("external_id"):
        return "no required parameter'external_id'", HTTPStatus.BAD_REQUEST
    return None, None


@app.route("/item", methods=["POST"])
def post():
    res = make_response("", HTTPStatus.NO_CONTENT)
    try:
        r_json = request.json
        err_str, err_code = validate_request(r_json)
        if err_str:
            return err_str, err_code
        cookie_dict = request.cookies.to_dict()
        cart_id = cookie_dict.get("cart_id", "")
        if not cart_id:
            cart_id = str(uuid.uuid1())
        add_item(cart_id, r_json, setup_session(setup_envvar_engine()))
        res.set_cookie(key="cart_id", value=cart_id, max_age=259200)
    except Exception as e:
        rootLogger.error(e)
    return res


if __name__ == "__main__":
    app.run(debug=True)
