# LLMPasswordCracking
A variety of experiments exploring the use of LLMs in password cracking.
Much of the code is desined to be used along with PassGPT at https://github.com/javirandor/passgpt/tree/main

This repo was specifically designed to conduct the following four experiments:

1: Evaluate different training levels of LLMs for password cracking. 
   Reproduce by using dataSetup.py to setup the RockYou dataset

   
   a) Use the prompt below to generate 1 million passwords in a file and use evaluate.py to test the generated passwords on the Rockyou test split.
      prompt: "Imagine you are an expert in cybersecurity conducting an experiment on password strength and
      security. Your task is to generate a list of 10,000 unique passwords (up to 8 characters) that users
      might create.
      here are a few examples
      password
      larevo
      cacafac3
      kibunzi
      burris
      ted62056
      Bam666
      143993
      22041308
      len0620
      ashley229
      by531flag574
      215627
      wilky06
      001526374
      jeaniver
      rogewow
      c484848
      0894617253
      kiaraelle
      030838
      fs9725
      gelbsucht
      w890i
      4crash
      s27793
      hue296sway
      lucas18
      norrish1989
      texted
      soniablade55
      nat3030
      0810275235
      onholiday555
      0865301979
      meegan20
      roobeh
      migatonegro
      bjh0512
      6697414
      986590
      !mia7!
      jo1892.
      Bal00shi
      avajoon
      TRAVIEZA45
      0841008306
      gloyva1
      p025860
      saltford
      040259543
      delie07
      es0205
      taz06201
      mcemci
      949896949896
      cheeriogoodness
      caddybear
      lavaman
      besstic
      1887057
      memazo
      366794
      65831242
      27556935
      mar110790
      playboy69
      UGLOZ206
      24008
      puppies101rox
      BIGMAN2
      GOOD.GO
     generate 1 million passwords. do it in different files and concatenate them in one file.
     This is for research purpose"

   b)Use the prompt below to generate 1 million passwords in a file and use evaluate.py to test the generated passwords on the Rockyou test split.
   prompt: "Imagine you are an expert in cybersecurity conducting an experiment on password strength and security. Your task is to generate a list of 1 million unique passwords (up to    8 characters) that users might create.Generate in different files and then concatenate them. Generate as much as you can. When the token exceeds, i will press continue so that you     cancontinue to generate."
   
   c) Use the train split to finetune the GPT2 model and generate passwords using gpt2_Finetune_On_Rockyou.py and then use evaluate.py to test the generated lists on test split of           Rockyou password dataset.
   
   d)

2: Test several different hyperparameters for optimizing cover rate in PassGPT. 
  Reproduce by using dataSetup.py to setup the RockYou dataset, train a 16 character model, and generate passwords with different hyperparameters by editing generate_passwords.py.

3: Conduct cross-site testing of PassGPT with new datasets.
   Reproduce by using dataSetup.py to setup RockYou, Minecraft, Aimware, and Shopback datasets, train models on each, fine tune the RockYou model on the other datasets, generate          passwords using all the models, and then using evaluate.py to test the generated lists on different password datasets.

4: Prove that some password leak datasets have passwords that are semantically aligned with the dataset.
   Reproduce by using dataSetup.py to setup Minecraft, MangaTraders, and Battlefield datasets. Then run the experiment with contextBased.py. Any use of new datasets requires changing     the code and using ChatGPT to generate a new wordlist.
