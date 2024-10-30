import logging, os
import pandas as pd
import argparse
from prompts import SYSTEM_MESSAGE_LS, PROMPT_TEMPLATE

logging.basicConfig(format=os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))


def main(file_path: str, output_file: str = "ModelfileLS_FS", base_model: str = "llama3.1"):
    """
    Converts a CSV file containing columns 'Original' and 'Leichte Sprache' to a text file with specific formatting for model usage.

    Args:
        file_path (str): Path to the input CSV file.
        output_file (str, optional): Name of the output text file. Defaults to "ModelfileLS_FS".
        base_model (str, optional): Base model name for the specific format requirements. Defaults to "llama3.1".

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        KeyError: If required columns ('Original' or 'Leichte Sprache') are missing in the CSV file.

    Returns:
        None
    """

    BASE_FILE_TXT = (
        f"FROM {base_model}\n"
        "PARAMETER temperature 0.2\n"
        "SYSTEM \"\"\"\n"
        f"{SYSTEM_MESSAGE_LS}\n"
        "\"\"\"\n"
    )

    logger.info(f"Loading dataset from {file_path}")

    print("Base File Text:")
    print(BASE_FILE_TXT)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    # Read the input CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Check if the required columns are present
    if 'Original' not in df.columns or 'Leichte Sprache' not in df.columns:
        logger.error(
            "The input CSV file must contain the columns 'Original' and 'Leichte Sprache'."
        )
        parser.print_help()
        return

    # Write the rows of the specified columns to a text file
    with open(output_file, 'w') as f:
        f.write(f"{BASE_FILE_TXT}")
        for index, row in df[['Original', 'Leichte Sprache']].iterrows():
            f.write("MESSAGE user \"\"\"")
            # f.write(f"{PROMPT_TEMPLATE.format(text='')}")
            f.write(PROMPT_TEMPLATE.format(text=""))
            f.write(f"{row['Original']}\n")
            f.write("\"\"\"\n")
            f.write("MESSAGE assistant \"\"\"\n")
            f.write(f"{row['Leichte Sprache']}\n")
            f.write("\"\"\"\n")

    logger.info(f"Data has been written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to TXT with specific formatting")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file")
    parser.add_argument(
        "--output_file",
        type=str,
        default="ModelfileLS_FS",
    )
    parser.add_argument("--base_model", type=str, default="llama3.1")
    args = parser.parse_args()

    main(args.input_file, args.output_file, args.base_model)
