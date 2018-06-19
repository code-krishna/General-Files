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
import unittest
from Variables import GD_Variable, Aacmi_Variable
from Helpers import Callers
import xml.dom.minidom as minidom


class TestGateway(unittest.TestCase):

 @classmethod
 def setUpClass(cls):
  print("Setup started")
 
 def test_GDCall(self):
  caller = Callers()
  doc = minidom.parse("MyFile.xml")
  nusers = doc.getElementsByTagName("usersGD")
  for n in nusers:
    no_users = int(n.getAttribute("users"))
  users = caller.GetUsers(no_users)
  for uid in users:
   #print(uid)
   post_response = caller.GD_Call(uid)
   response_GD = post_response.json()
   print("-----")
   print("Response_GD",response_GD)
   print("-----")
   self.assertEqual(post_response.status_code,200)
 

 def test_AacmiCall(self):
  caller = Callers()
  doc = minidom.parse("MyFile.xml")
  nusers = doc.getElementsByTagName("usersAacmi")
  for n in nusers:
    no_users = int(n.getAttribute("users"))
  users = caller.GetUsers(no_users)
  for uid in users:
    post_responseAacmi = caller.Aacmi_Call(uid)
    response_Aacmi = post_responseAacmi.json()
    print("-----")
    print("response_Aacmi",response_Aacmi)
    print("-----")
    self.assertEqual(post_responseAacmi.status_code,200)

 def test_Gateway(self):
  caller = Callers()
  doc = minidom.parse("MyFile.xml")
  nusers = doc.getElementsByTagName("usersAuth")
  for n in nusers:
    no_users = int(n.getAttribute("users"))
  users = caller.GetUsers(no_users)
  ver = doc.getElementsByTagName("AuthVersion")
  for n in ver:
    version = int(n.getAttribute("version"))
  Tokens = []
  for uid in users:
   print(uid)
   Tokens.append(caller.V_AuthCall(uid,version))
  print(Tokens)
  post_responseAacmi = caller.Aacmi_Call('3c8c34a26d197249')
  response_Aacmi = post_responseAacmi.json()
  host = response_Aacmi['data']['sdHost']
  port = response_Aacmi['data']['sdPort']
  

  print(doc.nodeName)
  print(doc.firstChild.tagName)

  expertise = doc.getElementsByTagName("Interval")
  for skill in expertise:
    myArray = skill.getAttribute("GatewayPing")
  myArray = myArray.split(' ')
  
  myArray = [int(i) for i in myArray]
  #print(myArray)

  i=0
  TimeArray = []
  for p in myArray:
    TimeArray.append(p-i)
    i = p
  print(TimeArray)
 
  for tym in TimeArray:
    time.sleep(tym)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    for token in Tokens:
      print("Token : ",token)
      if(version==0) :
        caller.V0_authPacket(10,0,token, "temp", s)
      if(version==1):
        caller.V1_authPacket(10,1,token, s)
      if(version==3):
        caller.V3_authPacket(10,3,token, s)

 @classmethod
 def tearDownClass(cls):
   print("Tear Down started")

suite = unittest.TestLoader().loadTestsFromTestCase(TestGateway)
unittest.TextTestRunner(verbosity=2).run(suite)
