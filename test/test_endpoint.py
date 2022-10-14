import pickle
import requests
import binascii
from pytest import fixture 
from src.tables import Cart, Item

# all cookies received will be stored in the session object
from src.app import validate_request
from src.db import setup_engine, setup_session, setup_envvar_engine
from test.test_db import setup_psql, setup_eng



def test_valid():
    item = {
        "external_id": 1,
        "name": "item",
        "value": 1,
    }
    assert validate_request(item) == True
    item["value"]="bad"
    assert validate_request(item) == False
    item = {
        "external_id": [],
        "name": "item",
        "value": 1,
    }
    assert validate_request(item) == True
    item = {
        "external_id": "0",
        "name": "item",
        "value": 1,
    }
    assert validate_request(item) == True


def test_endpoint(setup_psql):
    s = requests.Session()
    s2 = requests.Session()
    res = s.post(
        "http://127.0.0.1:5000/item",
        json={"external_id": 1, "name": "item", "value": 1,},
    )
    assert res.ok
    res = s.post(
        "http://127.0.0.1:5000/item",
        json={"external_id": 2, "name": "item", "value": 12,},
    )
    assert res.ok
    res = s.post(
        "http://127.0.0.1:5000/item",
        json={"external_id": 2, "name": "item", "value": 12,},
    )
    assert res.ok
    res = s.post(
        "http://127.0.0.1:5000/item",
        json={"external_id": 2, "name": "item", "value": 12,},
    )
    res = s.post(
        "http://127.0.0.1:5000/item",
        json={"external_id": 2, "name": "item", "value": 12,},
    )
    assert res.ok
    with setup_psql.begin() as session:
        assert session.query(Item).count() == 2
        assert session.query(Cart).count() == 1
    res = s2.post(
        "http://127.0.0.1:5000/item",
        json={"external_id": 2, "name": "item", "value": 12,},
    )
    assert res.ok
    with setup_psql.begin() as session:
        assert session.query(Item).count() == 3
        assert session.query(Cart).count() == 2
    

    