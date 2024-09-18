from flask import request
from flask import Flask
from ec2 import action_app_ec2
from s3 import action_app_s3
from route53 import action_app_route53

app = Flask(__name__)


@app.route('/ec2', methods=['POST'])
def ec2():
    response = action_app_ec2(request)
    return response[0], response[1]


@app.route('/s3', methods=['POST'])
def s3():
    response = action_app_s3(request)
    return response[0], response[1]


@app.route('/route53', methods=['POST'])
def route53():
    response = action_app_route53(request)
    return response[0], response[1]


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=1020, debug=True)  # run the server
