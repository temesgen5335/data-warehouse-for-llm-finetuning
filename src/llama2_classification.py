from src.database import MongoDB
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset
import torch
from sklearn.preprocessing import LabelEncoder


db_name = 'clean_data'
collection_name = 'alain_news_clean'
connection_string = 'mongodb://localhost:27017/'
amharic_db = MongoDB(db_name=db_name, collection_name=collection_name, connection_string=connection_string)

data = list(amharic_db.collection.find({}))

texts = [item['content'] for item in data]
labels = [item['category'] for item in data]

# Split the data into training and test sets
train_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Load the pre-trained model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained('allenai/led-base-16384', num_labels=3)  # Adjust num_labels according to your classification task


tokenizer = AutoTokenizer.from_pretrained('allenai/led-base-16384')

# Tokenize the training data
train_encodings = tokenizer(train_texts, truncation=True, padding=True)

# Tokenize the test data
test_encodings = tokenizer(test_texts, truncation=True, padding=True)

class CustomDataset(Dataset):
  def __init__(self, encodings, labels):
    self.encodings = encodings
    self.labels = labels

  def __getitem__(self, idx):
    item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
    item['labels'] = torch.tensor(self.labels[idx])
    return item

  def __len__(self):
    return len(self.labels)

# Instantiate the encoder
le = LabelEncoder()

# Fit the encoder and transform the labels
train_labels = le.fit_transform(train_labels)
test_labels = le.transform(test_labels)

train_dataset = CustomDataset(train_encodings, train_labels)
test_dataset = CustomDataset(test_encodings, test_labels)

from transformers import TrainingArguments, Trainer

# Define the training arguments
training_args = TrainingArguments(
  output_dir='./results',          # output directory
  num_train_epochs=3,              # total number of training epochs
  per_device_train_batch_size=16,  # batch size per device during training
  warmup_steps=500,                # number of warmup steps for learning rate scheduler
  weight_decay=0.01,               # strength of weight decay
  logging_dir='./logs',            # directory for storing logs
)

# Create the Trainer and train
trainer = Trainer(
  model=model,                         # the instantiated 🤗 Transformers model to be trained
  args=training_args,                  # training arguments, defined above
  train_dataset=train_dataset,         # training dataset
  eval_dataset=test_dataset,           # evaluation dataset
)

trainer.train()