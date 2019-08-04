from flask import Blueprint, request as req, Response as res, json
from Test.table import TestTable
import os

CreateTestApp = Blueprint("create_test", __name__)

@CreateTestApp.route("",methods=["POST"])
def CreateTest():
    print(req.json)
    res_code = TestTable.insert(req.json)
    if(res_code == -1):
        response = res(json.dumps({"message":"Error"}), status=500, mimetype="application/json")
    elif(res_code == -2):
        response = res(json.dumps({"message":"Duplicate"}), status=409, mimetype="application/json")
    else:
        os.makedirs('./Tests/{}'.format(req.json.get('name')))
        response = res(json.dumps({"message":"Success"}), status=200, mimetype="application/json")
    return response
    