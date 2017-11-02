#! /usr/bin/python3

import pandas as pd
import sys
import re

def readCsvToDicts(filename,keyname):
    #reader = csv.DictReader(open(filename,"r").read().replace('\r\n','\n'))
    #reader = pd.read_csv(filename, sep=',', engine='python')
    reader = pd.read_csv(filename)
    result = {}
    for row in reader.itertuples():
        rowDict = row._asdict()
        key = rowDict[keyname]
        if key in result:
            sys.exit("fatal error, the file: "+filename+" has double key: "+key)
        result[key] = rowDict
    return result

def fatal(errorMsg):
    print(errorMsg)
    exit(1)
    

print("<?xml version=\"1.0\"?>")

entities = readCsvToDicts("entities.csv","item")
keys = readCsvToDicts("keys.csv","name")
key_texts = readCsvToDicts("key_text.csv","key")
#print(keys)


def printKeys(item_name):
    for item in key_texts:
        if (item_name in keys.keys()):
            keyLine = keys[item_name]
            if (item in keyLine.keys()):
                hasKey = keyLine[item]
                if (hasKey):
                    print("<"+key_texts[item]["type"]+" key=\""+item+"\"",end="")
                    name = item
                    fullname = key_texts[item]["fullname"]
                    if (isinstance(fullname, str) and len(fullname)>0):
                        name = fullname
                    print (" name=\""+name+"\"", end = "");
                    print(">"+key_texts[item]["text"]+"</"+key_texts[item]["type"]+">")
            

print("<classes>")
for item in entities:
    row = entities[item]
    quaked = row["quaked"]
    model = ""
    p = re.compile('\((.+?)\)')
    parans = p.findall(quaked)
    try:
        color = parans[0] #re.search('\((.+?)\)', quaked).group(1)
    except AttributeError:
        fatal("Failed it find color in: "+quaked)
    if (len(parans) > 1):
        box1 = parans[1]
    if (len(parans) > 2):
        box2 = parans[2]
    if isinstance(row["model"],str):
        model = row["model"]
    print("  <point name=\"" + item + "\" color=\""+color+"\"", end ="")
    if (box1 and box2):
        print(" box=\""+box1+" "+box2+"\"", end = "")
    print(" model=\""+model+"\">")
    if isinstance(row["description"],str):
        print(row["description"])
    print("-------- KEYS --------")
    printKeys(item)
    print("-------- SPAWNFLAGS --------")
    print("-------- NOTES --------")
    print("  </point>")
print("</classes>")
