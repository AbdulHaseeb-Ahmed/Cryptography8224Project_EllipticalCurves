import json
import os.path
import time
from random import randint
import random
import functions
from polynomial import Polynomial
import pyaes
import hashlib



### GET THE DOMAIN PARAMETERS ###
with open("Domain_Parameters.txt", 'r') as file:
    EC_params = file.read()
EC_params = json.loads(EC_params)
print("The Domain Parameters Bob Recieved are: " + str(EC_params))
print()

a = int(EC_params['EC Param a'])
b = int(EC_params['EC Param b'])
p = int(EC_params['EC Param p'])
E = int(EC_params['EC Param E'])
P = tuple(EC_params['EC Param P'])

print("Elliptical Curve is: ")
elliptical_curve = Polynomial(1, 0, int(EC_params['EC Param a']), int(EC_params['EC Param b']))
print('y^2 = ' + str(elliptical_curve))
print()



### CACLUATE BOB's PRIVATE KEY (INTEGER) ###
good_private_key = False
while (good_private_key == False):
    k_private_bob = random.randint(2, (E - 1))
    if (k_private_bob % E == 0):
        continue
    else:
        good_private_key = True
print("Bob's Private Key is: " + str(k_private_bob))



### CACLUATE BOB'S PUBLIC KEY (POINT) ###
k_public_bob = functions.CalculatePoints(k_private_bob, P, a, p)
print("Bob's Public Key is: " + str(k_public_bob))

with open("Bob Public Key.txt", "w") as file:
    file.write(str(k_public_bob))
print()



### GET ALICE'S PUBLIC KEY (POINT) ###
while not os.path.exists("Alice Public Key.txt"):
    time.sleep(1)
    print("waiting for Alice's Public Key!")
if os.path.isfile("Alice Public Key.txt"):
    with open("Alice Public Key.txt", "r") as file:
        alice_public_key = file.readline()
else:
    raise ValueError("%s isn't a file!" % "Alice Public Key.txt")
print()

print("Alice's Public Key is: " + str(alice_public_key))
print()



### COMPUTE THE SHARED KEY ###
A = eval(alice_public_key)
shared_key = functions.CalculatePoints(k_private_bob, A, a, p)
print("Shared Key is: " + str(shared_key))


### GET ALICE'S CIPHERTEXT ###
while not os.path.exists("Alice Ciphertext.txt"):
    time.sleep(1)
    print("waiting for Alice's Ciphertext!")
if os.path.isfile("Alice Ciphertext.txt"):
    with open("Alice Ciphertext.txt", "r") as file:
        alice_ciphertext = file.readline()
else:
    raise ValueError("%s isn't a file!" % "Alice Ciphertext.txt")
print()

print("Alice's Ciphertext is: " + str(alice_ciphertext))
print()



### CONVERT ALICE'S CIPHERTEXT TO DECIMAL ###
ciphertext = [int(alice_ciphertext[i:i + 2], 16) for i in range(0, len(alice_ciphertext), 2)]
print("Alice's Ciphertext in Decimal:")
print(ciphertext)
print()




### COMPUTE AES KEY ###
x_hash = hashlib.md5(str(shared_key[0]).encode()).hexdigest().upper()
y_hash = hashlib.md5(str(shared_key[1]).encode()).hexdigest().upper()
AES_Key = x_hash[:8] + y_hash[:8]
print("AES Shared Key is: " + str(AES_Key))
print()

aes = pyaes.AES(AES_Key.encode())



### DECRYPT ###
decrypted = aes.decrypt(ciphertext)
print("Decrypted Text in Decimal:")
print(decrypted)
print()
print("Decrypted Text in Hex:")
hex_decrypted = [hex(x).lstrip("0x").rstrip("L").upper() for x in decrypted]
print(hex_decrypted)
print()
print("Decrypted Text in ASCII:")
hex_decrypted = [chr(x) for x in decrypted]
recieved_text = "".join(hex_decrypted)
print(recieved_text)
print()



