# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

### UDP server - Authentication Server (A)

import socket
import os
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
import random
import time
import hashlib


#UDP_IP = "CHANGE TO PI'S IP"
#localIP     = "127.0.0.1"
#localPort   = 20001
localIP     = "127.0.0.1"
localPort   = 5005
bufferSize  = 1024

serverAddressPort_b = ("127.0.0.2", 20001)

### NB-IoT simulation specifications
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
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()
with open('private_pem.pem', 'w') as pr:
    pr.write(private_pem)
with open('public_pem.pem', 'w') as pu:
    pu.write(public_pem)
    
#Importing keys from files, converting it into the RsaKey object   
sk_key_a = RSA.import_key(open('private_pem.pem', 'r').read())
pk_key_a = RSA.import_key(open('public_pem.pem', 'r').read())
#sk_key_a = 0x89F7A70
#pk_key_a = 0x8416FF0

# Other public keys
sk_key_b = 0x8736A30
pk_key_b = 0x8499F90
sk_key_c = 0x87F0A50
pk_key_c = 0x8281D90

cipher_a = PKCS1_OAEP.new(key=pk_key_a)
decrypt_a = PKCS1_OAEP.new(key=sk_key_a)

na = "%032x" % random.randrange(16**32)
#ta = str(int(time.time()))
ta = '12345678'
tc = '23456789'
A = '0x00000000000000ab'  #address of A
###


msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort)) 

print("UDP listening")


# Listen for incoming datagrams
i=0
while(i<1):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    ### send 2 - A to C
    nc = message[4:35]
    hash2 = str(hashlib.sha256((na+nc).encode('utf-8')).hexdigest())
    hash2a = str(hashlib.sha256((na+ta).encode('utf-8')).hexdigest())
    M = cipher_a.encrypt((na+hash2a+hash2)[0:32])
    bytesToSend = decrypt_a.decrypt(M)
    
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
    i = i + 1
    ###
    
    
### send 3 - A to B
N = cipher_a.encrypt((A+tc+na+hash2a)[0:32])
bytesToSend1 = decrypt_a.decrypt(N)
UDPServerSocket.sendto(bytesToSend1, serverAddressPort_b)
###