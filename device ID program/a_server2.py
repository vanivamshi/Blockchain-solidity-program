# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#cd Desktop
#sudo mkdir receive
#cd receive
#sudo nano receive.py

### UDP server - Data Server (B)

import socket
import os
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
import random
import time


### UDP_IP = "CHANGE TO PI'S IP"
#localIP     = "127.0.0.2"
#localPort   = 20001
localIP     = "127.0.0.2"
localPort   = 20001
bufferSize  = 1024

serverAddressPort_a = ("127.0.0.1", 5005)

# NB-IoT simulation specifications
def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 40    # bandwidth = 0.18M, rx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 40dBm
   return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)
###

### RSA key generation
private_key = RSA.generate(1024)
#Generating the public key (RsaKey object) from the private key
public_key = private_key.publickey()
#print(type(private_key), type(public_key))#Converting the RsaKey objects to string 
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()
#print(type(private_pem), type(public_pem))#Writing down the private and public keys to 'pem' files
with open('private_pem.pem', 'w') as pr:
    pr.write(private_pem)
with open('public_pem.pem', 'w') as pu:
    pu.write(public_pem)
    
#Importing keys from files, converting it into the RsaKey object   
sk_key_b = RSA.import_key(open('private_pem.pem', 'r').read())
pk_key_b = RSA.import_key(open('public_pem.pem', 'r').read())
#sk_key_b = 0x8736A30
#pk_key_b = 0x8499F90

# Other public keys
sk_key_a = 0x89F7A70
pk_key_a = 0x8416FF0
sk_key_c = 0x87F0A50
pk_key_c = 0x8281D90

cipher_b = PKCS1_OAEP.new(key=pk_key_b)
decrypt_b = PKCS1_OAEP.new(key=sk_key_b)
###

message2 = 'RApp'
UID = '0x00000000000000bb'
SEC = '0x0000000000000011'
tb = '345678901'
nb = "%032x" % random.randrange(16**32)


msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)
 

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort)) 

print("UDP listening")
 

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

   

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
    
    ### send 5 - B to C
    cipher_text3 = cipher_b.encrypt((message2+UID+SEC+tb+nb)[0:32])
    decrypt_msg3 = decrypt_b.decrypt(cipher_text3)

    bytesToSend3 = decrypt_msg3
    UDPServerSocket.sendto(bytesToSend3, address)

    ###
