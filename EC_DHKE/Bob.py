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
k_public_bob = NeededFunctions.CalculatePoints(k_private_bob, P, a, p)
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
shared_key = NeededFunctions.CalculatePoints(k_private_bob, A, a, p)
print("Shared Key is: " + str(shared_key))


