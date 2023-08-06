import requests
import ast

url = "http://55.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152"
page = requests.get(url)
page = page.content
data = ast.literal_eval(page.decode('utf-8'))
data = data["data"]["diff"]

stkList = {}

for each in data:
    stkList[each["f12"]] = {} 
    stkList[each["f12"]]["name"] = each['f14']
    stkList[each["f12"]]['price'] = each['f2']
    stkList[each["f12"]]['per'] = each['f9']
    stkList[each["f12"]]['mktCap'] = each['f20']
    stkList[each["f12"]]['flowCap'] = each['f21']
    stkList[each["f12"]]['market'] = each['f13']    
    stkList[each["f12"]]['amount'] = each['f6']    
    stkList[each["f12"]]['amplitude'] = each['f7']    
    stkList[each["f12"]]['high'] = each['f15']    
    stkList[each["f12"]]['low'] = each['f16']    
    stkList[each["f12"]]['open'] = each['f17']    
    stkList[each["f12"]]['turnoverRate'] = each['f8']    
    stkList[each["f12"]]['vol'] = each['f5']    
    stkList[each["f12"]]['upAmount'] = each['f3']    

def getStkName(code):
    return stkList[code]["name"]
def getPrice(code):
    return stkList[code]["price"]
def getPer(code):
    return stkList[code]["per"]
def getMktCap(code):
    return stkList[code]["mktCap"]
def getFlowCap(code):
    return stkList[code]["flowCap"]
def getMarketId(code):
    return stkList[code]['market']
def getAmount(code):
    return stkList[code]['amount']
def getAmplitude(code):
    return stkList[code]['amplitude']
def getHigh(code):
    return stkList[code]['high']
def getLow(code):
    return stkList[code]['low']
def getOpen(code):
    return stkList[code]['open']
def getTurnoverRate(code):
    return stkList[code]['turnoverRate']
def getVol(code):
    return stkList[code]['vol']
def getUpAmount(code):
    return stkList[code]['upAmount']
