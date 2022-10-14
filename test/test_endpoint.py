import pickle
import requests
import binascii

s = requests.Session() 
# all cookies received will be stored in the session object


def test_endpoint():
    res = s.post('http://127.0.0.1:5000/item', json={
        "external_id":1,
        "name":"item",
        "value":1,
        })
    if res.ok:
        print(s.cookies)
    res = s.post('http://127.0.0.1:5000/item', json={
        "external_id":2,
        "name":"item",
        "value":12,
        }, cookies=s.cookies)
    res = s.post('http://127.0.0.1:5000/item', json={
        "external_id":2,
        "name":"item",
        "value":12,
        })
    res = s.post('http://127.0.0.1:5000/item', json={
        "external_id":2,
        "name":"item",
        "value":12,
        }, cookies=s.cookies)
