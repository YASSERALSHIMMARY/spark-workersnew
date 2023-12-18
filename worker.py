from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

def get_api_key() -> str:
    try:
        secret = os.environ.get("COMPUTE_API_KEY")
        if secret:
            return secret
        else:
            # Local testing
            with open('.key') as f:
                return f.read()
    except Exception as e:
        app.logger.error(f"Error in get_api_key: {e}")
        return None

@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add:"

@app.route("/test")
def test():
    try:
        return get_api_key()
    except Exception as e:
        app.logger.error(f"Error in test route: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/add", methods=['GET', 'POST'])
def add():
    try:
        if request.method == 'GET':
            return "Use POST to add"  # replace with form template
        else:
            token = get_api_key()
            if not token:
                raise Exception("API key retrieval failed")
            ret = addWorker(token, request.form['num'])
            return ret
    except Exception as e:
        app.logger.error(f"Error in add route: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

def addWorker(token, num):
    try:
        with open('payload.json') as p:
            tdata = json.load(p)
        tdata['name'] = 'slave' + str(num)
        data = json.dumps(tdata)
        url = 'https://www.googleapis.com/compute/v1/projects/leafy-future-333222/zones/europe-west1-b/instances'
        headers = {"Authorization": "Bearer " + token}
        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code == 200:
            return "Done"
        else:
            app.logger.error(f"Error in addWorker response: {resp.content}")
            return "Error\n" + resp.content.decode('utf-8') + '\n\n\n' + data
    except Exception as e:
        app.logger.error(f"Error in addWorker: {e}")
        return "Error in adding worker"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')

