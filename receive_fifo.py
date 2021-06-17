
# # Receive message from SQS queue
# response = sqs.receive_message(
#     QueueUrl=queue_url,
#     AttributeNames=[
#         'SentTimestamp'
#     ],
#     MaxNumberOfMessages=1,
#     MessageAttributeNames=[
#         'All'
#     ],
#     WaitTimeSeconds=5
# )

# data = response['Messages'][0]['Body']
# receipt_handle = response['Messages'][0]['ReceiptHandle']

# # Delete from the Queue
#response = sqs.delete_message(
#    QueueUrl=queue_url,
#    ReceiptHandle=receipt_handle
#)
# # Importing Libraries
import time
import uuid
import json
import boto3
import base64
import logging
from botocore.exceptions import ClientError

# # Setting up configparser
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def lambda_handler(event, context):
    # TODO implement
    
    print('context')
    print(context)
    print('event')
    print(event)
    
    # # Setting up Values for SES
    SENDER = "Sulabh Shrestha <tsulabh4@gmail.com>"
    # RECIPIENT = "sulabhshrestha@outlook.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "Status of the Document"
    SUCCESS_BODY_TEXT = ("Status of the Document\r\n"
                 "Your file has been uploaded successfully"
                )
    FAILURE_BODY_TEXT = ("Status of the Document\r\n"
                 "Your file hasn't been uploaded successfully"
                )
    SUCCESS_BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Status of the Document</h1>
      <p>Your file has been uploaded successfully</p>
    </body>
    </html>
                """            
    FAILURE_BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Status of the Document</h1>
      <p>Your file hasn't been uploaded successfully</p>
    </body>
    </html>
                """            
    CHARSET = "UTF-8"
    
    # # Setting up boto3 client
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # # Setting up variables
    queue_url = config['SQS']['connection_string']
    bucket_name = config['SQS']['bucket_name']
    randomuuid = str(uuid.uuid4())
    
    print('Start to consume message')
    
    # Receive message from SQS queue
    # response = sqs.receive_message(
    #     QueueUrl=queue_url,
    #     AttributeNames=[
    #         'SentTimestamp'
    #     ],
    #     MaxNumberOfMessages=1,
    #     MessageAttributeNames=[
    #         'All'
    #     ],
    #     WaitTimeSeconds=20
    # )
    # print('Message received')
    # print('data')
    # print(response)
    
    print('start to parse data')
    # data = response['Messages'][0]['Body']
    # print('data here')
    # receipt_handle = response['Messages'][0]['ReceiptHandle']
    
    data = event['Records'][0]['body']
    
    # print('data')
    # print(data)
    # print('receipt_handle')
    # print(receipt_handle)

    # # Decode and Save
    # print('Checking the type of the data file')
    # print(type(data))

    # # Split the string to separate the email and bytes
    temp_split = data.split('.com')
    email = temp_split[0] + '.com'
    RECIPIENT = email
    dataonly = temp_split[1]
    
    # # Give appropriate filename
    filename = randomuuid + email + '.jpg'

    # # Convert to Byte
    data_byte = bytes(dataonly, 'utf-8')
    print(type(data_byte))
    image_64_decode = base64.decodebytes(data_byte)
    image_result = open('/tmp/'+filename, 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)

    # # Upload to S3
    s3.upload_file('/tmp/'+filename, bucket_name, filename)
    print('Uploaded to S3')

    # # Send Email to the recipient
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': SUCCESS_BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': SUCCESS_BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )

    # Delete from the Queue
    # response = sqs.delete_message(
    #     QueueUrl=queue_url,
    #     ReceiptHandle=receipt_handle
    # )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

