from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Path to the directory where you saved the model and tokenizer
model_directory = 'C:/Users/alexa/Desktop/alexgpt/saved_model'

# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(model_directory)

# Load the model
model = GPT2LMHeadModel.from_pretrained(model_directory)

# Set the device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Initialize conversation
print("Bot: Hi! I'm here to chat. You can type 'exit' to end the conversation.")

while True:
    # Get user input
    user_input = input("You: ")

    # Check if user wants to exit
    if user_input.lower() == 'exit':
        print("Bot: Goodbye!")
        break

    # Tokenize input text
    input_ids = tokenizer.encode(user_input, return_tensors='pt').to(device)

    # Generate response
    try:
        output = model.generate(
            input_ids=input_ids,
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            pad_token_id=model.config.pad_token_id,
            attention_mask=torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
        )

        # Decode and print the generated text
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        print("Bot:", generated_text)

    except Exception as e:
        print("Error generating response:", e)
