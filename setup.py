import os
from urllib.request import urlretrieve
from functools import reduce
from password_strength import PasswordStats
from sklearn.model_selection import train_test_split 
import pandas as pd
import sys
import platform

def main():
    make_directories() #always

    if (sys.argv[1] == "clear"): 
        type = sys.argv[2]
        if not type in ['contextless', 'domain', 'username']:
            print("Type must be in {contextless, domain, username}")
        clear_folder(type)
        return
    
    type = sys.argv[1]
    if not type in ['contextless', 'domain', 'username']:
        print("Type must be in {contextless, domain, username}")

    download_files(type)
    process_files(type)
    split_files(type)
    analyze_folder(type)

#URLS here for downloading: ()

contextless = [
    ('rockyou', 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt'), #14m
    ('ignis','https://raw.githubusercontent.com/ignis-sec/Pwdb-Public/master/wordlists/ignis-10M.txt'), #10m
    ('linkedin.found','https://cdn.hashmob.net/hashlists/1342/1342.100.found') #60m
]

domain = [
    ('minecraft.found', 'https://cdn.hashmob.net/hashlists/466/466.2811.found'), #149k
    ('mangatraders.found', 'https://cdn.hashmob.net/hashlists/752/752.0.found'), #619k
    #('wattpad.found', 'https://cdn.hashmob.net/hashlists/4364/4364.3200.found'), 23 m
    ('battlefield.found', 'https://cdn.hashmob.net/hashlists/541/541.0.found'), #420k
    ('wanelo.found', 'https://cdn.hashmob.net/hashlists/2925/2925.0.found'), #2 m
    ('everydayrecipes.found', 'https://cdn.hashmob.net/hashlists/134/134.0.found'), #25k
    #('zynga.found', 'https://cdn.hashmob.net/hashlists/740/740.27200.found'), #48 m
    ('dosportseasy.found', 'https://cdn.hashmob.net/hashlists/268/268.100.found') #45k
]

username = [
    #'https://example.com/group3_data1.txt',
]

# Function to create directories for datasets
def make_directories():
    if os.path.exists("./datasets"): return
    os.makedirs("./datasets/contextless/train")
    os.makedirs("./datasets/contextless/test")
    os.makedirs("./datasets/domain/train")
    os.makedirs("./datasets/domain/test")
    os.makedirs("./datasets/username/train")
    os.makedirs("./datasets/username/test")

# Function to download files into directories
def download_files(folderName):
    print(folderName)
    match folderName:
        case "contextless":
            urls = contextless
        case "domain":
            urls = domain
        case "username":
            urls = username
    for filename, url in urls:
        downloadPath = os.path.join("datasets", folderName, filename)
        if not os.path.exists(downloadPath):
            print("Downloading " + filename)
            urlretrieve(url, downloadPath)

# Function to process files into CSV format
def process_files(folderName):
    folderPath = os.path.join("datasets", folderName)
    for filename in os.listdir(folderPath):
        if not ".txt" in filename: continue
        input_file = os.path.join(folderPath, filename)
        output_file = os.path.join(folderPath, filename.replace('.txt', '.csv'))
        if os.path.exists(output_file): continue
        print("Processing " + filename)
        
        with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
            if ".txt" in filename:
                f_out.write("password\n")
                for line in f_in:
                    f_out.write("\"" + line.strip() + "\"\n")
            if ".found" in filename:
                f_out.write("password\n")
                for line in f_in:
                    f_out.write("\"" + line[line.rindex(':')+1:].strip() + "\"\n")
            if ".comb" in filename:
                f_out.write("username, password\n")
                print("username not ready yet")
                #not sure about this one yet
                #for line in f_in:
                    #writer.writerow([item.strip() for item in line.split(',')])


# Function to split CSV files into training and test sets
def split_files(folderName):
    folderPath = os.path.join("datasets", folderName)
    for filename in os.listdir(folderPath):
        if not ".csv" in filename: continue
        input_file = os.path.join(folderPath, filename)
        train_file = os.path.join(folderPath, "train", filename)
        test_file = os.path.join(folderPath, "test", filename)
        if os.path.exists(train_file) and os.path.exists(test_file): continue

        print("Splitting " + filename)
        df = pd.read_csv(input_file)
        X = df.iloc[:, :-1]  # Features
        y = df.iloc[:, -1]   # Labels

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        Xy_train = pd.concat([X_train, y_train], axis=1)
        Xy_train.to_csv(train_file, index=False)

        Xy_test = pd.concat([X_test, y_test], axis=1)
        Xy_test.to_csv(test_file, index=False)

def analyze_folder(folderName):
    folderPath = os.path.join("datasets", folderName)
    for filename in os.listdir(folderPath):
        if not ".csv" in filename: continue
        filename = os.path.join(folderPath, filename)
        analyze_file(filename)

def analyze_file(fileName):
    df = pd.read_csv(fileName)
    length = len(df.index)
    strengthAverage = reduce(strengthReduce, df['password']) / length
    print(fileName + ": length=" + str(length) + " strengthAverage=" + str(strengthAverage))

def strengthReduce(arg1, arg2):
    if isinstance(arg1, str): arg1 = PasswordStats(arg1).strength()
    return arg1 + PasswordStats(arg2).strength()

def clear_folder(folderName):
    folderPath = os.path.join("datasets", folderName)
    trainPath = os.path.join(folderPath, "train")
    testPath = os.path.join(folderPath, "test")
    for path in [folderPath, trainPath, testPath]:
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath): continue
            os.remove(filepath)

if __name__=="__main__": 
    main() 