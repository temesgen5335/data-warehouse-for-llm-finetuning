from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, LlamaForCausalLM
from peft import LoraConfig, # Apply LoRA to the model
model = get_peft_model(model, lora_config), prepare_model_for_int8_training

# Load the base model and tokenizer
model_name = "Samuael/llama-2-7b-tebot-amharic"
# model_name_garri = "iocuydi/llama-2-amharic-3784m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
# tokenizer = LlamaTokenizer.from_pretrained(model_name_garri, revision=commit_hash, cache_dir= cache_dir)
model = AutoModelForCausalLM.from_pretrained(model_name)
# model = LlamaForCausalLM.from_pretrained(model_name_garri)

# Prepare the model for int8 training (helps reduce memory usage)
model = prepare_model_for_int8_training(model)

# Define LoRA configuration
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none"
)

# Apply LoRA to the model
model = get_peft_model(model, lora_config)

# Tokenize example input
input_text = "ሰላም እንዴት ነህ?"
inputs = tokenizer(input_text, return_tensors="pt")

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test']
)

def main():
    # Train the model
    trainer.train()

    # Save the model
    model.save_pretrained("./finetuned_model")

    # Test the fine-tuned model
    output = model.generate(**inputs, max_length=50)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(generated_text)

if __name__ == "__main__":
    main()