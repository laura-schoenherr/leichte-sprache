import pandas as pd
from matplotlib import pyplot as plt
import textstat
import argparse
from leichtesprache.utils import get_new_file_path
from leichtesprache.parameters import LANGUAGE

textstat.set_lang(LANGUAGE)


def calculate_fre_score(text: str) -> float:
    return textstat.flesch_reading_ease(text)


def calculate_wstf_score(text: str) -> float:
    return textstat.wiener_sachtextformel(text, 1)


def preprocess_data(
    file_path: str, save_file: bool = False, verbose: bool = False
) -> pd.DataFrame:
    """Clean the data from a CSV file"""

    df = pd.read_csv(file_path, usecols=[0, 1])
    if verbose:
        print("Initial Dataset Info:")
        df.info(verbose=False)
        print()
        print(df.describe().to_markdown())

        # Check for empty values and duplicates
        empty_values = df[df.isna().any(axis=1)]
        duplicated_values = df[df.duplicated()]
        if len(empty_values) > 0:
            print("-" * 80)
            print("Empty Values:\n", empty_values)
        if len(duplicated_values) > 0:
            print("\nDuplicated Values:\n", duplicated_values)

    df.dropna(inplace=True, ignore_index=True)

    # Rename Column Names
    headers = df.columns.to_list()
    df.rename(columns={headers[0]: 'Original', headers[1]: 'Leichte Sprache'}, inplace=True)
    df.drop_duplicates(inplace=True, ignore_index=True)

    if verbose:
        print("\n" + "-" * 80)
        print("\nPreprocessed Dataset Info:")
        df.info(verbose=False)
        print()
        print(df.describe().to_markdown())

    if save_file:
        output_file = get_new_file_path(suffix="_preprocessed")
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Preprocessed data saved to {output_file}")

    return df


def calculate_complexity_scores(
    df: pd.DataFrame, verbose: bool = True, tophard: bool = False
) -> pd.DataFrame:
    """
    Calculate Flesch Reading Ease (FRE) score and Wiener Sachtextformel (WSTF) score for a given DataFrame.

    Args:
        df: The DataFrame containing the text to be analyzed.
        language (str, optional): The language of the text (Defaults to 'de' for German)

    Returns:
        A DataFrame with the Original and Leichte Sprache texts along with their respective scores.
    """

    # Calculate Flesch Reading Ease scores
    df['Original FRE Score'] = df['Original'].apply(calculate_fre_score)
    df['Leichte Sprache FRE Score'] = df['Leichte Sprache'].apply(calculate_fre_score)

    # Calculate Wiener Sachtextformel scores
    df['Original WSTF Score'] = df['Original'].apply(calculate_wstf_score)
    df['Leichte Sprache WSTF Score'] = df['Leichte Sprache'].apply(calculate_wstf_score)

    if verbose:
        # Calculate averages
        average_original = df['Original FRE Score'].mean().round(2)
        average_leichte_sprache = df['Leichte Sprache FRE Score'].mean().round(2)
        average_original_wstf = df['Original WSTF Score'].mean().round(2)
        average_leichte_sprache_wstf = df['Leichte Sprache WSTF Score'].mean().round(2)

        # Print scores and averages
        print("\n" + "=" * 80)
        print("\nText Complexity Scores")
        print("\nFlesch Reading Ease Score (low = hard, high = easy):")
        print("Average Original FRE Score:", average_original)
        print("Average Leichte Sprache FRE Score:", average_leichte_sprache)
        print("\n" + "-" * 80)
        print("\nWiener Sachtextformel: (min: 4 = easy, max: ~15 = hard)")
        print("Average Original WSTF Score:", round(average_original_wstf, 2))
        print("Average Leichte Sprache WSTF Score:", round(average_leichte_sprache_wstf, 2))

    if tophard:
        top_n = min(10, round(df.shape[0] * 0.1))
        print("\n" + "-" * 80)
        print(f"\nTop {top_n} hardest samples according Flesch Reading Ease Score:\n")
        fre_top = df.sort_values(by='Original FRE Score', ascending=True)[:top_n]
        print(
            fre_top[
                ["Original", "Original FRE Score", "Leichte Sprache", "Leichte Sprache FRE Score"]
            ].to_markdown()
        )

        print(f"\nTop {top_n} hardest samples according Wiener Sachtextformel Score:\n")
        wstf_top = df.sort_values(by='Original WSTF Score', ascending=False)[:top_n]
        print(
            wstf_top[
                [
                    "Original",
                    "Original WSTF Score",
                    "Leichte Sprache",
                    "Leichte Sprache WSTF Score",
                ]
            ].to_markdown()
        )

    return df


def plot_scores(
    df: pd.DataFrame,
    score_name: str = "FRE",
    save_file: bool = True,
    orig_file: str = None,
    show_graph: bool = True,
):
    """
    Plot a bar graph of the scores.

    Args:
        df: The DataFrame containing the text with respective scores.
        score_name (str, optional): The name of the score to plot. Defaults to "FRE".
        save_file (bool, optional): Whether to save the graph as an image. Defaults to True.
        orig_file (str, optional): The original file path for saving the graph. If None, a new filename will be generated.
        show_graph (bool, optional): Whether to display the graph in a window. Defaults to True.

    Returns:
        None
    """

    COLORS = [
        "black",
        "grey",
        "orange",
        "green",
        "brown",
        "darkcyan",
        "red",
        "blue",
    ]
    headers = df.columns.to_list()
    score_headers = [header for header in headers if score_name in header]
    colors = COLORS[: len(score_headers)]

    if not score_headers:
        raise ValueError("No score headers found for the specified score name.")

    # Average scores for plotting
    averages = [df[header].mean().round(2) for header in score_headers]

    df.plot.bar(x=None, y=score_headers, color=colors, figsize=(10, 7), legend=True)

    plt.title(f"{score_name} Scores")

    for average, header, color in zip(averages, score_headers, colors):
        plt.axhline(
            y=average,
            linestyle='--',
            label=f'Average {header}: ' + str(average),
            color=color,
        )

    plt.legend()
    plt.xlabel('Text Sample')
    plt.ylabel(f"{score_name} Score")
    plt.tight_layout()
    plt.grid(True)

    if save_file:
        if orig_file:
            file_name = get_new_file_path(
                orig_file, suffix=f"_{score_name}_scores", extension=".png"
            )
        else:
            file_name = f"{score_name}_scores.png"
        plt.savefig(file_name, dpi=200)

    if show_graph:
        plt.show()


def main(
    file_path: str, save_file: bool = True, plot: bool = True, verbose: bool = True
) -> pd.DataFrame:

    df = preprocess_data(file_path, save_file=False, verbose=verbose)

    df = calculate_complexity_scores(df, tophard=True)

    if verbose:
        print("\n" + "=" * 80)
        print("\nAnalysed Data Stats:\n")
        print(df.describe().to_markdown())

    output_filename = None
    if save_file:
        output_filename = get_new_file_path(file_path, suffix="_analysed")
        df.to_csv(output_filename, index=False, encoding="utf-8")
        print(f"\nSaved analysed dataset to {output_filename}")

    if plot:
        show_graph = True if df.shape[0] < 100 else False
        plot_scores(
            df, score_name="FRE", save_file=True, orig_file=output_filename, show_graph=show_graph
        )
        plot_scores(
            df, score_name="WSTF", save_file=True, orig_file=output_filename, show_graph=show_graph
        )

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze text complexity using Flesch Reading Ease and Wiener Sachtextformel scores."
    )
    parser.add_argument("file", type=str, help="Path to the input CSV file")
    args = parser.parse_args()

    main(args.file)
