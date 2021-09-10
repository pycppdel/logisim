#assembler for logisim cpu
#it gets called assembler.py [path to file]
#and outputs a file with a similar name decoded into hex

import sys
import os
import re

filename = sys.argv[1]

if not os.path.exists(filename):
    raise FileNotFoundError("This file does not exist")

#file is verified
#setting variables

names_to_hex = {

"sub": 0x0,
"add": 0x1,
"and":0x2,
"or": 0x3,
"mov": 0x4,
"ld": 0x5,
"hlt": 0x6,
}

try:
    name = filename.split(".")[0]
except Exception:
    name = filename

name += ".hex"

all_names_big_and_small = [el+"|"+el.upper()+"|" for el in names_to_hex]
names_pattern =""
for el in all_names_big_and_small:
    names_pattern += el

line_pattern = r"(sub|SUB|add|ADD|and|AND|or|OR|mov|MOV|ld|LD|hlt|HLT])\s+([[\-|0-9]+|AX|ax|BX|bx])"

bn_inc = 0

with open(name, "w") as f:
    f.write("v2.0 raw\n")
    #starting transformation
    with open(filename, "r") as rf:
        for el in rf.readlines():
            found = re.search(line_pattern, el)
            #transforming second word
            if found.groups()[1] == "ax" or found.groups()[1] == "AX":
                sec_2_w = hex(126)
            elif found.groups()[1] == "bx" or found.groups()[1] == "BX":
                sec_2_w = hex(127)
            else:
                if int(found.groups()[1]) > 0:
                    	sec_2_w = hex(int(found.groups()[1]))
                else:
                    u = int(found.groups()[1])*-1
                    zahl = 255-(u-1)
                    sec_2_w = hex(zahl)
            sec_2_w = sec_2_w.split("x")[1]
            #starting work
            f.write(str(names_to_hex[found.groups()[0].lower()])+" "+sec_2_w+" ")
            bn_inc += 1
            if bn_inc == 4:
                bn_inc = 0
                f.write("\n")
