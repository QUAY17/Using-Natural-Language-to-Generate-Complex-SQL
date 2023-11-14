import pandas as pd

# Load the dataset
data = pd.read_csv('/Users/quay17/Desktop/GitLocal/NLP/llama2/data/format_v2/SQLQueriesV2.csv')

# Randomly shuffle the data to ensure diversity
data_shuffled = data.sample(frac=1, random_state=42)

# Split the shuffled data into smaller chunks
chunk_size = 5000  # 1/30 of data
chunks = [data_shuffled[i:i + chunk_size] for i in range(0, data_shuffled.shape[0], chunk_size)]

# Save each chunk as a separate CSV file
for index, chunk in enumerate(chunks):
    filename = f"train_5k_chunk_{index}.csv"
    chunk.to_csv(filename, index=False)
    print(f"Saved chunk {index} to {filename}")
