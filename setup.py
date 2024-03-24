import os
from urllib.request import urlretrieve
import csv
import random
from functools import reduce
from password_strength import PasswordStats
from sklearn.model_selection import train_test_split 
import pandas as pd

# Function to download files into directories
def download_files(urls, folderName):
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
            match folderName:
                case "contextless":
                    f_out.write("password\n")
                    for line in f_in:
                        f_out.write("\"" + line.strip() + "\"\n")
                case "domain":
                    f_out.write("password\n")
                    for line in f_in:
                        f_out.write("\"" + line[line.rindex(':')+1:].strip() + "\"\n")
                case "username":
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

# Function to calculate the number of rows in each CSV file
# def count_rows(input_dirs):
#     for input_dir in input_dirs:
#         print(f"Counting rows in {input_dir} directory:")
#         for filename in os.listdir(input_dir):
#             input_file = os.path.join(input_dir, filename)
#             with open(input_file, 'r') as f_in:
#                 num_rows = sum(1 for row in f_in)
#                 print(f"Number of rows in {filename}: {num_rows}")

# # Function to calculate average password strength using functools.reduce
# def calculate_average_password_strength(input_dirs):
#     for input_dir in input_dirs:
#         print(f"Calculating average password strength in {input_dir} directory:")
#         for filename in os.listdir(input_dir):
#             input_file = os.path.join(input_dir, filename)
#             with open(input_file, 'r') as f_in:
#                 passwords = [row.strip().split(',')[1] for row in f_in]  # Assuming password is the second column
#                 if passwords:
#                     password_strengths = [PasswordStats(password).entropy() for password in passwords]
#                     average_strength = reduce(lambda x, y: x + y, password_strengths) / len(password_strengths)
#                     print(f"Average password strength in {filename}: {average_strength}")
#                 else:
#                     print(f"No passwords found in {filename}")

# URLs of files to download
contextless = [
    'https://example.com/group2_data1.txt',
    'https://example.com/group2_data2.txt',
    'https://example.com/group2_data3.txt'
]

domain = [
    ('minecraft.txt', 'https://cdn.hashmob.net/hashlists/466/466.2811.found'), #149k
    ('mangatraders.txt', 'https://cdn.hashmob.net/hashlists/752/752.0.found'), #619k
    #('wattpad.txt', 'https://cdn.hashmob.net/hashlists/4364/4364.3200.found'), 23 m
    ('battlefield.txt', 'https://cdn.hashmob.net/hashlists/541/541.0.found'), #420k
    ('wanelo.txt', 'https://cdn.hashmob.net/hashlists/2925/2925.0.found'), #2 m
    ('everydayrecipes.txt', 'https://cdn.hashmob.net/hashlists/134/134.0.found'), #25k
    #('zynga.txt', 'https://cdn.hashmob.net/hashlists/740/740.27200.found'), #48 m
    ('dosportseasy.txt', 'https://cdn.hashmob.net/hashlists/268/268.100.found') #45k
]

username = [
    #'https://example.com/group3_data1.txt',
]


# Download files
#download_files(urls_group1, [download_dirs[0]] * len(urls_group1))
download_files(domain, "domain")
#download_files(urls_group3, [download_dirs[2]] * len(urls_group3))

# Process files
process_files("domain")

#split files
split_files("domain")

#analyze_files("domain")
