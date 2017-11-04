#! /usr/bin/python3

import pandas as pd
import sys
import re

def readCsvToDicts(filename,keyname):
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
notes = readCsvToDicts("note.csv","name")
note_texts = readCsvToDicts("note_text.csv", "key")
# There are no spawnflags.csv at the moment. We only have suspended and it is part if the QUAKED line
spawnflag_texts = readCsvToDicts("spawnflag_text.csv","key")


def printKeys(item_name):
    for item in key_texts:
        if (item_name in keys.keys()):
            keyLine = keys[item_name]
            if (item in keyLine.keys()):
                hasKey = keyLine[item]
                if (hasKey):
                    name = item
                    fullname = key_texts[item]["fullname"]
                    if (isinstance(fullname, str) and len(fullname)>0):
                        name = fullname
                    print("<"+key_texts[item]["type"]+" key=\""+item+"\" name=\""+name+"\">"+key_texts[item]["text"]+"</"+key_texts[item]["type"]+">")
                    
def printNotes(item_name):
    for item in note_texts:
        if (item_name in notes.keys()):
            keyLine = notes[item_name]
            if (item in keyLine.keys()):
                hasKey = keyLine[item]
                if (hasKey):
                    print(note_texts[item]["text"])
                    
def printSpawnflags(item_name):
    if ("suspended" in entities[item_name]["quaked"]):
        flagRow = spawnflag_texts["SUSPENDED"]
        print("<flag key=\""+flagRow["key"]+"\" name=\""+flagRow["fullname"]+"\" bit=\""+str(flagRow["bit"])+"\">"+flagRow["text"]+"</flag>")
            

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
    printSpawnflags(item)
    print("-------- NOTES --------")
    printNotes(item)
    print("  </point>")
print("</classes>")
