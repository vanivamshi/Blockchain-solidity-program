# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 12:36:05 2021

@author: vamshi
"""

# for AES-128, set - secret_key = urandom(16)
# for AES-256, set - secret_key = urandom(32)

### UDP client - NB-IoT device (C)

import socket
import os
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
import random
import time
import hashlib


serverAddressPort_a   = ("127.0.0.1", 5005)
serverAddressPort_b   = ("127.0.0.2", 20001)
bufferSize          = 1024

#noise = 

### NB-IoT simulation specifications
def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 70    # bandwidth = 0.18M, tx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 70dBm
   return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)
###


####### RSA key generation
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
sk_key_c = RSA.import_key(open('private_pem.pem', 'r').read())
pk_key_c = RSA.import_key(open('public_pem.pem', 'r').read())
#print(type(pr_key), type(pu_key))#Instantiating PKCS1_OAEP object with the public key for encryption
#sk_key_c = 0x87F0A50
#pk_key_c = 0x8281D90

#Other keys
sk_key_a = 0x89F7A70
pk_key_a = 0x8416FF0
sk_key_b = 0x8736A30
pk_key_b = 0x8499F90

cipher_c = PKCS1_OAEP.new(key=pk_key_c)
cipher_a = PKCS1_OAEP.new(key=sk_key_a)
cipher_b = PKCS1_OAEP.new(key=pk_key_b)

decrypt_c = PKCS1_OAEP.new(key=sk_key_c)
#######


#Encrypting the message with the PKCS1_OAEP object
message1 = 'NReq'
nc = "%032x" % random.randrange(16**32)  #nonce - '0x' + "%032x" % random.randrange(16**32)
tc = str(int(time.time()))  #timestamp
OldID = '0x000000000000000a'  #old ID of C
C = '0x00000000000000aa'  #address of C
Rep = '6'

### send 1 - C to A
cipher_text1 = cipher_c.encrypt(message1+nc+tc+OldID+C)
decrypt_msg1 = decrypt_c.decrypt(cipher_text1)
#cipher_text1 = cipher_c.encrypt(cipher_a.encrypt(message1+nc+tc+OldID+C))

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


 
bytesToSend = decrypt_msg1
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort_a)
### 

### recv 3 - B to C
msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
###

### send 4 - C to B
na = msgFromServer[0]

hash2a = 'c46f30851f25887830ffd4ade03ded781d20b2f568e4d57b72a809ccf41692a1'
ta = '12345678'
hash2a = str(hashlib.sha256((na+ta).encode('utf-8')).hexdigest())
cipher_text2 = cipher_c.encrypt((message1+C+nc+Rep+ta+na+hash2a)[0:32])
decrypt_msg2 = decrypt_c.decrypt(cipher_text1)

bytesToSend2 = decrypt_msg2
UDPClientSocket.sendto(bytesToSend2, serverAddressPort_b)
###

### recv 5 - B to C
msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)

###


#print(na)
