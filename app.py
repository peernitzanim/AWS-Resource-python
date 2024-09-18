from flask import request
from flask import Flask
from ec2 import action_app_ec2
from s3 import action_app_s3
from route53 import action_app_route53

# Initialize the Flask application
app = Flask(__name__)

# Route to handle EC2 actions
@app.route('/ec2', methods=['POST'])
def ec2():
    # Call EC2 action function with the incoming request
    response = action_app_ec2(request)
    # Return response message and HTTP status code
    return response[0], response[1]  # Improved return with status message and code

# Route to handle S3 actions
@app.route('/s3', methods=['POST'])
def s3():
    # Call S3 action function with the incoming request
    response = action_app_s3(request)
    # Return response message and HTTP status code
    return response[0], response[1]  # Improved return with status message and code

# Route to handle Route 53 actions
@app.route('/route53', methods=['POST'])
def route53():
    # Call Route 53 action function with the incoming request
    response = action_app_route53(request)
    # Return response message and HTTP status code
    return response[0], response[1]  # Improved return with status message and code

# Main entry point to run the Flask application
if __name__ == "__main__":
    # Run the application on localhost with debugging enabled
    app.run(host='127.0.0.1', port=1020, debug=True)  # Server is running on port 1020
