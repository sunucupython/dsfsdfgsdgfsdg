from flask import Flask,json
import time
import requests
app = Flask(__name__)
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
Authorization = """Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIrOTA1NDI3NjY1MTU0IiwiYXV0aCI6IlJPTEVfVVNFUiJ9.iOjX0MpPlDLIg6LMis-GK9py4j18s7EWlThiUyu5PuH1UCOp3ng-qGzipKuIKDuMfAoRCymkLzoyMikjTCxyRg"""
CType = """application/json; charset=utf-8"""

Uagent="""Dalvik/2.1.0 (Linux; U; Android 7.1.1; General Mobile 4G Build/NMF26F)"""

herlink="https://dentdestek.herokuapp.com/aldim"
btimestamp=int(time.time())
stimestamp=int(time.time())
def get_pricelist():
    global stimestamp
    listem = []
    for i in range(1,1001):
        listem.append(i)
    link="https://craterapi.com/api/package/offer/buy"
    headerx={"User-Agent":Uagent,"Authorization":"aa","Content-Type":CType}
    r = requests.post(link,headers=headerx,data=str(listem))
    stimestamp=int(time.time())
    return r.json()
def buy(paket_id,price):
    ham = {"msisdn":"","package_id":paket_id,"mode":"new","activation_type":"store","price":price}
    data=json.dumps(ham, sort_keys=True)
    linkbuy="https://craterapi.com/api/buy"
    headerx={"User-Agent":Uagent,"Authorization":Authorization,"Content-Type":CType}
    r = requests.post(linkbuy,headers=headerx,data=data)
    return r.json()

def paketlist():
    ham = {"msisdn":"","mode":"owned","products":["airtime","credit","data"]}
    data=json.dumps(ham, sort_keys=True)
    linkpaketlist="https://craterapi.com/api/package/advanced_search"
    headerx={"User-Agent":Uagent,"Authorization":Authorization,"Content-Type":CType}
    r = requests.post(linkpaketlist,headers=headerx,data=data)
    paketl=[]
    for i in r.json():
        name = i["carrier"]["name"]+" "+str(i["plan"]["size"])
        paketl.append(name)
        
    return paketl

def balance():
    linkbalance="https://craterapi.com/api/balance"
    headerx={"User-Agent":Uagent,"Authorization":Authorization,"Content-Type":CType}
    r = requests.get(linkbalance,headers=headerx)
    for i in r.json():
        if i["asset"]=="token":
            return i["balance"]
    return False

@app.route("/puan")
def puan():
    try:
        return str(balance())
    except:
        return "hata"
@app.route("/pklist")
def pklist():
    try:
        veri=paketlist()
        return json.dumps(veri, cls=SetEncoder)
    except:
        return "hata"
@app.route("/aldim")
def aldim():
    while True:
        r = requests.get(herlink)
        if r.status_code==200:
            return True
    return False
@app.route("/")
def index():
    return "baslangic t:{}  son kontrol t:{}".format(btimestamp,stimestamp)
from apscheduler.schedulers.blocking import BlockingScheduler
def calisma():
    veri = get_pricelist()
    for i in veri:
        if i["price"]<50:
            paketid=i['package_id']
            fiyat = float(i["price"])
            buy(paketid,fiyat)
sched = BlockingScheduler()
sched.add_job(calisma, 'interval', seconds=0.5)
sched.start()
if __name__=="__main__":
    app.run(port =80,debug=True)
