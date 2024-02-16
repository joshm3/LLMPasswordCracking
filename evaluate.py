#Checks to see how many passwords in the second file are guessed by the wordlist in the first file
#Usage:   python evaluate.py <wordlist.csv> <passwords.csv>

#Could be improved, does not account for repeated passwords

import sys

def main():
    wordlist = open(sys.argv[1], "r")
    passwordsFound = 0
    with open(sys.argv[2]) as passwords:
        for password in passwords:
            password = password.strip()
            wordlist.seek(0)
            for word in wordlist:
                word = word.strip()              
                if password == word:
                    passwordsFound += 1
                    break
    
    print(str(passwordsFound) + " passwords found in " + sys.argv[2] + " using wordlist " + sys.argv[1])


if __name__ == "__main__":
    main()