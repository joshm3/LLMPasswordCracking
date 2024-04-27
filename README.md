# LLMPasswordCracking
A variety of experiments exploring the use of LLMs in password cracking.
Much of the code is desined to be used along with PassGPT at https://github.com/javirandor/passgpt/tree/main

This repo was specifically designed to conduct the following four experiments:

1: Evaluate different training levels of LLMs for password cracking. 
  Reproduce by... Nikita

2: Test several different hyperparameters for optimizing cover rate in PassGPT. 
  Reproduce by using dataSetup.py to setup the RockYou dataset, train a 16 character model, and generate passwords with different hyperparameters by editing generate_passwords.py.

3: Conduct cross-site testing of PassGPT with new datasets.
  Reproduce by using dataSetup.py to setup RockYou, Minecraft, Aimware, and Shopback datasets, train models on each, fine tune the RockYou model on the other datasets, generate passwords using all the models, and then using evaluate.py to test the generated lists on different password datasets.

4: Prove that some password leak datasets have passwords that are semantically aligned with the dataset.
  Reproduce by using dataSetup.py to setup Minecraft, MangaTraders, and Battlefield datasets. Then run the experiment with contextBased.py. Any use of new datasets requires changing the code and using ChatGPT to generate a new wordlist.
