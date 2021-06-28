# Serverless Photo App
Serverless Photo Application

# Motivation:

Let's say we have to architect a solution where we have to design a serverless image application where we have to send an image through an image web app and our serverless architecture. We will utilize AWS to send our data from our image web application which is hosted on the EC2 instance and then it puts the data in the queue which will trigger the Lambda function. Lambda function is designed to take the image and save it to S3, and send a message to the email mentioning if the image has been successfully uploaded or not.

# Architecture:
![architecture](https://user-images.githubusercontent.com/13358738/123573432-ae836600-d7ed-11eb-8dda-1bb99fbe07fa.png)

# Prerequisites:
1. AWS Lambda
2. AWS S3
3. AWS SES
4. AWS SQS
5. AWS Route53
6. AWS EC2
7. AWS IAM

# Replication Steps
1. Configure your server to run aws cli
2. Create a config.ini file in this format
```bash
[SQS]
connection_string=<your-connection-string>
```
3. Commands to confiure the application
```bash
git clone git@github.com:codexponent/serverless-photo-app.git
pip install -r requirements.txt
python main.py
```


