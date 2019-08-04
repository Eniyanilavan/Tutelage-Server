import orm
from orm import ORM
from flask import Flask, Response, request, json
from auth.signup import signupApp
from auth.login import loginApp
from auth.users import Users
from Test.QuestionUpload import QuestionUploadApp
from Test.CreateTest import CreateTestApp
from dashboard.list import ListTestApp
from RunCode.run import ExecuteApp
from report.report import reportApp
from Test.GetQuestions import GetQuestionApp
from flask_cors import CORS
import jwt

app = Flask(__name__)
CORS(app, allow_headers= ['Content-Type','Set-Cookie','*'])

@app.before_request
def verifyUser():
    print(request.path)
    if('/login' not in request.path and '/signup' not in request.path):
        try:
            jwt.decode(request.args.get('token'), 'srimanakulavinayagarengineeringcollege-vikram-dl', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response(json.dumps({'message':'unauthorized'}), status=403)
    

app.register_blueprint(signupApp, url_prefix="/signup")
app.register_blueprint(loginApp, url_prefix="/login")
app.register_blueprint(QuestionUploadApp, url_prefix="/upload")
app.register_blueprint(CreateTestApp, url_prefix="/create_test")
app.register_blueprint(ExecuteApp, url_prefix="/code")
app.register_blueprint(ListTestApp, url_prefix="/tests")
app.register_blueprint(GetQuestionApp, url_prefix="/get_questions")
app.register_blueprint(reportApp, url_prefix="/report")

app.run(port=5000, debug=True, host="0.0.0.0")



