
# A very simple Flask Hello World app for you to get started with...
import os
from flask import Flask, send_from_directory, abort,Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        
        return render_template('index.html')
         
    except Exception as e:
        return e  # Internal server error

DOWNLOAD_DIRECTORY2 = os.path.join(os.getcwd(), 'download/premium')

@app.route('/download/premium/<path:filename>', methods=['GET'])
def download_file2(filename):
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY2, filename, as_attachment=True)
       
    except Exception as e:
        return e  # Internal server error

    
DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), 'download')

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, filename, as_attachment=True)
       
    except Exception as e:
        return e  # Internal server error
    

application = app