#Converts hashcat found file to plaintext only csv file

import re
import sys

def main():
    csv = open(sys.argv[2], "w")
    foundCount = 0
    with open(sys.argv[1]) as found:
        for line in found:
            plaintext = line[line.rindex(':')+1:]
            if (len(plaintext) <= 10):
                csv.write(plaintext)
                foundCount += 1
    
    print(sys.argv[2] + " has " + str(foundCount) + " passwords" )


if __name__ == "__main__":
    main()