import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
import torch

# Load environment variables from .env
load_dotenv()

# Get model name from .env
MODEL_NAME = os.getenv("MODEL_NAME", "ibm-granite/granite-3.3-2b-instruct")

print(f"🔹 Loading Granite model: {MODEL_NAME}")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",        # Uses GPU if available
    torch_dtype=torch.float32 # Forces CPU-friendly precision
)

print("✅ Model loaded successfully! Now generating text...")

# Prompt
prompt = "Give me 3 personal finance tips for saving money."

# Tokenize and run inference
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)

# Decode response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("\n🤖 Granite says:", response)