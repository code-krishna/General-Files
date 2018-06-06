import requests
import sys
import json
import socket
import binascii
import pickle
import base64
import time
import hashlib
from array import *
from random import randint

def int_to_bytes1(value, length):
    result = []

    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)

    result.reverse()

    return result


def str_xor(s1, s2):
 encr = []
 p=0
 for i in s1:
  encr.append(i ^ s2[p % len(s2)])
  p+=1;
 return encr


def methodV0 (AUTH_REQUEST, VER_ZERO, token, sig, socket): 
  sig_len = 4
  tokenLen = 24
  bodyLen = 2 + tokenLen + sig_len + 2
  buf = []
  pos = 0
  myArray = array('B', [(AUTH_REQUEST << 4) + VER_ZERO])
  for x in myArray:
      buf.append(x)
  #print(' '.join('{:02x}'.format(x) for x in myArray))
  pos += 1

  low = (bodyLen & 0x00ff)
  high = ((bodyLen & 0xff00) >> 8)
  myArray = array('B', [high, low])
  #print(' '.join('{:02x}'.format(x) for x in myArray))
  for x in myArray:
      buf.append(x)
  pos += 2

  low = (tokenLen & 0x00ff)
  high = ((tokenLen & 0xff00) >> 8)
  myArray = array('B', [high, low])
  #print(' '.join('{:02x}'.format(x) for x in myArray))
  for x in myArray:
      buf.append(x)
  pos += 2
  #print(' '.join('{:02x}'.format(x) for x in myArray))
  i = 0
  for item in token:
      buf.append(item)
  pos += tokenLen

  low = (sig_len & 0x00ff)
  high = ((sig_len & 0xff00) >> 8)
  myArray = array('B', [high, low])
  print(myArray)
  #print(' '.join('{:02x}'.format(x) for x in myArray))
  for x in myArray:
      buf.append(x)
  pos += 2
  for item in sig:
      buf.append(item)
  pos += sig_len
  print(token)
  print(buf)
  packet = str(bytearray(buf))
  appendData = "\nGET / HTTP/1.1\r\nHost: www.datami.com\r\nUser-Agent: curl/7.51.0\r\nAccept: */*\r\n\r\n"
  packet += appendData
  print(packet)
  x=0
  '''
  socket.send(packet)
  print(int(time.time()))
  tym = str(int(time.time()))
  timNum = []
  for i in list(tym):
   timNum.append(int(i))
  p = array('B', timNum)
  print(p)
  '''
  for x in range (0,40):
    print(x)
    socket.send(packet)
    print(socket.recv(1024))

  return (socket.recv(1024))

