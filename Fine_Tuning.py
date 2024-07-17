from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TrainerCallback, DataCollatorForLanguageModeling
import os
import torch

# Function to split text into manageable chunks respecting maximum sequence length
def split_text_into_chunks(text, max_chunk_length=1024):
    chunks = []
    current_chunk = []
    current_length = 0
    
    for line in text.splitlines():
        tokens = line.split()
        for token in tokens:
            token_length = len(token) + 1  # Add 1 for space between tokens
            if current_length + token_length > max_chunk_length:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(token)
            current_length += token_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

# Function to load and split text dataset into chunks
def load_and_split_text_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return split_text_into_chunks(text)

# Load and split the combined datasets
books_chunks = load_and_split_text_dataset('C:\\Users\\alexa\\Desktop\\combined_books.txt')
scripts_chunks = load_and_split_text_dataset('C:\\Users\\alexa\\Desktop\\combined_scripts.txt')
master_chunks = load_and_split_text_dataset('C:\\Users\\alexa\\Desktop\\master_combined.txt')

# Initialize tokenizer and adjust parameters
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token

# Tokenize function
def tokenize_function(examples):
    return tokenizer(examples, return_special_tokens_mask=True)

# Tokenize all chunks
tokenized_books = [tokenize_function(chunk) for chunk in books_chunks]
tokenized_scripts = [tokenize_function(chunk) for chunk in scripts_chunks]
tokenized_master = [tokenize_function(chunk) for chunk in master_chunks]

# Custom data collator
class CustomDataCollator(DataCollatorForLanguageModeling):
    def __init__(self, tokenizer):
        super().__init__(tokenizer=tokenizer, mlm=False)

    def collate_batch(self, batch):
        batch = [example for example in batch if len(example['input_ids']) > 0]  # Filter out empty examples
        return self.tokenizer.pad(
            batch,
            padding=True,
            return_tensors="pt",
        )

# Initialize GPT-2 model
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./fine_tuned_model',
    overwrite_output_dir=True,
    num_train_epochs=3,  # Adjust epochs as needed
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
    prediction_loss_only=True,
)

# Custom callback for printing progress
class ProgressCallback(TrainerCallback):
    def on_train_begin(self, args, state, control, **kwargs):
        print("Training is starting!")

    def on_epoch_end(self, args, state, control, **kwargs):
        print(f"Finished epoch {state.epoch}")

    def on_log(self, args, state, control, logs=None, **kwargs):
        print(logs)

# Function to train the model on chunks
def train_model_on_chunks(tokenized_chunks, model, training_args):
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_chunks,  # Ensure tokenized chunks are dictionaries with 'input_ids' and 'attention_mask'
        data_collator=CustomDataCollator(tokenizer=tokenizer),
        callbacks=[ProgressCallback()]
    )
    trainer.train()

# Train on each dataset
print("Training on books chunks...")
train_model_on_chunks(tokenized_books, model, training_args)

print("Training on scripts chunks...")
train_model_on_chunks(tokenized_scripts, model, training_args)

print("Training on master combined chunks...")
train_model_on_chunks(tokenized_master, model, training_args)

print("Fine-tuning completed successfully.")
