# %% Set-up

import os
import pandas as pd
import json
from typing import List, Dict
from prompts import PROMPT_TEMPLATE_BASIC

data_path = 'local/train/data'
file_name = 'datasetv03_full_analysed.csv'
file_path = os.path.join(data_path, file_name)


TRAIN_FRACTION = 0.8
TEST_FRACTION = 1 - TRAIN_FRACTION
RANDOM_SEED = 42
INPUT_HEADER = "input"
TARGET_HEADER = "output"


# %% Load and split data

print(f'Loading data from {file_path}')
df = pd.read_csv(file_path, usecols=[0, 1], names=[INPUT_HEADER, TARGET_HEADER], header=0)

print(df.info())
# print(df.head())
print(f"Number of samples: {len(df)}")
print("-" * 80)

train_df = df.sample(frac=TRAIN_FRACTION, random_state=RANDOM_SEED)
test_df = df.drop(train_df.index)

# Show the sizes of the datasets
print(f"Train set size: {len(train_df)}")
print(f"Test set size: {len(test_df)}")

# Show head of each dataset
print(f"\nTrain set:\n{train_df.head()}")
print(f"\nTest set:\n{test_df.head()}")


# %% Save the datasets to separate CSV files
train_df.to_csv(os.path.join(data_path, "train.csv"), index=False, encoding='utf-8')
test_df.to_csv(os.path.join(data_path, "test.csv"), index=False, encoding='utf-8')


# %% Format to Alpaca Dataset


def format_dataframe_to_alpaca_dataset(df: pd.DataFrame) -> List[Dict]:
    """
    Format a DataFrame to the Alpaca dataset format.

    Args:
    - df (pd.DataFrame): DataFrame containing input and output columns.

    Returns:
    - List[Dict]: A list of dictionaries in the format required by Alpaca.
    """
    return [
        {
            "instruction": PROMPT_TEMPLATE_BASIC.format(text=row[INPUT_HEADER]),
            INPUT_HEADER: "",
            TARGET_HEADER: row[TARGET_HEADER],
        }
        for _, row in df.iterrows()
    ]


# Convert the train, validation, and test datasets to Alpaca template format
train_alpaca = format_dataframe_to_alpaca_dataset(train_df)
test_alpaca = format_dataframe_to_alpaca_dataset(test_df)


# Save list to json file
def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


# print("Alpaca format sample:")
# print(json.dumps(train_alpaca[:2], indent=4))

save_to_json(train_alpaca, os.path.join(data_path, "train_alpaca.json"))
save_to_json(test_alpaca, os.path.join(data_path, "test_alpaca.json"))

print("Data has been converted to Alpaca format and saved to JSON files.")


# %% Format to chatml template


def format_dataframe_to_chatml_dataset(df: pd.DataFrame) -> List[Dict]:
    """
    Format a DataFrame to the ChatML dataset format.

    Args:
    - df (pd.DataFrame): DataFrame containing input and output columns.

    Returns:
    - List[Dict]: A list of dictionaries in the format required by ChatML.
    """
    return [
        {
            "messages": [
                {
                    "content": PROMPT_TEMPLATE_BASIC.format(text=row_dict[INPUT_HEADER]),
                    "role": "user",
                },
                {"content": row_dict[TARGET_HEADER], "role": "assistant"},
            ]
        }
        for row_dict in df.to_dict(orient="records")
    ]


# Format the train, validation, and test datasets to ChatML template
train_chatml = format_dataframe_to_chatml_dataset(train_df)
test_chatml = format_dataframe_to_chatml_dataset(test_df)


# Print the first few entries to verify the format

print("ChatML format sample:")
print(json.dumps(train_chatml[:2], indent=4))


# %% Save the ChatML datasets to JSONL files


def save_to_jsonl(data: List[Dict], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')


save_to_jsonl(train_chatml, os.path.join(data_path, "train.jsonl"))
save_to_jsonl(test_chatml, os.path.join(data_path, "test.jsonl"))

print("Data has been converted to Chatml format and saved to JSONL files.")
