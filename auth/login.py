from flask import Blueprint, request as req, Response as res, json, make_response, after_this_request
from auth.users import Users
import jwt
import time, datetime

loginApp = Blueprint("login", __name__)

@loginApp.route("",methods=["POST"])
def signup():
    print(req.json)
    body = req.json
    rows = Users.findAll({
        'where':{
            'regno':body['regno']
        }
    })
    print(rows)
    if(len(rows) == 0):
        response = res(json.dumps({"message":"User does not exists"}), status=403, mimetype="application/json")
    elif(body['password'] == rows[0][6]):
        payload = req.json.copy()
        payload['timestamp'] = str(time.time())
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=180000)
        token = jwt.encode(payload, "srimanakulavinayagarengineeringcollege-vikram-dl", algorithm='HS256').decode("utf-8") 
        response = res(json.dumps({"message":"Success", "user": rows[0][:-1], 'token':token}), status=200, mimetype="application/json")
        response.set_cookie("token", token, domain="172.20.10.6:*")
    else:
        response = res(json.dumps({"message":"Unauthorized"}), status=403, mimetype="application/json")
    return response