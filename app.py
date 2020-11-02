# python3
"""
    Python Flask Rest api to reflect AWS api gateway
    """

from flask import Flask, request, render_template, redirect, flash
import requests
import os
import json

app = Flask(__name__)
app.secret_key = 'some secret key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = "%s/.env" % BASE_DIR


# retrieve url from env file
def get_api_url():
    file = open(ENV_FILE, "r")
    return file.read().strip()


# store url to env file
def store_url(_url):
    file = open(ENV_FILE, "w")
    file.write(_url)
    file.close()


@app.route("/", methods=['POST'])
def index():
    """
        Reflector function
        """

    request_url = get_api_url()
    status_code = 400
    message = ""

    try:
        data = request.get_json()
        headers = {
            'Content-Type': request.headers['Content-Type'],
            'X-API-Key': request.headers['X-API-Key']
        }
        res = requests.post(request_url, json.dumps(data), headers=headers)
        status_code = res.status_code

    except Exception as e:
        message = str(e)

    return message, status_code


# @app.route('/url', methods=['GET', 'POST'])
# def url():
#     """
#         Form to edit api gateway url
#         """
#     if request.method == 'POST':
#         # store url to temp file
#         store_url(request.form['url'])
#         flash('Successfully updated.', 'success')
#         return redirect('/url')
#
#     return render_template('form.html', url=get_api_url())


if __name__ == "__main__":
    app.run(debug=True)
