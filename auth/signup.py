from flask import Blueprint, request as req, Response as res, json
from auth.users import Users
from init import Orm

signupApp = Blueprint("signup", __name__)

@signupApp.route("",methods=["POST"])
def signup():
    print(req.json)
    res_code = Users.insert(req.json)
    if(res_code == -1):
        response = res(json.dumps({"message":"Error"}), status=500, mimetype="application/json")
    elif(res_code == -2):
        response = res(json.dumps({"message":"Duplicate"}), status=409, mimetype="application/json")
    else:
        response = res(json.dumps({"message":"Success"}), status=200, mimetype="application/json")
    return response