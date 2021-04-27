import random
import json
from polynomial import Polynomial
import math
import os.path
import time
import ast
import NeededFunctions


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
    k_private_bob = random.randint(2, int(EC_params['EC Param E']))
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
while not os.path.exists("Alice Stuff for Bob.txt"):
    time.sleep(1)
    print("waiting for Alice!")
if os.path.isfile("Alice Stuff for Bob.txt"):
    with open("Alice Stuff for Bob.txt", "r") as file:
        encrypted_message = []
        for line in file:
            encrypted_message.append(ast.literal_eval(line))
else:
    raise ValueError("%s isn't a file!" % "Alice Stuff for Bob.txt")
print()

decrypted_hex = []
for i in range(0, len(encrypted_message)):
    ### ALICES EPHEMERAL KEY ###
    A = (encrypted_message[i][0], encrypted_message[i][1])

    ### MASKING KEY ####
    masking_key = NeededFunctions.CalculatePoints(k_private_bob, A, a, p)

    ### INVERSE OF MASKING KEY X COORDINATE ###
    inverse = NeededFunctions.gcdExtended(p, int(masking_key[0]))

    ### DECRYPTION ###
    val = hex(((int(encrypted_message[i][2]) * inverse[2]) - 1) % p).lstrip("0x").rstrip("L").upper()
    if len(val) == 0:
        val = str(0)
    decrypted_hex.append(val)

hexes = []
for i in range(0, len(decrypted_hex), 2):
    val = str(decrypted_hex[i]) + str(decrypted_hex[i + 1])
    hexes.append(str(val))
print("The recieved hex values are: ")
print(hexes)
print()

decrypted_msg = ""
for i in range(0, len(hexes)):
    bytes_object = bytes.fromhex(hexes[i])
    ascii_string = bytes_object.decode("ASCII")
    decrypted_msg = decrypted_msg + ascii_string

print("The decrypted message is: " + str(decrypted_msg))
