#Checks to see how many passwords in the second file are guessed by the wordlist in the first file
#Usage:   python evaluate.py <generatedList.csv> <evaluationList.csv>

#Could be improved, does not account for repeated passwords

import sys
import pandas as pd
import sys
from functools import reduce
from password_strength import PasswordStats

def main():
    #fix gendf file to hasv password at top if not csv
    if not ".csv" in sys.argv[1]: addKey(sys.argv[1])
    genDf = pd.read_csv(sys.argv[1])
    evalDf = pd.read_csv(sys.argv[2])
    passwordsFound = 0
    attempts = 0
    totalAttemptsForSuccess = 0

    for password in evalDf['password']:
        attempts = 0
        for word in genDf['password']:
            attempts+= 1
            if password == word:
                passwordsFound += 1
                totalAttemptsForSuccess += attempts
                break
    
    avgAttemptsForSuccess = totalAttemptsForSuccess / passwordsFound
    
    print("Passwords found: " + str(passwordsFound) + "\tAverage attempts for success: " + str(avgAttemptsForSuccess))
    analyze_file(sys.argv[1])
    analyze_file(sys.argv[2])


def addKey(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("password\n" + content)

def analyze_file(fileName):
    df = pd.read_csv(fileName)
    length = len(df.index)
    strengthAverage = reduce(strengthReduce, df['password']) / length
    print(fileName + ": length=" + str(length) + " strengthAverage=" + str(strengthAverage))

def strengthReduce(arg1, arg2):
    if isinstance(arg1, str): arg1 = PasswordStats(arg1).strength()
    return arg1 + PasswordStats(arg2).strength()


if __name__ == "__main__":
    main()