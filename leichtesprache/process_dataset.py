import logging, os
import argparse
import pandas as pd
from tqdm import tqdm
from core import simplify_text
from analysedata import calculate_fre_score, calculate_wstf_score, plot_scores
from utils import get_new_file_path
import parameters as p

logging.basicConfig(format=os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))

# %% ============== Load Dataset ============================================


def load_dataset(file_path: str, verbose=True) -> pd.DataFrame:
    """Load cleaned and analysed dataset from file path."""

    logger.info(f"Loading dataset from {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    df = pd.read_csv(file_path)

    if verbose:
        print("Initial Dataset Info:")
        print(df.info(verbose=False))
        print("Headers:", df.columns.to_list())
        print(df.describe())

        # Average FRE score
        if "Original FRE Score" in df.columns:
            avg_original = df["Original FRE Score"].mean().round(2)
            print("-" * 80)
            print("Flesch Reading Ease Score (low = hard, high = easy):")
            print("Average Original FRE Score:", avg_original)
        if "Leichte Sprache FRE Score" in df.columns:
            avg_leichte_sprache = df["Leichte Sprache FRE Score"].mean().round(2)
            print("Average Leichte Sprache FRE Score:", avg_leichte_sprache)

        # Average Wiener score
        if "Original WSTF Score" in df.columns:
            avg_original_wstf = df["Original WSTF Score"].mean().round(2)
            print("-" * 80)
            print("Wiener Sachtextformel: (min: 4 = easy, max: ~15 = hard)")
            print("Average Original WSTF Score:", round(avg_original_wstf, 2))
        if "Leichte Sprache WSTF Score" in df.columns:
            avg_leichte_sprache_wstf = df["Leichte Sprache WSTF Score"].mean().round(2)
            print("Average Leichte Sprache WSTF Score:", round(avg_leichte_sprache_wstf, 2))
            print("-" * 80)

    return df


# %% ============== Process Dataset with LLM ===================================


def process_df_w_llm(
    df: pd.DataFrame,
    model: str = p.MODEL,
    use_rules: bool = False,
    column_choice: str = "Original",
    verbose: bool = True,
) -> pd.DataFrame:
    """Process the dataset with LLM and calculate readability scores."""

    logger.info(f"Processing dataset with LLM {model}...")

    HEADER = model
    if use_rules:
        HEADER += "_w_rules"

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        if pd.isna(row[column_choice]):
            continue
        response = simplify_text(
            row[column_choice],
            model,
            use_rules=use_rules,
            top_k=p.TOP_K,
            top_p=p.TOP_P,
            temp=p.TEMP,
        )
        fre_score = calculate_fre_score(response)
        wstf_score = calculate_wstf_score(response)

        df.loc[index, f"Leichte Sprache {HEADER}"] = response
        df.loc[index, f"{HEADER} FRE Score"] = fre_score
        df.loc[index, f"{HEADER} WSTF Score"] = wstf_score

    if verbose:
        # Average FRE score
        print(f"\n{HEADER} Average Scores:")
        avg_fre = df[f"{HEADER} FRE Score"].mean().round(2)
        print("Average Flesch Reading Ease Score:", avg_fre)

        # Average WSTF score
        avg_wstf = df[f"{HEADER} WSTF Score"].mean().round(2)
        print("Average Wiener Sachtextformel Score:", avg_wstf)

    return df


def main(
    file_path: str,
    model: str,
    use_rules: bool = False,
    column: str = "Original",
    save_file: bool = True,
    plot: bool = True,
    verbose: bool = True,
):
    """Main function to process the dataset with Leichte Sprache model."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    df = load_dataset(file_path)

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the dataset.")

    df = process_df_w_llm(df, model, use_rules, column_choice=column, verbose=verbose)

    output_file = None
    if save_file:
        suffix = "_llm_processed"
        if use_rules:
            suffix += "_w_rules"
        output_file = get_new_file_path(file_path, suffix=suffix)
        df.to_csv(output_file, index=False, encoding="utf-8")
        logger.info(f"Saved processed dataset to {output_file}")

    if plot:
        show_graph = True if df.shape[0] < 100 else False
        plot_scores(
            df, score_name="FRE", save_file=True, orig_file=output_file, show_graph=show_graph
        )
        plot_scores(
            df, score_name="WSTF", save_file=True, orig_file=output_file, show_graph=show_graph
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a dataset with Leichte Sprache model.")
    parser.add_argument("file_path", type=str, help="Path to the input CSV file.")
    parser.add_argument(
        "-m", "--model", type=str, default=p.MODEL, help="Model to use for processing."
    )

    parser.add_argument("-r", "--use_rules", action="store_true", help="Use rules for processing.")

    parser.add_argument(
        "-c",
        "--column",
        type=str,
        default="Original",
        help="Name of the column containing the text to process.",
    )

    args = parser.parse_args()

    use_rules = args.use_rules or p.USE_RULES

    main(args.file_path, args.model, use_rules, args.column)