def methodV3 (AUTH_REQUEST, VER_THREE, token, socket): 
  tokenLen=24;
  signatureLen=40;
  encrypt_key_number = 5
  encodedTokenLen = 32
  encodedToken = ""
  #print('encodedTokenLen :', encodedTokenLen)
  bodyLen=0
  pos=0
  written_len = 0
  respond=1
  appId = "acr.browser.lightning"
  skeys = ['SM62KphYVQN1Y1OI', 'O2bxWuezJ5JhrdeZ', 'Yab4V6u8pzM3h9u8', 'mvLDu0c0tKw8fEd5', 'K6Ja3ZsVF2WvBWsA', '7NPs6Q4xXddwUVVV', 'HmbJ6zGm5qddMiie', 'sMyypdfUnXaPUS3g', 'IrrsXwfr4CCD9MuQ', 'rzQ3HlVbtNVIQSrv']
  buffr = "{\"isFg\" : \"true\",\"userId\" : " + "012345678998" + "\",\"dUid\" : \"" + "3c8c34a26d197249" + "\",\"dMk\" : \"samsung\",\"dMl\" : \"s4\",\"mccMnc\" : \"987-870\"}"
  written_len = len(buffr)
  #print("signatureLen: ",sys.getsizeof(signatureLen))
  bodyLen = 2 + encodedTokenLen + 2 + 8 + 40 + 1 + written_len + 2
  #print("bodyLen : ", bodyLen)
  buf = []
  req_buf = []
  pos_req = 0
  myArray = array('B', [(AUTH_REQUEST << 4) + VER_THREE])
  for x in myArray:
    req_buf.append(x)
  pos_req+=1
  myArray = array('B', [encrypt_key_number])
  for x in myArray:
      req_buf.append(x)
  pos_req+=1
  '''
  low = (bodyLen & 0x00ff);
  high = ((bodyLen & 0xff00) >> 8)
  myArray = array('B', [high,low])
  for x in myArray:
      buf.append(x)
  pos_req+=2
  '''
  low = (respond & 0x00ff)
  print("First low: ",low)
  buf.append(low)
  pos+=1
  low =(encodedTokenLen & 0x00ff);
  high =((encodedTokenLen & 0xff00) >> 8)
  buf.append(high)
  buf.append(low)
  pos+=2
  print("Buf before adding token ", buf)
  encodedToken += str((base64.b64encode(bytes(token))).decode("utf-8")) #encoding in base64
  #encodedToken+="\0"
  print("This is encodedToken")
  print(encodedToken)
  length = len(encodedToken)
  print(length)
  for item in encodedToken:
   buf.append(ord(item))
  pos += length
  print("Buf after adding token ", buf)
  buf.append(0)
  #Adding current timestamp
  buf.append(0)
  tym = int(time.time())
  p = int_to_bytes1(tym,8)
  #p = int_to_bytes1(1528200938,8)
  for item in p:
    buf.append(item)
  #buf.append(0)
  '''
  buf.append(p[7])
  buf.append(p[6])
  buf.append(p[5])
  buf.append(p[4])
  buf.append(p[3])
  buf.append(p[2])
  buf.append(p[1])
  buf.append(p[0])
  '''
  pos+=8
  print("Buf after adding timestamp: ", buf)
  #Adding Signature len
  low = (signatureLen & 0x00ff);
  high = ((signatureLen & 0xff00) >> 8)
  buf.append(high)
  buf.append(low)
  pos+=2

  ts_str = str(tym)
  
  buf2 = token + ts_str + appId + skeys[0]
  print("This is buf2")
  print(buf2)
  #encrypting in SHA1
  sha_1 = hashlib.sha1()
  sha_1.update(buf2)
  digest = sha_1.digest()

  print("This is digest")
  print(digest)

  result = ""
  #print(" ".join("{:08x}".format(ord(c)) for c in digest))
  x=0
  while x<5:
    result+="".join("{:08x}".format(ord(digest[x])))
    x+=1
  #result+="".join("{:08x} ".format(ord(c)) for c in digest)
  print("This is result:")
  print(result)
  
  # Putting digest key in buffer
  for item in result:
   buf.append(ord(item))
  pos += 40
  
  #Adding payload length
  low = (len(buffr) & 0x00ff);
  high = ((len(buffr) & 0xff00) >> 8)
  buf.append(high)
  buf.append(low)
  pos+=2

  
  for item in buffr:
    buf.append(ord(item))
  buf.append(0)
  pos+=len(buffr)

  print("This is buf")
  print(buf)
  print(len(buf))
  pack = ""
  for item in buf:
    pack+=str(item)
  print(pack)
  #packet = str(bytearray(buf))
  #print("This is buf packet")
  #print(packet)
  #encrypted=[]
  encrypted1=""
  '''
  for i in buf:
   encrypted += i ^ skeys[encrypt_key_number]
   '''
  skey = []
  for item in skeys[encrypt_key_number]:
    skey.append(ord(item))
  encrypted=str_xor(buf, skey)
  encrypted[pos] = 0
  '''
  for i in encrypted:
   encrypted1 += str(i) ^ skeys[encrypt_key_number]
  '''
  #encrypted1+=str_xor(encrypted, skey)

  print("This is encrypted buf:")
  print(encrypted)
  #print("This is decrypted buf:")
  #print(encrypted1)
  #print(len(encrypted))
  low = (pos & 0x00ff)
  high = ((pos & 0xff00) >> 8)
  print("High and Low")
  print(high)
  print(low)
  myArray = array('B', [high,low])
  for x in myArray:
    req_buf.append(x)
  pos_req+=2
  print("This is req_buf")
  packet = str(bytearray(req_buf))
  print("".join("{:02x} ".format(ord(c)) for c in packet))
  req_buf = req_buf + encrypted
   #print(x)
  pos_req+=pos
  print("This is req_buf with encrypted buf")
  print(req_buf)

  packet = str(bytearray(req_buf))
  print("This is req_buf packet: ")
  print(packet)
  print("This is req_buf hex packet: ")
  print(" ".join("{:02x}".format(ord(c)) for c in list(packet)))
  appendData = "\nGET / HTTP/1.1\r\nHost: www.codeforces.com\r\nUser-Agent: curl/7.51.0\r\nAccept: */*\r\n\r\n"
  packet += appendData
  print(packet)
  socket.send(packet)
  print(socket.recv(1024))



