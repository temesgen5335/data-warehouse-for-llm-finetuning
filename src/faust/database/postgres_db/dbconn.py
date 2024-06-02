import psycopg2
import os

# Database connection parameters
dbname = 'amharic_news'
user = 'postgres'
password = 'postgres'
host = 'localhost'  # or your host address
port = '5432'  # or your port number

# CSV file path
csv_file_path = os.path.abspath('../week-5/data-warehouse-for-llm-finetuning/data/preprocessed.csv')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
cur = conn.cursor()
'''
# Create table
create_table_query = """
CREATE TABLE amharic_news_data (
    id INTEGER,
    url TEXT,
    source TEXT,
    title TEXT,
    text TEXT,  -- If you want to preserve this column
    category TEXT,
    tags TEXT,
    word_count INTEGER,
    language TEXT
);
"""
cur.execute(create_table_query)
conn.commit()
'''

#ALTER TABLE amharic_news_data
#ALTER COLUMN category DROP NOT NULL;

# Load data from CSV file
with open(csv_file_path, 'r') as file:
    next(file)  # Skip the header row
    cur.copy_from(file, 'amharic_news_data', sep=',')

# Commit changes and close cursor and connection
conn.commit()
cur.close()
conn.close()
