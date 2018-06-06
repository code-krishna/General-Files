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

def methodV3 (AUTH_REQUEST, VER_THREE, token): 
  tokenLen=24;
  signatureLen=40;
  encrypt_key_number = 5
  encodedTokenLen = 33
  encodedToken = ""
  print('encodedTokenLen :', encodedTokenLen)
  bodyLen=0
  pos=0
  written_len = 0
  respond=1
  appId = "com.sanity.test"
  skeys = ['SM62KphYVQN1Y1OI', 'O2bxWuezJ5JhrdeZ', 'Yab4V6u8pzM3h9u8', 'mvLDu0c0tKw8fEd5', 'K6Ja3ZsVF2WvBWsA', '7NPs6Q4xXddwUVVV', 'HmbJ6zGm5qddMiie', 'sMyypdfUnXaPUS3g', 'IrrsXwfr4CCD9MuQ', 'rzQ3HlVbtNVIQSrv']
  buffr = "{\"isFg\" : \"true\",\"userId\" : \"testUser:79eec5bdfe7c6f03\",\"dUid\" : \"79eec5bdfe7c6f03\",\"dMk\" : \"HMD Global\",\"dMl\" : \"TA-1021\",\"mccMnc\" : \"405-53\"}"
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
  print("This is encodedToken")
  print(encodedToken)
  length = len(encodedToken)+1
  print(length)
  for item in encodedToken:
   buf.append(ord(item))
  pos += length
  print("Buf after adding token ", buf)
  #buf.append(0)
  #Adding current timestamp
  buf.append(0)
  tym = int(time.time())
  #p = int_to_bytes1(tym,8)
  p = int_to_bytes1(1528200938,8)
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
  low = (signatureLen & 0x00ff);
  high = ((signatureLen & 0xff00) >> 8)
  buf.append(high)
  buf.append(low)
  pos+=2

  ts_str = tym
  
  buf2 = "5b0fe4cd15b96108449339885b16311ecom.sanity.testSM62KphYVQN1Y1OI"
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
  encrypted=[]
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

methodV3(10,3, "5b0fe4cd15b9610844933988")
#print(int_to_bytes1(1528200938,8))