#Checks to see how many passwords in the second file are guessed by the wordlist in the first file
#Usage:   python evaluate.py <generatedList.csv> <testListName>

#Could be improved, does not account for repeated passwords

import sys
import pandas as pd
import sys
from zxcvbn import zxcvbn
import os
import csv

delimiterChar = '\t'

def main():
    genListPath = sys.argv[1]
    testListName = sys.argv[2]
    typeOfTest = "unassigned"

    #first search for the evaluation list given the base name ex: "minecraft"
    for filename in os.listdir("./datasets/test"):
        if testListName in filename:
            testListPath = os.path.join("datasets", "test", filename)
            typeOfTest = type
            break

    if (typeOfTest == "unassigned"): 
        print("Error")
        return

    #fix gendf file to hasv password at top if not csv
    if not ".csv" in genListPath: addKey(genListPath)
    genDf = pd.read_csv(genListPath, delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
    testDf = pd.read_csv(testListPath, delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
    passwordsFound = 0

    scoreSum = 0
    for password in testDf['password']:
        cracked=False
        for word in genDf['password']:
            if password == word:
                scoreSum += zxcvbn(password)['score']
                passwordsFound += 1
                cracked=True
                break
        if cracked==False: print(password)
    
    averageScorePasswordsFound = scoreSum / passwordsFound
    ppc = passwordsFound / len(testDf.index) #percent of passwords cracked

    
    # print("Results added to " + typeOfTest + "Results.csv")
    # printResults(typeOfTest, "strategy test", testListName, ppc)

    print("Passwords found: " + str(passwordsFound) + " out of " + str(len(testDf.index)))
    print("PPC=" + str(ppc) + " AverageScoreForPasswordsFound=" + str(averageScorePasswordsFound))


def printResults(typeOfTest, strategy, testListName, ppc):
    df = pd.read_csv(typeOfTest + "Results.csv")
    colName = testListName + "Ppc"
    new_row = {'strategy': strategy, colName: ppc}  # Modify column names and values as needed
    df = df._append(new_row, ignore_index=True)
    print(df)
    df.to_csv(typeOfTest + "Results.csv", index=False)


def addKey(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("password\n" + content)
    os.rename(filename, filename + ".csv")

def analyze_file(fileName):
    df = pd.read_csv(fileName)
    length = len(df.index)
    scoreSum = 0
    for password in df['password']:
        scoreSum += zxcvbn(password)['score']
    scoreAverage = scoreSum / length
    print(fileName + ": length=" + str(length) + " strengthAverage=" + str(scoreAverage))

if __name__ == "__main__":
    main()