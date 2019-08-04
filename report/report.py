from flask import Blueprint, request as req, Response as res, json
from auth.users import Users
from init import Orm

reportApp = Blueprint("report", __name__)

@reportApp.route("",methods=["POST"])
def report():
    body = req.json.copy()
    body['report'] = json.dumps(body['report'])
    res_code = Report.insert(body)
    if(res_code == -1):
        response = res(json.dumps({"message":"Error"}), status=500, mimetype="application/json")
    elif(res_code == -2):
        response = res(json.dumps({"message":"Duplicate"}), status=409, mimetype="application/json")
    else:
        response = res(json.dumps({"message":"Success"}), status=200, mimetype="application/json")
    return response


from init import Orm
import orm

Report = Orm.define('report', {
    'id':{
        'type':orm.STRING,
        'notNull':True
    },
    'uname':{
        'type':orm.STRING,
        'notNull':True
    },
    'dept':{
        'type':orm.STRING,
        'notNull':True
    },
    'year':{
        'type':orm.STRING,
        'notNull':True
    },
    'section':{
        'type':orm.STRING,
        'notNull':True
    },
    'test':{
        'type':orm.STRING,
        'notNull':True
    },
    'report':{
        'type':orm.STRING,
        'notNull':True
    },
})