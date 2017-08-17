#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask import make_response,render_template
import requests

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/policy', methods=['GET','POST'])
def term_policy():
    return render_template("policy.html")
def private_policy():
    return render_template('private_policy.html')

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    try:
        print('yes')
        print(request)  
        req = request.get_json(silent=True, force=True)
        print('===========',dict(req))
        r=processRequest(dict(req))
        r.headers['Content-Type'] = 'application/json'
    except Exception as ex:
        print(ex)
    return r

def processRequest(req):
    try:    
        if req["result"]["action"]!= "glassdoor_review":
             return {}
        else:
            print('not found')
        result = req.get("result")
        paramters=result["paramters"]
        company=paramters["company"]
        baseurl = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=183304&t.k=bhWphgxkLDO&action=employers&q="+company
        baseurl+="&userip=192.168.1.44&useragent=Mozilla/%2F5.0"
        header = {'User-Agent': 'Mozilla/5.0'}
        result = str(requests.request(url=baseurl,headers=header,method="GET").text).replace('\n','')
        data = json.loads(result)
        res = makeWebhookResult(data)
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r
    except Exception as ex:
        print(ex)
        return json.dumps({'error':ex}) 
def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))
    speech = "According to glassdoor ,these are the reviews that i found \n"
    speech+="1.Pros "+ str(data['response']['employers'][0]['featuredReview']['pros'])+"\n"
    speech+="2.Cons "+ str(data['response']['employers'][0]['featuredReview']['cons'])+"\n"
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
