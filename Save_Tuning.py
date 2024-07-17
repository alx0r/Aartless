import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Path to save the model and tokenizer
model_directory = 'C:/Users/alexa/Desktop/alexgpt/saved_model'

# Create the directory if it doesn't exist
os.makedirs(model_directory, exist_ok=True)

# Initialize and save the model
model = GPT2LMHeadModel.from_pretrained('gpt2')
model.save_pretrained(model_directory)

# Initialize and save the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.save_pretrained(model_directory)

print("Model and tokenizer saved successfully!")
