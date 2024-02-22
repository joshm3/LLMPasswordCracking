#!/usr/bin/env python
# coding: utf-8

# In[16]:


pip install transformers datasets torch


# In[74]:


from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "javirandor/passgpt-10characters" # Make sure the model name is correctly specified
model = AutoModelForCausalLM.from_pretrained(model_name)


# In[75]:


import os
import argparse
import torch
from transformers import GPT2LMHeadModel
from pathlib import Path

from transformers import RobertaTokenizerFast

import numpy as np
import random
from tqdm import trange
import string


# In[76]:


MAXCHARS = 10
tokenizer = RobertaTokenizerFast.from_pretrained(model_name , 
                                                max_len=MAXCHARS+2,
                                                padding="max_length", 
                                                truncation=True,
                                                do_lower_case=False,
                                                strip_accents=False,
                                                mask_token="<mask>",
                                                unk_token="<unk>",
                                                pad_token="<pad>",
                                                truncation_side="right")


# In[77]:



def main(input_file, output_file):
    foundCount = 0
    with open(input_file) as found:
        with open(output_file, "w") as csv:
            for line in found:
                plaintext = line[line.rindex(':')+1:]  # Use strip() to remove leading/trailing whitespace
                plaintext_no_commas = plaintext.replace(',', '')  # Remove commas
                if len(plaintext_no_commas) <= 10:
                    csv.write(plaintext_no_commas)  # Add newline to separate passwords
                    foundCount += 1
    
    print(f"{output_file} has {foundCount} passwords")


# Define input and output file paths
input_file = "/Users/nikitayeole/passGPT/dataset.txt"
output_file = "/Users/nikitayeole/passGPT/passwords.csv"

# Call the main function
main(input_file, output_file)


# In[78]:


from datasets import load_dataset

# Specify the path to your CSV file
file_path = '/Users/nikitayeole/passGPT/passwords.csv'

# Load the dataset and explicitly add a column name
dataset = load_dataset('csv', data_files=file_path, column_names=['password'])


# In[88]:


from datasets import DatasetDict

# Assuming "dataset" is your initial dataset without splits
train_testvalid = dataset["train"].train_test_split(test_size=0.2)
test_valid = train_testvalid["test"].train_test_split(test_size=0.5)

# Creating a new DatasetDict with train, validation, and test splits
full_dataset = DatasetDict({
    "train": train_testvalid["train"],
    "validation": test_valid["train"],
    "test": test_valid["test"]
})

# Then tokenize this new split dataset
tokenized_datasets = full_dataset.map(lambda examples: tokenizer(examples['password'], padding="max_length", truncation=True, add_special_tokens=False, max_length=10), batched=True)


# In[89]:


tokenized_datasets


# In[90]:


# Print out tokenized examples
for example in tokenized_datasets["train"]:
    print("Original Password:", example["password"])
    print("Tokenized Password:", tokenizer.convert_ids_to_tokens(example["input_ids"]))
    print("Length:", len(example["input_ids"]))
    print()


# In[96]:


from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"]
)

trainer.train()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[92]:


# Debug batching process
for batch in trainer.get_train_dataloader():
    batch_input_ids = batch['input_ids']
    batch_lengths = [len(input_ids) for input_ids in batch_input_ids]
    print("Batch Sequence Lengths:", batch_lengths)


# In[ ]:





# In[ ]:




