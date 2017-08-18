#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import request
from flask import render_template,jsonify
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
        req = request.get_json(silent=True, force=True)
        res = json.dumps(req, indent=4)
            
        res=processRequest(req)    
        res = json.dumps(res, indent=4)
        r = make_response(res)
        print(type(r))
        r.headers['Content-Type'] = 'application/json'
        return r
    except Exception as ex:
        return(json.dumps({"error":str(ex),"type":str(type(r))}))
    return r

def processRequest(req):
    try:    
        print(type(req))
        print(req.get("result"))
        if req.get("result").get("action") != "glassdoor_review":
             return {}
        result = req.get("result")
        parameters=result.get("parameters")
        company=parameters.get("company")
        
        baseurl = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=183304&t.k=bhWphgxkLDO&action=employers&q="+company
        baseurl+="&userip=192.168.1.44&useragent=Mozilla/%2F5.0"
        header = {'User-Agent': 'Mozilla/5.0'}
        result = str(requests.request(url=baseurl,headers=header,method="GET").text).replace('\n','')
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res
    except Exception as ex:
        print(ex)
        return(json.dumps({"error":str(ex)}))

def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))
    speech = "According to glassdoor ,these are the reviews that i found \n"
    speech+="1.Pros "+ str(data['response']['employers'][0]['featuredReview']['pros'])+"\n"
    speech+="2.Cons "+ str(data['response']['employers'][0]['featuredReview']['cons'])+"\n"

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
