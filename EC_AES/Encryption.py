import AES_Key_Generation
import hashlib
import numpy as np
from itertools import chain

vhex = np.vectorize(hex)

s_box = np.array([
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
])

r_con = np.array([
    [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
])

def xor(a, b, n):
    ans = ""

    # Loop to iterate over the
    # Binary Strings
    for i in range(n):

        # If the Character matches
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans

def key_state(input_list):
    key_state = np.zeros([4, 4], dtype=object)
    index = 0
    for row in range(0, 4):
        for col in range(0, 4):
            key_state[col][row] = input_list[index]
            index = index + 1
    return key_state


def State_Matrix_and_Round_Key(text, key):
    text_matrix = key_state(text)

    key_matrix = key_state(key)

    new_matrix = np.zeros([4, 4], dtype=object)
    for i in range(0, 4):
        for j in range(0, 4):
            text_val = int("{0:08b}".format(int(text_matrix[i][j], 16)), 2)
            key_val = int("{0:08b}".format(int(key_matrix[i][j], 16)), 2)
            val = hex(text_val ^ key_val).lstrip("0x").rstrip("L").upper()
            if val == "":
                new_matrix[i][j] = "00"
            elif len(val) != 2:
                new_matrix[i][j] = "0" + val
            else:
                new_matrix[i][j] = val

    return new_matrix


def Sub_State_Matrix(State_Matrix):
    sub_matrix = np.zeros([4, 4], dtype=object)
    for i in range(0, 4):
        for j in range(0, 4):
            row = int(State_Matrix[i][j][0], 16)
            col = int(State_Matrix[i][j][1], 16)
            val = hex(s_box[row][col]).lstrip("0x").rstrip("L").upper()
            if (val == ""):
                sub_matrix[i][j] = "00"
            else:
                sub_matrix[i][j] = val

    return sub_matrix

def Sub_State_Matrix_2(State_Matrix):
    State_Matrix = key_state(State_Matrix)
    sub_matrix = np.zeros([4, 4], dtype=object)
    for i in range(0, 4):
        for j in range(0, 4):
            row = int(State_Matrix[i][j][0], 16)
            col = int(State_Matrix[i][j][1], 16)
            val = hex(s_box[row][col]).lstrip("0x").rstrip("L").upper()
            if (val == ""):
                sub_matrix[i][j] = "00"
            else:
                sub_matrix[i][j] = val

    return sub_matrix

def Shift_Rows(State_Matrix):
    for i in range(0, 4):
        State_Matrix[i] = np.roll(State_Matrix[i], -i)
    return State_Matrix

def Mix_Column(State_Matrix):
    result = np.zeros([4, 4], dtype="int")
    mixcol = np.array([["00000010", "00000011", "00000001", "00000001"],
                       ["00000001", "00000010", "00000011", "00000001"],
                       ["00000001", "00000001", "00000010", "00000011"],
                       ["00000011", "00000001", "00000001", "00000010"]])
    bin_State_Matrix = np.zeros([4, 4], dtype=object)
    for i in range(0, 4):
        for j in range(0, 4):
            bin_State_Matrix[i][j] = "{0:08b}".format(int(State_Matrix[i][j], 16))

    new_matrix = np.zeros([4, 4], dtype=object)
    for i in range(len(mixcol)):
        # iterate through columns of Y
        for j in range(len(bin_State_Matrix[0])):
            # iterate through rows of Y
            vals = []
            for k in range(len(bin_State_Matrix)):
                if (mixcol[i][k] == "00000001"):
                    mixval = int(mixcol[i][k], 2)
                    stateval = int(bin_State_Matrix[k][j], 2)
                    result = "{0:08b}".format(mixval * stateval)
                    vals.append(result)
                elif (mixcol[i][k] == "00000010" and bin_State_Matrix[k][j][0] == '0'):
                    mixval = int(mixcol[i][k], 2)
                    stateval = int(bin_State_Matrix[k][j], 2)
                    result = "{0:08b}".format(mixval * stateval)
                    vals.append(result)
                elif (mixcol[i][k] == "00000010" and bin_State_Matrix[k][j][0] == '1'):
                    mixval = int(mixcol[i][k], 2)
                    stateval = int(bin_State_Matrix[k][j], 2)
                    tmp = "{0:08b}".format(mixval * stateval)
                    result = xor(tmp[1:], "00011011", 8)
                    vals.append(result)
                elif (mixcol[i][k] == "00000011"):
                    if (bin_State_Matrix[k][j][0] == '0'):
                        mixval = int("00000010", 2)
                        stateval = int(bin_State_Matrix[k][j], 2)
                        val2 = "{0:08b}".format(mixval * stateval)
                    else:
                        mixval = int("00000010", 2)
                        stateval = int(bin_State_Matrix[k][j], 2)
                        tmp = "{0:08b}".format(mixval * stateval)
                        val2 = xor(tmp[1:], "00011011", 8)

                    mixval = int("00000001", 2)
                    stateval = int(bin_State_Matrix[k][j], 2)
                    val1 = "{0:08b}".format(mixval * stateval)
                    result = xor(val2, val1, len(val1))
                    vals.append(result)

            tmp = xor(vals[0], vals[1], len(vals[0]))
            tmp2 = xor(tmp, vals[2], len(vals[2]))
            tmp3 = xor(tmp2, vals[3], len(vals[3]))
            if len(hex(int(tmp3, 2)).lstrip("0x").rstrip("L").upper()) == 2:
                new_matrix[i][j] = hex(int(tmp3, 2)).lstrip("0x").rstrip("L").upper()
            else:
                new_matrix[i][j] = "0" + hex(int(tmp3, 2)).lstrip("0x").rstrip("L").upper()

    return new_matrix

def Round_Output(State_Matrix, Next_Round_Key):
    key_matrix = key_state(Next_Round_Key)

    round_output = np.zeros([4, 4], dtype=object)
    for i in range(0, 4):
        for j in range(0, 4):
            text_val = int("{0:08b}".format(int(State_Matrix[i][j], 16)), 2)
            key_val = int("{0:08b}".format(int(key_matrix[i][j], 16)), 2)
            val = hex(text_val ^ key_val).lstrip("0x").rstrip("L").upper()
            if val == "":
                round_output[i][j] = "00"
            elif len(val) != 2:
                round_output[i][j] = "0" + val
            else:
                round_output[i][j] = val

    return round_output


def Convert_Round_Output(State_Matrix, k):
    output = []
    for i in range(0, 4):
        output.append(State_Matrix[:,i].tolist())
    flatten_output = [j for sub in output for j in sub]

    return flatten_output





def __main__(key, plaintext):
    Key_Schedule = AES_Key_Generation.key_sch(key)

    hex_plaintext = []
    for i in plaintext:
        hex_plaintext.append(hex(ord(i)).lstrip("0x").rstrip("L").upper())
    print("Plaintext is: " + str(plaintext))
    print("Hex Plaintext:")
    print(hex_plaintext)
    print()
    dec_plaintext = [int(hex_plaintext[i], 16) for i in range(0, len(hex_plaintext))]
    print("Plaintext in Decimal:")
    print(dec_plaintext)
    print()

    the_outputs = []
    the_outputs.append(hex_plaintext)
    for i in range(0, 10):
        if i == 0:
            Step_1 = State_Matrix_and_Round_Key(the_outputs[-1], Key_Schedule[i])
            Step_2 = Sub_State_Matrix(Step_1)
            Step_3 = Shift_Rows(Step_2)
            Step_4 = Mix_Column(Step_3)
            Step_5 = Round_Output(Step_4, Key_Schedule[i + 1])
            Step_6 = Convert_Round_Output(Step_5, i+1)
        elif i == 9:
            Step_2 = Sub_State_Matrix_2(the_outputs[-1])
            Step_3 = Shift_Rows(Step_2)
            Step_5 = Round_Output(Step_3, Key_Schedule[i + 1])
            Step_6 = Convert_Round_Output(Step_5, i + 1)
        else:
            Step_2 = Sub_State_Matrix_2(the_outputs[-1])
            Step_3 = Shift_Rows(Step_2)
            Step_4 = Mix_Column(Step_3)
            Step_5 = Round_Output(Step_4, Key_Schedule[i+1])
            Step_6 = Convert_Round_Output(Step_5, i+1)
        the_outputs.append(Step_6)

    ciphertext = "".join(the_outputs[-1])

    return ciphertext
