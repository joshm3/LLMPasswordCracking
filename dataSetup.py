# Used to download and process the datasets into a standard csv format
# Note that analyzing the file is not necessary and can take a lot of time due to strength calculations

import os
from urllib.request import urlretrieve
from functools import reduce
from zxcvbn import zxcvbn
from sklearn.model_selection import train_test_split 
import pandas as pd
import sys
from math import isnan
import re
import csv

delimiterChar = '\t' #because I don't think this is a valid character in a password

def main():
    make_directories() #always

    # Option 1: "delete" delete files -> setup.py delete {dataset name}
    if (sys.argv[1] == "delete"):
        deleteAll(sys.argv[2])
        return

    # Option 2: "{dataset name}"download files -> setup.py {dataset name}
    if (sys.argv[1] in datasets):
        filename = sys.argv[1]
        download_file(filename)
        process_file(filename)
        split_file(filename)
        analyze_file(filename)
        return
    
    # Option 3: "all" download all the files
    if (sys.argv[1] == "all"):
        for filename in datasets:
            download_file(filename)
            process_file(filename)
            split_file(filename)
            analyze_file(filename)
        return
    
    print("ERROR: first argument must be delete, all, or <dataset name>")
    
#URLS here for downloading: (hashmob downloads are much slower)
datasets = {
    'rockyou': ('rockyou.txt', 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt'), #14m
    # 'ignis': ('ignis.txt','https://raw.githubusercontent.com/ignis-sec/Pwdb-Public/master/wordlists/ignis-10M.txt'), #10m
    #'linkedin': ('linkedin.found.1','https://cdn.hashmob.net/hashlists/1342/1342.100.found'), #60m TAKES TOO LONG
    'minecraft': ('minecraft.found.2', 'https://cdn.hashmob.net/hashlists/466/466.2811.found'), #151k
    'mangatraders': ('mangatraders.found.1', 'https://cdn.hashmob.net/hashlists/752/752.0.found'), #619k
    'battlefield': ('battlefield.found.1', 'https://cdn.hashmob.net/hashlists/541/541.0.found'), #420k
    # 'wanelo': ('wanelo.found.1', 'https://cdn.hashmob.net/hashlists/2925/2925.0.found'), #2 m
    # 'everydayrecipes': ('everydayrecipes.found.1', 'https://cdn.hashmob.net/hashlists/134/134.0.found'), #25k
    # 'dosportseasy': ('dosportseasy.found.1', 'https://cdn.hashmob.net/hashlists/268/268.100.found'), #45k
    #'wattpad': ('wattpad.found.1', 'https://cdn.hashmob.net/hashlists/4364/4364.3200.found'), #23 m TAKES TOO LONG
    #'zynga': ('zynga.found.1', 'https://cdn.hashmob.net/hashlists/740/740.27200.found') #48 m TAKES TOO LONG
    # 'yahoo': ('yahoo.found.1', 'https://cdn.hashmob.net/hashlists/623/623.100.found'),
    'shopback': ('shopback.found.2', 'https://cdn.hashmob.net/hashlists/1717/1717.120.found'),
    'aimware': ('aimware.found.2', 'https://cdn.hashmob.net/hashlists/4360/4360.2811.found')
}

# Function to create directories for datasets
def make_directories():
    if (not os.path.exists("./datasets")): os.mkdir("./datasets")
    if (not os.path.exists("./datasets/train")): os.mkdir("./datasets/train")
    if (not os.path.exists("./datasets/test")): os.mkdir("./datasets/test")
    

# Function to download files into directories
def download_file(filename):
    downloadName, url = datasets[filename]
    downloadPath = os.path.join("datasets", downloadName)
    if not os.path.exists(downloadPath):
        print("Downloading " + filename)
        urlretrieve(url, downloadPath)

# Function to process files into CSV format
def process_file(filename):
    for file in os.listdir("./datasets"):
        parts = file.split('.', 2)
        if not (parts[0] == filename): continue
        if not (parts[1] == "txt" or parts[1] == "found"): continue

        input_file = os.path.join("datasets", file)
        output_file = os.path.join("datasets", filename + ".csv")
        if os.path.exists(output_file): return

        print("Processing " + filename)
        
        
        if ".txt" in file:
            with open(input_file, 'r', encoding='latin1') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write("password\n")
                for line in f_in:
                    f_out.write(line.strip() + "\n") #FIX THIS!!!!!!!!!!!!!!
        if ".found" in file:
            passwordIndex = int(file[-1])
            with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write("password\n")
                for line in f_in:
                    pw = line.split(':', 2)[passwordIndex].strip()
                    if not pw == "":
                        f_out.write(pw + "\n")
        if ".comb" in filename:
            with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write("username" + delimiterChar + "password\n")
                print("username not ready yet")
                #not sure about this one yet
                #for line in f_in:
                    #writer.writerow([item.strip() for item in line.split(',')])


# Function to split CSV files into training and test sets
def split_file(filename):
    input_file = os.path.join("datasets", filename + ".csv")
    train_file = os.path.join("datasets", "train", filename + ".csv")
    test_file = os.path.join("datasets", "test", filename + ".csv")

    if os.path.exists(train_file) and os.path.exists(test_file): return

    print("Splitting " + filename)
    df = pd.read_csv(input_file, delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Labels

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    Xy_train = pd.concat([X_train, y_train], axis=1)
    Xy_train.to_csv(train_file, index=False, sep='\t')

    Xy_test = pd.concat([X_test, y_test], axis=1)
    Xy_test.drop_duplicates()
    Xy_test.to_csv(test_file, index=False, sep='\t')

def analyze_file(filename):
    print("Analyzing " + filename)
    input_file = os.path.join("datasets", filename + ".csv")
    df = pd.read_csv(input_file, delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
    df.drop_duplicates()

    length = len(df.index)
    print("length=" + str(length))

    df['strength'] = df.apply(getStrength, axis=1)
    averageStrength = df['strength'].sum() / length
    print("averageStrength=" + str(averageStrength))

    # minLength = 99
    # minCap = 99
    # minNum = 99
    # minSpecial = 99
    # for password in df['password']:
    #     if len(password) < minLength: minLength = len(password)
    #     if len(re.findall(r'[A-Z]',password)) < minCap: minCap = len(re.findall(r'[A-Z]',password))
    #     if len(re.findall(r'[0-9]',password)) < minNum: minNum = len(re.findall(r'[0-9]',password))
    #     if len(re.findall(r'[^A-Za-z0-9]',password)) < minSpecial: minSpecial = len(re.findall(r'[^A-Za-z0-9]',password))
    # print("minLength=" + str(minLength) + " minCap=" + str(minCap) + " minNum=" + str(minNum) + " minSpecial=" + str(minSpecial))

def getStrength(row):
    return(zxcvbn(row['password'])['score'])

def deleteAll(datasetName):
    folderPath = os.path.join("datasets")
    trainPath = os.path.join(folderPath, "train")
    testPath = os.path.join(folderPath, "test")
    for path in [folderPath, trainPath, testPath]:
        for filename in os.listdir(path):
            if datasetName in filename:
                filepath = os.path.join(path, filename)
                os.remove(filepath)

if __name__=="__main__": 
    main() 