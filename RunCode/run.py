from flask import Blueprint, request as req, Response as res, json
from kafka import KafkaProducer
import os
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

ExecuteApp = Blueprint("run_code", __name__)

@ExecuteApp.route("/submit",methods=["POST"])
def submit():
    print(req.json)
    message = req.json
    message['isRun'] = False
    producer.send(req.json['lang'], value=json.dumps(message).encode('utf-8'))
    return res(json.dumps({'id':message['id']}), status=200)

@ExecuteApp.route("/run",methods=["POST"])
def run():
    # print(req.json)
    message = req.json
    message['isRun'] = True
    print(message)
    producer.send(req.json['lang'], value=json.dumps(message).encode('utf-8'))
    return res(json.dumps({'id':message['id']}), status=200)
    