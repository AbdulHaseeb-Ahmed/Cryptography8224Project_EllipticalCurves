import json
from polynomial import Polynomial

domain_params = {}
ECC_params_state = False
while (ECC_params_state == False):
    print("Enter elliptical curve parameters: ")
    domain_params['EC Param a'] = int(input("Enter a in HEX: "), 16)
    domain_params['EC Param b'] = int(input("Enter b in HEX: "), 16)
    domain_params['EC Param p'] = int(input("Enter modulus p in HEX: "), 16)
    x = int(input("Enter point P's x-coordiante in HEX: "), 16)
    y = int(input("Enter point P's y-coordiante in HEX: "), 16)
    domain_params['EC Param P'] = (x, y)
    domain_params['EC Param E'] = int(input("Enter #E in HEX: "), 16)

### MAKE SURE CONDITION OF 4*a^3 + 27*b^2 != 0 mod p HOLDS OTHERWISE RE-ENTER PARAMETERS ###
    if ((((4 * pow(int(domain_params['EC Param a']), 3)) + (27 * pow(int(domain_params['EC Param b']), 2))) % int(domain_params['EC Param p'])) == 0):
        print("Invalid elliptical curve parameters!")
        print()
        continue
    else:
### MAKE SURE THE MODULUS p IS LARGER THAN 3 ###
        if (int(domain_params['EC Param p']) < 3):
            print("Modolus is too small!")
            print()
            continue
        else:
            ECC_params_state = True


### PRINT WHAT THE ELIPTICAL CURVE LOOKS LIKE ###
print("Elliptical Curve is: ")
elliptical_curve = Polynomial(1, 0, int(domain_params['EC Param a']), int(domain_params['EC Param b']))
print('y^2 = ' + str(elliptical_curve))
print()

elliptic_curve_paras = f"y^2 = x^3 + {domain_params['EC Param a']}x + {domain_params['EC Param b']}" \
                       f" mod {domain_params['EC Param p']}"
print("The elliptical curve is: " + str(elliptic_curve_paras))
print("The elliptical curve #E parameter is: " + str(domain_params['EC Param E']))
print("The elliptical curve P parameter point is: " + str(domain_params['EC Param P']))

### SAVE THE DOMAIN PARAMETERS TO A FILE SO THAT THE PARTIES CAN ACCESS IT LATER ###
json = json.dumps(domain_params)
file = open("Domain_Parameters.txt", "w")
file.write(json)
file.close()
