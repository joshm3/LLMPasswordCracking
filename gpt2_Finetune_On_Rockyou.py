#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
from torch.utils.data import DataLoader, Dataset
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW
from torch.nn.utils.rnn import pad_sequence

#To Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token

#To Read the dataset
max_passwords = 1000000
with open('rockyouTrain.txt', 'r', encoding='utf-8') as file:
    passwords = [next(file).strip() for _ in range(max_passwords)]

#To Encode the passwords
inputs = [tokenizer.encode(password.strip(), add_special_tokens=True) for password in passwords]

class PasswordDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings)

    def __getitem__(self, idx):
        return torch.tensor(self.encodings[idx], dtype=torch.long)

def collate_batch(batch):
    input_ids = [item for item in batch]
    input_ids_padded = pad_sequence(input_ids, batch_first=True, padding_value=tokenizer.pad_token_id)
    return input_ids_padded, input_ids_padded

dataset = PasswordDataset(inputs)
loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=collate_batch)

model = GPT2LMHeadModel.from_pretrained('gpt2')
model.train()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = AdamW(model.parameters(), lr=1e-3)

epochs = 2
for epoch in range(epochs):
    for input_ids, labels in loader:
        optimizer.zero_grad()
        input_ids, labels = input_ids.to(device), labels.to(device)
        outputs = model(input_ids, labels=labels)
        loss = outputs.loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        print(f"Epoch: {epoch+1}, Loss: {loss.item()}")

model.save_pretrained('./fine_tune_gpt2')
tokenizer.save_pretrained('./fine_tune_gpt2')

print("Model training complete and saved.")


# In[1]:


import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import random
from tqdm import tqdm
import os
from pathlib import Path

def check_model_parameters(model):
    for param in model.parameters():
        if torch.isnan(param).any() or torch.isinf(param).any():
            return False
    return True

def generate_passwords(model, tokenizer, device, num_generate, batch_size, max_length, temperature, top_k, top_p, output_file):
    model.eval()  # This is to ensure that model is in evaluation mode
    progress_bar = tqdm(total=num_generate, desc="Generating passwords")
    with torch.no_grad():
        for _ in range(0, num_generate, batch_size):
            # To set seed for reproducibility and diversity
            seed = random.randint(0, 10000)
            torch.manual_seed(seed)
            
            # Generate passwords
            input_ids = torch.tensor([tokenizer.encode("pa", add_special_tokens=True)] * batch_size).to(device)
            outputs = model.generate(
                input_ids,
                max_length=max_length + 2,
                pad_token_id=tokenizer.pad_token_id,
                num_return_sequences=batch_size,
                num_beams=1,
                do_sample=True,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature
            )
            outputs = outputs[:, 1:] 
            
            # Decode and write passwords to file
            for output in outputs:
                password = tokenizer.decode(output, skip_special_tokens=True).split("</s>")[0]
                output_file.write(f"{password}\n")

            progress_bar.update(batch_size)
    progress_bar.close()

if __name__ == "__main__":
    model_path = './fine_tune_gpt2'
    num_generate = 1000000 // 8
    batch_size = 8
    max_length = 16
    temperature = 0.7
    top_k = 40
    top_p = 0.9

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = GPT2LMHeadModel.from_pretrained(model_path).to(device)
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)

    # To Check if model parameters are valid
    if not check_model_parameters(model):
        print("Model parameters contain Nan or Inf values.")
        exit(1)

    #Output path and file
    out_path = "./generated_passwords1"
    filename = "passwords.txt"
    Path(out_path).mkdir(parents=True, exist_ok=True)
    
    with open(os.path.join(out_path, filename), 'w') as f:
        generate_passwords(model, tokenizer, device, num_generate, batch_size, max_length, temperature, top_k, top_p, f)

    print(f"Generated {num_generate} passwords and saved to '{os.path.join(out_path, filename)}'")


# In[ ]:


def display_cuda_memory():    
    print("\n--------------------------------------------------\n")
    print("torch.cuda.memory_allocated: %fGB"%(torch.cuda.memory_allocated(0)/1024/1024/1024))
    print("torch.cuda.memory_reserved: %fGB"%(torch.cuda.memory_reserved(0)/1024/1024/1024))
    print("torch.cuda.max_memory_reserved: %fGB"%(torch.cuda.max_memory_reserved(0)/1024/1024/1024))
    print("\n--------------------------------------------------\n")
display_cuda_memory()


# In[ ]:


import torch
torch.cuda.empty_cache()

