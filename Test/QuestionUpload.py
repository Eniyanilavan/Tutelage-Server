from flask import Blueprint, request as req, Response as res, json
import os

QuestionUploadApp = Blueprint("question_upload", __name__)

@QuestionUploadApp.route("/<test_name>",methods=["POST"])
def upload(test_name):
    questions = req.json['questions']
    for index in range(0,len(questions)):
        question = questions[index]
        os.makedirs('./Tests/{}/{}'.format(test_name, str(index)))
        os.makedirs('./Tests/{}/{}/Testcases'.format(test_name, str(index)))
        with open('./Tests/{}/{}/question.txt'.format(test_name, str(index)), 'w') as fp:
            fp.writelines(question.get('string'))
        testcases = question.get('testcases')
        for i_index in range(0, len(testcases)):
            testcase = testcases[i_index]
            os.makedirs('./Tests/{}/{}/Testcases/{}'.format(test_name, str(index), str(i_index)))
            input_file = open('./Tests/{}/{}/Testcases/{}/input.txt'.format(test_name, str(index), str(i_index)), 'w')
            input_file.writelines(testcase.get('input'))
            output_file = open('./Tests/{}/{}/Testcases/{}/output.txt'.format(test_name, str(index), str(i_index)), 'w')
            output_file.writelines(testcase.get('output'))
    
    return res(status=200)