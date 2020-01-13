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

def fiyatlist(listem,token):
    link="https://craterapi.com/api/package/offer/buy"
    headerx={"User-Agent":Uagent,"Authorization":token,"Content-Type":"""application/json; charset=utf-8"""}
    r = requests.post(link,headers=headerx,data=str(listem))
    return r.json()

@app.route("/balance")
def balance():
    try:
        token= request.headers["token"]
        linkbalance="https://craterapi.com/api/balance"
        headerx={"User-Agent":Uagent,"Authorization":token,"Content-Type":"""application/json; charset=utf-8"""}
        r = requests.get(linkbalance,headers=headerx)
        for i in r.json():
            if i["asset"]=="token" and i["ticker"]=="DENT":
                return str(i["balance"])
        return False
    except Exception as e:
        print(e)
        return "Hata"
    
@app.route("/pklist")
def pklist():
    try:
        token= request.headers["token"]
        veriler = paketlist(token)
        pbilgi_list=[]
        balance = 0
        pkidler=[]
        for i in veriler:
            paketid=i["id"]
            pkidler.append(paketid)
            paketmiktar=i["lotsize"]
            name = i["carrier"]["name"]+" "+str(i["plan"]["size"])
            pbilgi_list.append([paketmiktar,name])
        fiyatlar = fiyatlist(pkidler,token)
        x=0
        donut=[]
        toplamPaketSayisi=0
        while(x<len(fiyatlar)):
            toplamPaketSayisi+=1
            paketdeger=fiyatlar[x]["price"]
            balance+=paketdeger*pbilgi_list[x][0]
            donut.append({"pname":pbilgi_list[x][1],"paketmiktar":pbilgi_list[x][0],"paketfiyat":paketdeger,"deger":paketdeger*pbilgi_list[x][0]})
            x+=1
        donut.reverse()
        donut.append({"toplamPaketSayisi":toplamPaketSayisi})
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
    app.run(debug=True)
