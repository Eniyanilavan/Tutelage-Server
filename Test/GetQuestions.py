from flask import Blueprint, request as req, Response as res, json
from Test.table import TestTable
import os

GetQuestionApp = Blueprint("get_question", __name__)

@GetQuestionApp.route("/<test_name>",methods=["GET"])
def GetQuestion(test_name):
    print(test_name)
    questions = []
    questions_dirs = os.listdir('./Tests/{}'.format(test_name))
    for questions_dir in questions_dirs:
        content = open('./Tests/{}/{}/question.txt'.format(test_name, questions_dir))
        questions.append(content.read())
    print(questions)
    return res(json.dumps({'questions':questions}), status=200, mimetype="application/json")
    