urlD = 'https://discovery.cloudmi.datami.com/v0'
HeaderD = {
     'x-dmi-code-path': 'test',
     'x-dmi-sdk': 'slasanity-amznlinux_1.0.0/6.5.0',
     'x-dmi-api-key': 'dmi-dev-sdk-build-7b29616f0c08ec653263f3979424986b419e738f',
     'x-dmi-service-token': 'd419a39cb068a64a52937d55c4ba3d163bc4b3d2',
     'x-real-ip': '244.243.0.0',
     'x-client-ip': '223.227.56.103',
     'x-dmi-app': 'com.tej.test.sdk',
     'content-type': 'application/json'
}

bodyD = {'op': 'tej-test-opname', 'appId': 'com.sanity.test', 'mccmnc': '987-870', 'uid': 'sanity.device.uid'}
# POST some form-encoded data:
post_response = requests.post(urlD, data=json.dumps(bodyD), headers=HeaderD)
print(post_response.json())
response = post_response.json()
print(response['services'])
newURLD = response['services']['aacmi'] + '/v1/sd/int/authorize'
print(newURLD)
newHeaderD = {
   "content-type": "application/json",
   "x-dmi-api-key": "dmi-dev-sdk-build-7b29616f0c08ec653263f3979424986b419e738f",
   "x-nokia-msisdn": "012345678998",
   "x-dmi-sdk": "smisdk-android_1.1.0/4.4.2",
   "x-real-ip": "244.243.0.0",
   "x-client-ip": "244.244.0.0",
   "x-forwarded-for": "244.244.0.0",
   "x-dmi-service-token": "d4d7e86ba36fb82ab10241d3973deca5877f3496",
   "x-dmi-uuid": "880a2173-d305-4b89-bb48-14a36844ddca"
}

newBodyD = {"auth": {
     "url": "http://s3.amazonaws.com/assets.cloudmi.datami.com/public/cloud-sanity-test",
     "appId": "com.sanity.test",
     "accessType": "APP_PROXY",
     "deviceId": {
       "uid": "3c8c34a26d197249",
       "make": "samsung",
       "model": "s4"
     },
     "adInfo": {
       "trackinEnabled": 'true',
       "googleId": "5e8e35bf-8b54-49f4-bee0-11a01a4a1d6d"
     },
     "userId": "3583b3447841b6f",
     "packageCode": "QA-SANITY-TEST-14b071eab780dba2c7ac1219"
   }
}
post_response1 = requests.post(newURLD, data=json.dumps(newBodyD), headers=newHeaderD)
print(post_response1.json())
print(post_response1.json()['data']['sdPort'])
print(post_response1.json()['data']['sdHost'])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = post_response1.json()['data']['sdHost']
port = post_response1.json()['data']['sdPort']
tkn = json.dumps(post_response1.json()['data']['zMiAuthToken'])
token = ""
for i in tkn:
  if i!='"':
   token+=i
print(token)
s.connect((host, port))
methodV3(10, 3, "5b17b65015b9612e807ce5fb", s)
#methodV0(10,0,token, "temp", s)
s.close()

