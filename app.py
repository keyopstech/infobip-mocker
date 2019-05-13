# compose_flask/app.py
from flask import Flask, request, Response, render_template, jsonify, redirect, url_for
from redis import Redis
from time import gmtime, strftime
import json
import sys

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

def to_pretty_json(value):
    try:
        return json.dumps(json.loads(value), indent=2)
    except ValueError:
        return {"error": "Decoding JSON has failed"}

app.jinja_env.filters['to_pretty_json'] = to_pretty_json

@app.route('/', methods = ['GET'])
def main():
    return render_template("logs.html", logs=redis.xrevrange('smslog'))

@app.route('/clean-redis', methods = ['GET'])
def clean_redis():
    redis.flushall()
    return redirect(url_for('main'))

@app.route('/', defaults={'path': ''}, methods = ['POST'])
@app.route('/<path:path>', methods = ['POST'])
def catch_all(path):
    response = {"success": True}
    redis.xadd('smslog', {
        'time': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        'path': path,
        'payload': request.get_data(),
        'response': json.dumps(response)
    })
    return jsonify(response)

@app.route('/sms/<int:version>/text/advanced', methods = ['POST'])
def catch_sms_advanced(version):
    response = {
       "bulkId": True,
       "messages": [{
           "to": "fakeDest",
           "status":{
               "groupId":3,
               "groupName":"DELIVERED",
               "id":5,
               "name":"DELIVERED_TO_HANDSET",
               "description":"Message delivered to handset"
           },
           "smsCount": 1,
           "messageId": 1
       }]
    }
    redis.xadd('smslog', {
        'time': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        'path': 'sms/%d/text/advanced' % version,
        'payload': request.get_data(),
        'response': json.dumps(response)
    })
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)