from flask import Flask,json,request
import time
import requests
timestamp=int(time.time())
Uagent="""Dalvik/2.1.0 (Linux; U; Android 7.1.1; General Mobile 4G Build/NMF26F)"""
app = Flask(__name__)
@app.route("/wakeup")
def wakeup():
    global timestamp
    timestamp=int(time.time())
    return "1"
@app.route("/buy")
def buy():
    try:
        global timestamp
        timestamp=int(time.time())
        paket_id= request.headers["paket_id"]
        price= float(request.headers["price"])
        token= request.headers["token"]
        ham = {"msisdn":"","package_id":paket_id,"mode":"new","activation_type":"store","price":price}
        data=json.dumps(ham, sort_keys=True)
        linkbuy="https://craterapi.com/api/buy"
        headerx={"User-Agent":Uagent,"Authorization":token,"Content-Type":"""application/json; charset=utf-8"""}
        r = requests.post(linkbuy,headers=headerx,data=data)
        return "1"
    except:
        return "Hata"
@app.route("/")
def index():
    return str(timestamp)
if __name__=="__main__":
    app.run()
