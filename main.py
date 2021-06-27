# # Importing Libraries
import os
import uuid
import boto3
import base64
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# # Setting up configparser
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Create SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

# # Setting Values
random_uuid = str(uuid.uuid4())
queue_url = config['SQS']['connection_string']

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)

	print('request.form.get')
	print(request.form.get)
	
	file = request.files['file']
	email= request.form.get("your_email", "")



	# print("----------------------")
	# print(email)
	# print("---------------------------")
	read_file = file.read()
	encoded = base64.encodebytes(read_file)
	# print(encoded)
	# print("----------------------")
	
	image_str = encoded.decode('utf-8')
	# print("---------------------------")
	result = email+image_str
	# print("----------------------")
	# print(result)
	# print("---------------------------")
	
	# Send message to SQS queue
	response = sqs.send_message(
		QueueUrl=queue_url,
		MessageDeduplicationId=random_uuid,
		MessageBody=(
			result
			),
			MessageGroupId='1'
		)
	# print(random_uuid)

	# if file.filename == '':
	# 	flash('No image selected for uploading')

	# 	# print(email)
	# 	return redirect(request.url)
	# if file and allowed_file(file.filename):
	# 	filename = secure_filename(file.filename)
		
	# 	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	# 	#print('upload_image filename: ' + filename)
	# 	flash('Image successfully uploaded and displayed below')
	# 	return render_template('upload.html', filename=filename)
	# else:
	# 	flash('Allowed image types are -> png, jpg, jpeg, gif')
	# 	return redirect(request.url)
	return render_template('upload.html')

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)