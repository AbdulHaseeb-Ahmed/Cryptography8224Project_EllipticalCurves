import json
import os.path
import time
from random import randint
import random
import NeededFunctions
from polynomial import Polynomial



### GET THE DOMAIN PARAMETERS ###
with open("Domain_Parameters.txt", 'r') as file:
    EC_params = file.read()
EC_params = json.loads(EC_params)
print("The Domain Parameters Alice Received are: " + str(EC_params))
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



### CACLUATE ALICE'S PRIVATE KEY (INTEGER) ###
good_private_key = False
while (good_private_key == False):
    k_private_alice = random.randint(2, (E - 1))
    if (k_private_alice % E == 0):
        continue
    else:
        good_private_key = True
print("Alice's Private Key is: " + str(k_private_alice))


### CACLUATE ALICE'S PUBLIC KEY (POINT) ###
k_public_alice = NeededFunctions.CalculatePoints(k_private_alice, P, a, p)
print("Alice's Public Key is: " + str(k_public_alice))

with open("Alice Public Key.txt", "w") as file:
    file.write(str(k_public_alice))
print()



### GET BOB'S PUBLIC KEY (POINT) ###
while not os.path.exists("Bob Public Key.txt"):
    time.sleep(1)
    print("waiting for Bob's Public Key!")
if os.path.isfile("Bob Public Key.txt"):
    with open("Bob Public Key.txt", "r") as file:
        bob_public_key = file.readline()
else:
    raise ValueError("%s isn't a file!" % "Bob Public Key.txt")
print()

print("Bob's Public Key is: " + str(bob_public_key))
print()



### COMPUTE THE SHARED KEY ###
B = eval(bob_public_key)
shared_key = NeededFunctions.CalculatePoints(k_private_alice, B, a, p)
print("Shared Key is: " + str(shared_key))
