# This script is specifically designed to execute the experiment described in experiment 4 of 
#   "The Application of LLMs in Password Cracking: A Series of Experiments and Findings"

# it does not actually contact ChatGPT and you must execute the prompt and gather the wordlists manually.

import pandas as pd
import os
from urllib.request import urlretrieve
import csv
import editdistance

delimiterChar = '\t'

#a slower but better option than just checking for substrings
def is_similar(str1, str2, threshold=4):
    distance = editdistance.eval(str1, str2)
    return distance < threshold

def battleCountFunction(row):
    word = row['password'].lower()
    count = 0
    for password in battleLeak['password']:
        if word in password.lower():
            count += 1
    return count

def mangaCountFunction(row):
    word = row['password'].lower()
    count = 0
    for password in mangaLeak['password']:
        if word in password.lower():
            count += 1
    return count

def minecraftCountFunction(row):
    word = row['password'].lower()
    count = 0
    for password in minecraftLeak['password']:
        if word in password.lower():
            count += 1
    return count



# download ignis 100k
ignisUrl = 'https://raw.githubusercontent.com/ignis-sec/Pwdb-Public/master/wordlists/ignis-100K.txt'
downloadPath = './datasets/ignis-100k'
if not os.path.exists(downloadPath):
    print("Downloading ignis 100k")
    urlretrieve(ignisUrl, downloadPath)

battleLeak = pd.read_csv("./datasets/battlefield.csv", delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
mangaLeak = pd.read_csv("./datasets/mangatraders.csv", delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
minecraftLeak = pd.read_csv("./datasets/minecraft.csv", delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)


if not os.path.exists("./contextResults.csv"):

    # arrays of all of the words for battlefield, mangatraders, and minecraft
    # prompt is "You are thinking of simple names or words to use in your password. List 10 common names associated with {Seed Word}."
    # prompt is entered in free ChatGPT 3.5 and manually copied into this script
    # the seed word is the name of the array
    battlefield = ["Battlefield","Assault","Recon","Medic","Engineer","Sniper","Tank","Squad","Commander","Grenade"]
    manga = ["Naruto","Goku","Luffy","Ichigo","Sasuke","Light","Edward","Inuyasha","Ash","Gon"]
    minecraft = ["Steve","Alex","Notch","Herobrine","Enderman","Creeper","Zombie","Skeleton","Pigman","Villager"]

    # combine everything
    df = pd.read_csv(downloadPath, names=["password"], delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
    df['ignis'] = True

    battleDf = pd.DataFrame(battlefield, columns =['password']) 
    battleDf['battlefieldSeed'] = True

    mangaDf = pd.DataFrame(manga, columns =['password']) 
    mangaDf['mangaSeed'] = True

    minecraftDf = pd.DataFrame(minecraft, columns =['password']) 
    minecraftDf['minecraftSeed'] = True

    df = pd.concat([df, battleDf, mangaDf, minecraftDf])

    # get counts of the words in each dataset, dataset already downloaded using setup.py, using entire dataset
    
    print("Counting matches for battlefield")
    df['battlefieldCount'] = df.apply(battleCountFunction, axis=1)
    print("Counting matches for manga")
    df['mangaCount'] = df.apply(mangaCountFunction, axis=1)
    print("Counting matches for minecraft")
    df['minecraftCount'] = df.apply(minecraftCountFunction, axis=1)

    #output the final results to a csv
    df.to_csv("./contextResults.csv")

df = pd.read_csv("./contextResults.csv")

#remove all of the small words that dont make any sense
# df = df[df['password'].str.len() >= 5]

# print out the average count for each word type for each dataset

# seperate the stats for iginis based on 20k intervals since they are ordered by occurence, they are the first 100k entries
print("Wordlist     & Battlefield     & MangaTraders   & Minecraft")

intervalSize = 20000 # so 5 intervals of 20k
for i in [1, 2, 3, 4, 5]:
    start = (i-1)*intervalSize
    end = (i)*intervalSize
    dfInterval = df[start:end]

    battleAv = round(dfInterval['battlefieldCount'].sum() / intervalSize / len(battleLeak.index) * 100000, 2)
    mangaAv = round(dfInterval['mangaCount'].sum() / intervalSize / len(mangaLeak.index) * 100000, 2)
    minecraftAv = round(dfInterval['minecraftCount'].sum() / intervalSize / len(minecraftLeak.index) * 100000, 2)

    print("Ignis", start, "-", end, " & ", battleAv, " & ",mangaAv, " & ",minecraftAv)
    # print("Battlefield word average count ", battleAv)
    # print("Manga word average count ", mangaAv)
    # print("Minecraft word average count ", minecraftAv)

for wordType in ['battlefieldSeed', 'mangaSeed', 'minecraftSeed']:
    #get all rows with that wordType
    dfInterval = df[df[wordType]==True]

    battleAv = round(dfInterval['battlefieldCount'].sum() / len(dfInterval.index) / len(battleLeak.index) * 100000, 2)
    mangaAv = round(dfInterval['mangaCount'].sum() / len(dfInterval.index) / len(mangaLeak.index) * 100000, 2)
    minecraftAv = round(dfInterval['minecraftCount'].sum() / len(dfInterval.index) / len(minecraftLeak.index) * 100000, 2)

    print(wordType, " & ",battleAv, " & ",mangaAv, " & ",minecraftAv)
    # print("Battlefield word average count ", battleAv)
    # print("Manga word average count ", mangaAv)
    # print("Minecraft word average count ", minecraftAv)
