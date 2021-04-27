import json
from polynomial import Polynomial
import math
import os.path
import time
from random import randint
import NeededFunctions



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
print()



### MESSAGE TO ENCRYPT ###
msg = input("Enter Message to send: ")
print("Plaintext is: " + str(msg))
msg_len = len(msg)
msg_hex = []
for i in range(0, msg_len):
    char_to_hex = hex(ord(msg[i])).lstrip("0x").rstrip("L")
    first_hex = str(char_to_hex[0]).upper()
    second_hex = str(char_to_hex[1]).upper()
    msg_hex.append(first_hex)
    msg_hex.append(second_hex)

stuff_to_send_bob = []
i = 0
while (i < len(msg_hex)):
    ### CACLUATE ALICE'S PRIVATE KEY (INTEGER) ###
    good_private_key = False
    while (good_private_key == False):
        k_private_alice = randint(2, (E - 1))
        if (k_private_alice % E == 0):
            continue
        else:
            good_private_key = True

    ### CACLUATE ALICE'S EPHEMERAL KEY (POINT) ###
    k_ephemeral_alice = NeededFunctions.CalculatePoints(k_private_alice, P, a, p)

    ### CALCULATE MASKING KEY ###
    B = eval(bob_public_key)
    masking_key = NeededFunctions.CalculatePoints(k_private_alice, B, a, p)

    if(int(masking_key[0]) == 0):
        continue

    ### ENCRYPT THE MESSAGE ###
    enc_msg = ((int(msg_hex[i], 16) + 1) * int(masking_key[0])) % p
    stuff_to_send_bob.append([int(k_ephemeral_alice[0]), int(k_ephemeral_alice[1]), enc_msg])

    i += 1

with open("Alice Stuff for Bob.txt", "w") as file:
    for items in stuff_to_send_bob:
        file.write('%s\n' % items)
print()
