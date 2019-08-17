from flask import Flask,json,request
import time
import json
import requests
timestamp=int(time.time())
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
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

def paketlist(token):
    ham = {"msisdn":"","mode":"owned","products":["airtime","credit","data"]}
    data=json.dumps(ham, sort_keys=True)
    linkpaketlist="https://craterapi.com/api/package/advanced_search"
    headerx={"User-Agent":Uagent,"Authorization":token,"Content-Type":"""application/json; charset=utf-8"""}
    r = requests.post(linkpaketlist,headers=headerx,data=data)
    return r.json()


def get_oneprice(id,token):
    listem = []
    listem.append(id)
    link="https://craterapi.com/api/package/offer/buy"
    headerx={"User-Agent":Uagent,"Authorization":token,"Content-Type":"""application/json; charset=utf-8"""}
    r = requests.post(link,headers=headerx,data=str(listem))
    return r.json()[0]["price"]

    
@app.route("/pklist")
def pklist():
    try:
        token= request.headers["token"]
        paketler = paketlist(token)
        balance = 0
        donut=[]
        for i in paketler:
            paketid=i["id"]
            paketmiktar=i["lotsize"]
            paketdeger=get_oneprice(paketid,token)
            balance+=(paketdeger*paketmiktar)
            name = i["carrier"]["name"]+" "+str(i["plan"]["size"])
            donut.append({"pname":name,"paketmiktar":paketmiktar,"paketfiyat":paketdeger,"deger":paketdeger*paketmiktar})
        donut.reverse()
        donut.append({"toplam":balance})
        donut.reverse()
        return json.dumps(donut, cls=SetEncoder)
    except Exception as e:
        print(e)
        return "Hata"
@app.route("/")
def index():
    return str(timestamp)
if __name__=="__main__":
    app.run()
