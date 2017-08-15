#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['GET','POST'])
def webhook():
    print('yes')
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    # if req.get("result").get("action") != "glassdoor_review":
    #     return {}
    baseurl = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=183304&t.k=bhWphgxkLDO&action=employers&q=prolifics"
    +"&userip=192.168.1.44&useragent=Mozilla/%2F5.0"
    header = {'User-Agent': 'Mozilla/5.0'}
    result = requests(baseurl,headers=header).text.replace('\n','')
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))
    speech = "According to glassdoor ,these are the reviews that i found"
    speech+="1.Pros "+ str(decoded['response']['employers'][0]['featuredReview']['pros'])
    speech+="2.Cons "+ str(decoded['response']['employers'][0]['featuredReview']['cons'])
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
