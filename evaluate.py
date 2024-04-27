#Checks to see how many passwords in the second file are guessed by the wordlist in the first file
#Basically calculates cover rate and unique rate in a similar format to PassGPT
#Usage:   python evaluate.py <generatedList.csv> <number of generated passwords> <testListName>

import sys
import pandas as pd
import sys
# from zxcvbn import zxcvbn
import os
import csv

delimiterChar = '\t'

def main():
    genListPath = sys.argv[1]
    genLength = int(sys.argv[2])
    testListPath = sys.argv[3]

    genDf = pd.read_csv(genListPath, delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE, names=["password"])
    genDf.drop_duplicates()
    uniqueLength = len(genDf.index)
    uniquePerc = uniqueLength / genLength * 100

    testDf = pd.read_csv(testListPath, delimiter=delimiterChar, keep_default_na=False, quoting=csv.QUOTE_NONE)
    testLength = len(testDf.index)
    passwordsFound = len( set(genDf['password']) .intersection(set(testDf['password'])))

    # format taken from passgpt
    print("Number of passwords generated: {}".format(genLength))
    print("{} unique passwords generated => {:.2f}%".format(uniqueLength, uniquePerc))
    print("{} passwords where found in the test set. {:.5f}% of the test set guessed.".format(passwordsFound, passwordsFound/testLength*100))

    # For measuring password strength

    # scoreSum = 0
    # for password in testDf['password']:
    #     for word in genDf['password']:
    #         if password == word:
    #             # scoreSum += zxcvbn(password)['score']
    #             break
        
    # averageScorePasswordsFound = scoreSum / passwordsFound
    # print("PPC=" + str(ppc) + " AverageScoreForPasswordsFound=" + str(averageScorePasswordsFound))

if __name__ == "__main__":
    main()