from polynomial import Polynomial
import math


### CALCULATE MODULAR INVERSE VIA EXTENDED EUCLIDEAN ALGORITHM ###
def modInverse(a, m):
    for x in range(1, m):
        if (((a % m) * (x % m)) % m == 1):
            return x
    return -1

### CONVERT DECIMAL TO BIANRY ###
def DecimalToBinary(n):
    return bin(n).replace("0b", "")


def CalculatePoints(multiple, primitive_P, the_a, the_mod):
    denominator = Polynomial(1, 0, 0)  # y^2
    denominatordev = denominator.derivative  # 2y
    first_dev = Polynomial(1, 0, 0, 0).derivative  # x^3 with devivative is 3x^2
    numerator = first_dev + the_a  # 3x^2 + c = 3x^2 + 2

    multiple_binary = DecimalToBinary(multiple)

    the_Ps = {}
    the_Ps["1P"] = primitive_P

    for i in range(1, len(multiple_binary)):
        eles = list(the_Ps.items())
        ### IF THE CURRENT BIT OF THE INTEGER IS 1, THEN DOUBLE P AND THEN ADD P ###
        if (multiple_binary[i] == "1"): 
            x1 = eles[-1][1][0]
            y1 = eles[-1][1][1]
            x2 = eles[-1][1][0]
            y2 = eles[-1][1][1]
            if (x1 == x2 and y1 != y2):
                x3 = math.inf
                y3 = math.inf
            elif (x1 == x2 and y1 == y2):
                s = ((numerator.calculate(x1) % the_mod) * (
                    modInverse(denominatordev.calculate(y1), the_mod))) % the_mod
                x3 = (s * s - x1 - x2) % the_mod
                y3 = ((s * (x1 - x3)) - y1) % the_mod
            elif (x1 == math.inf and y1 == math.inf):
                x3 = x2
                y3 = y2
            else:
                s = (((y2 - y1) % the_mod) * (modInverse((x2 - x1), the_mod))) % the_mod
                x3 = (s * s - x1 - x2) % the_mod
                y3 = ((s * (x1 - x3)) - y1) % the_mod

            new_P = (x3, y3)
            the_Ps[str(int(eles[-1][0][:-1]) * 2) + "P"] = new_P

            eles_add = list(the_Ps.items())
            x1_add = eles_add[-1][1][0]
            y1_add = eles_add[-1][1][1]
            x2_add = primitive_P[0]
            y2_add = primitive_P[1]
            if (x1_add == x2_add and y1_add != y2_add):
                x3_add = math.inf
                y3_add = math.inf
            elif (x1_add == x2_add and y1_add == y2_add):
                s_add = ((numerator.calculate(x1_add) % the_mod) * (
                    modInverse(denominatordev.calculate(y1_add), the_mod))) % the_mod
                x3_add = (s_add * s_add - x1_add - x2_add) % the_mod
                y3_add = ((s_add * (x1_add - x3_add)) - y1_add) % the_mod
            elif (x1_add == math.inf and y1_add == math.inf):
                x3_add = x2_add
                y3_add = y2_add
            else:
                s_add = (((y2_add - y1_add) % the_mod) * (modInverse((x2_add - x1_add), the_mod))) % the_mod
                x3_add = (s_add * s_add - x1_add - x2_add) % the_mod
                y3_add = ((s_add * (x1_add - x3_add)) - y1_add) % the_mod

            new_P_add = (x3_add, y3_add)
            the_Ps[str((int(eles[-1][0][:-1]) * 2) + 1) + "P"] = new_P_add

        ### IF THE CURRENT BIT OF THE INTEGER IS 0, THEN JUST DOUBLE P ###
        else:
            x1 = eles[-1][1][0]
            y1 = eles[-1][1][1]
            x2 = eles[-1][1][0]
            y2 = eles[-1][1][1]
            if (x1 == x2 and y1 != y2):
                x3 = math.inf
                y3 = math.inf
            elif (x1 == x2 and y1 == y2):
                s = ((numerator.calculate(x1) % the_mod) * (
                    modInverse(denominatordev.calculate(y1), the_mod))) % the_mod
                x3 = (s * s - x1 - x2) % the_mod
                y3 = ((s * (x1 - x3)) - y1) % the_mod
            elif (x1 == math.inf and y1 == math.inf):
                x3 = x2
                y3 = y2
            else:
                s = (((y2 - y1) % the_mod) * (modInverse((x2 - x1), the_mod))) % the_mod
                x3 = (s * s - x1 - x2) % the_mod
                y3 = ((s * (x1 - x3)) - y1) % the_mod

            new_P = (x3, y3)
            the_Ps[str(int(eles[-1][0][:-1]) * 2) + "P"] = new_P

    return (int(the_Ps[str(multiple) + "P"][0]), int(the_Ps[str(multiple) + "P"][1]))
