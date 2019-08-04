from flask import Blueprint, request as req, Response as res, json
from Test.table import TestTable
import os

ListTestApp = Blueprint("list_test", __name__)

@ListTestApp.route("",methods=["GET"])
def ListTest():
    print(req.json)
    rows = TestTable.findAll()
    response = res(json.dumps({"rows":rows}), status=200, mimetype="application/json")
    return response
    