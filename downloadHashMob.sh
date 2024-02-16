#!/bin/bash
#This script downloads several domain specific password leaks from hashmob.net with hashes and found passwords 

#These datasets will change overtime as more people crack passwords and upload them
#Thus all research should be careful to compare on the same dataset versions

wget -O minecraft.csv https://cdn.hashmob.net/hashlists/466/466.2811.found #minecraft 149,000
wget -O mangatraders.csv https://cdn.hashmob.net/hashlists/752/752.0.found #mangatraders 619,000
wget -O wattpad.csv https://cdn.hashmob.net/hashlists/4364/4364.3200.found #wattpad 23,000,000
wget -O battlefield.csv https://cdn.hashmob.net/hashlists/541/541.0.found #battlefield 420,000
wget -O wanelo.csv https://cdn.hashmob.net/hashlists/2925/2925.0.found #wanelo 2,000,000
wget -O everydayrecipes.csv https://cdn.hashmob.net/hashlists/134/134.0.found #everydayrecipes 25,000
wget -O zynga.csv https://cdn.hashmob.net/hashlists/740/740.27200.found #zynga 48,000,000
wget -O dosportseasy.csv https://cdn.hashmob.net/hashlists/268/268.100.found #dosportseasy 45,000
