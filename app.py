#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "findparcel":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    parcelnumber = parameters.get("parcelnumber")

    parcelinfo = {'5000':'your parcel has been shipped', '5001':'your parcel has not been shipped', '5002':'your parcel should be delivery in two days', '5003':'your parcel has been shipped', '5004':'your parcel has been shipped', '5005': 'your parcel should be delivery in three days'}

    speech = "Parcel with number: " + parcelnumber + " is " + str(parcelinfo[parcelnumber])"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
