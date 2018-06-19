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
from Variables import GD_Variable, Aacmi_Variable
from itertools import permutations
try:
    range = xrange
except NameError:
    pass
# Custom SHA-1 library
import sha1


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

class Callers:

	def GetUsers(self,value):
		perms = list([''.join(p) for p in permutations('3c8c34a2')])
		#print(perms[0])
		users = []
		#print (users)
		for x in range (0,value):
		 users.append(perms[x] + '6d197249')
		 #print(x)
		#print(users)
		return(users)	


	def GD_Call(self,uid):
		GDCall = GD_Variable(uid)
		print("GD_Request: ", GDCall.urlD, json.dumps(GDCall.bodyD), GDCall.HeaderD)
		post_response = requests.post(GDCall.urlD, data=json.dumps(GDCall.bodyD), headers=GDCall.HeaderD)
		return post_response

	def Aacmi_Call(self,uid):
		post_response = self.GD_Call(uid)
		response_GD = post_response.json()
		AacmiCall = Aacmi_Variable(response_GD['services']['aacmi'],uid)
		print("Aacmi_Request: ",AacmiCall.urlD, json.dumps(AacmiCall.bodyD), AacmiCall.HeaderD)
		post_responseAacmi = requests.post(AacmiCall.urlD, data=json.dumps(AacmiCall.bodyD), headers=AacmiCall.HeaderD)
		return post_responseAacmi

	def V0_authPacket (self,AUTH_REQUEST, VER_ZERO, token, sig, socket): 
		#buf is the packet to be sent
		sig_len = 4
		tokenLen = 24
		bodyLen = 2 + tokenLen + sig_len + 2
		buf = []
		pos = 0
		#Adding (Auth_req + VER) to buf
		myArray = array('B', [(AUTH_REQUEST << 4) + VER_ZERO])
		for x in myArray:
			buf.append(x)
		pos += 1
		#Adding bodyLen to buf
		low = (bodyLen & 0x00ff)
		high = ((bodyLen & 0xff00) >> 8)
		myArray = array('B', [high, low])
		for x in myArray:
			buf.append(x)
		pos += 2
		#Adding tokenLen to buf
		low = (tokenLen & 0x00ff)
		high = ((tokenLen & 0xff00) >> 8)
		myArray = array('B', [high, low])
		for x in myArray:
			buf.append(x)
		pos += 2
		i = 0
		#Adding Token to buf
		for item in token:
			buf.append(item)
		pos += tokenLen
		#Adding Siglen to buf 
		low = (sig_len & 0x00ff)
		high = ((sig_len & 0xff00) >> 8)
		myArray = array('B', [high, low])
		for x in myArray:
			buf.append(x)
		pos += 2
		#Adding Sig to buf
		for item in sig:
			buf.append(item)
		pos += sig_len
		print(token)
		print(buf)
		#Creating bytearray packet
		packet = str(bytearray(buf))
		appendData = "\nGET / HTTP/1.1\r\nHost: www.datami.com\r\nUser-Agent: curl/7.51.0\r\nAccept: */*\r\n\r\n"
		packet += appendData
		print(packet)
		x=0
		tot_bytes = 0
		socket.send(packet) #Packet Sent
		while True :
			if(len(socket.recv(1024))==0): 
				socket.close()
				break;
			tot_bytes+=len(socket.recv(1024))
			print(socket.recv(1024))
			x+=1
		print(tot_bytes)

	def V1_authPacket(self,AUTH_REQUEST, VER_ONE, token, socket): 
	  tokenLen=int(24)
	  signatureLen=int(40)
	  encodedToken = ""
	  encodedToken += str((base64.b64encode(bytes(token))).decode("utf-8")) #encoding in base64
	  encodedTokenLen = len(encodedToken)+1
	  print('encodedTokenLen :', encodedTokenLen)
	  bodyLen=0
	  pos=0
	  written_len = 0
	  respond=1
	  with open('Aacmi_Call.json') as f:
	 	data = json.load(f)
	  appId = str(data["Body"]["auth"]["appId"])
	  print("signatureLen: ",sys.getsizeof(signatureLen))
	  bodyLen = 2 + encodedTokenLen + 2 + 8 + 40 + 1
	  buf = []
	  req_buf = []
	  pos_req = 0
	  myArray = array('B', [(AUTH_REQUEST << 4) + VER_ONE])
	  for x in myArray:
	    req_buf.append(x)
	  pos_req+=1
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
	  tym = int(time.time()*1000)
	  print("Time: ", tym)
	  p = int_to_bytes1(tym,8)
	  for item in p:
	    buf.append(item)
	  pos+=8
	  print("Buf after adding timestamp: ", buf)

	  #Adding Signature len
	  low = (signatureLen & 0x00ff);
	  high = ((signatureLen & 0xff00) >> 8)
	  buf.append(high)
	  buf.append(low)
	  pos+=2

	  ts_str = str(tym)
	  
	  buf2 = token + ts_str + appId

	  print("signatureLen: ", signatureLen)
	  print("This is buf2")
	  print(buf2)
	  
	  #encrypting in SHA1
	  digest = []
	  digest = sha1.sha1(buf2)

	  print("This is digest")
	  print(digest)

	  result = ""
	  x=0
	  result+="".join("{:08x}".format(c) for c in digest)
	  #result+="".join("{:08x} ".format(ord(c)) for c in digest)
	  print("This is result:")
	  print(result)
	  print("signatureLen :",len(result))
	  
	  # Putting digest key in buffer
	  for item in result:
	   buf.append(ord(item))
	  pos += 40
	  print("This is buf after adding result")
	  print(buf)

	  print("This is buf")
	  packet2 = str(bytearray(buf))
	  print("".join("{:02x} ".format(ord(c)) for c in packet2))
	  print(buf)
	  print(len(buf))
	  pack = ""
	  for item in buf:
	    pack+=str(item)
	  print(pack)
	  
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
	  req_buf = req_buf + buf
	   #print(x)
	  pos_req+=pos
	  print("This is req_buf with buf")
	  print(req_buf)

	  packet = str(bytearray(req_buf))
	  print("This is req_buf packet: ")
	  print(packet)
	  print("This is req_buf hex packet: ")
	  print(" ".join("{:02x}".format(ord(c)) for c in list(packet)))
	  appendData = "\nGET / HTTP/1.1\r\nHost: www.datami.com\r\nUser-Agent: curl/7.51.0\r\nAccept: */*\r\n\r\n"
	  packet += appendData
	  print(packet)
	  x=0
	  tot_bytes = 0
	  socket.send(packet)
	  while True :
	    #print(x)
	    if(len(socket.recv(1024))==0): 
	      socket.close()
	      break;
	    tot_bytes+=len(socket.recv(1024))
	    print(socket.recv(1024))
	    x+=1
	  print(tot_bytes)

	def V3_authPacket (self,AUTH_REQUEST, VER_THREE, token, socket): 
	  tokenLen=int(24)
	  signatureLen=int(40)
	  encrypt_key_number = int(5)
	  encodedToken = ""
	  encodedToken += str((base64.b64encode(bytes(token))).decode("utf-8")) #encoding in base64
	  encodedTokenLen = len(encodedToken)+1
	  print('encodedTokenLen :', encodedTokenLen)
	  bodyLen=0
	  pos=0
	  written_len = 0
	  respond=1
	  with open('Aacmi_Call.json') as f:
	 	data = json.load(f)
	  appId = str(data["Body"]["auth"]["appId"])
	  skeys = ["SM62KphYVQN1Y1OI", "O2bxWuezJ5JhrdeZ", "Yab4V6u8pzM3h9u8", "mvLDu0c0tKw8fEd5", "K6Ja3ZsVF2WvBWsA", "7NPs6Q4xXddwUVVV", "HmbJ6zGm5qddMiie", "sMyypdfUnXaPUS3g", "IrrsXwfr4CCD9MuQ", "rzQ3HlVbtNVIQSrv"]
	  buffr = "{\"isFg\" : \"true\",\"userId\" : \"testUser:79eec5bdfe7c6f03\",\"dUid\" : \"79eec5bdfe7c6f03\",\"dMk\" : \"HMD Global\",\"dMl\" : \"TA-1021\",\"mccMnc\" : \"405-53\"} }"
	  print("Buffer: ", buffr)
	  written_len = len(buffr) 
	  print("signatureLen: ",sys.getsizeof(signatureLen))
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
	  #buf.append(0)
	  #pos+=1
	  tym = int(time.time()*1000)
	  print("Time: ", tym)
	  #tym = 1528200938
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

	  print("signatureLen: ", signatureLen)
	  print("This is buf2")
	  print(buf2)
	  
	  #encrypting in SHA1
	  #encrypting in SHA1
	  digest = []
	  digest = sha1.sha1(buf2)

	  print("This is digest")
	  print(digest)

	  result = ""
	  x=0
	  result+="".join("{:08x}".format(c) for c in digest)
	  #result+="".join("{:08x} ".format(ord(c)) for c in digest)
	  print("This is result:")
	  print(result)
	  print("signatureLen :",len(result))
	  
	  # Putting digest key in buffer
	  for item in result:
	   buf.append(ord(item))
	  pos += 40
	  print("This is buf after adding result")
	  print(buf)

	  
	  #Adding payload length
	  low = (len(buffr) & 0x00ff);
	  high = ((len(buffr) & 0xff00) >> 8)
	  buf.append(high)
	  buf.append(low)
	  pos+=2

	  
	  for item in buffr:
	    buf.append(ord(item))
	  #buf.append(0)
	  pos+=len(buffr)
	  print("This is buf after adding buffer: ")
	  print(buf)
	  print("This is buf")
	  packet2 = str(bytearray(buf))
	  print("".join("{:02x} ".format(ord(c)) for c in packet2))
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
	  #encrypted[pos] = 0
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
	  tot_bytes = 0
	  print("Response: ", socket.send(packet))
	  while True :
	    #print(x)
	    if(len(socket.recv(1024))==0): 
	      socket.close()
	      break;
	    tot_bytes+=len(socket.recv(1024))
	    print(socket.recv(1024))
	    x+=1
	  print(tot_bytes)


	def V_AuthCall(self,uid,version):
		post_responseAacmi = self.Aacmi_Call(uid)
		response_Aacmi = post_responseAacmi.json()
		print("-------")
		print("Response Aacmi ",response_Aacmi)
		print("-------")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = response_Aacmi['data']['sdHost']
		port = response_Aacmi['data']['sdPort']
		tkn = json.dumps(response_Aacmi['data']['zMiAuthToken'])
		token = ""
		for i in tkn:
			if i!='"':
				token+=i
		print("Token" , token)
		s.connect((host, port))
		if(version==0):
			self.V0_authPacket(10,0,token, "temp", s)
		if(version==1):
			self.V1_authPacket(10,1,token, s)
		if(version==3):
			self.V3_authPacket(10,3,token, s)
		s.close()
		return token




