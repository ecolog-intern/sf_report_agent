# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path


def check_csv_match(csv1_path: str, csv2_path: str) -> dict:
    """
    Check if columns and shape match between two CSV files.

    Args:
        csv1_path: Path to first CSV file
        csv2_path: Path to second CSV file

    Returns:
        dict: Comparison results
    """
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    result = {
        "csv1": {
            "path": csv1_path,
            "shape": df1.shape,
            "columns": list(df1.columns),
        },
        "csv2": {
            "path": csv2_path,
            "shape": df2.shape,
            "columns": list(df2.columns),
        },
        "columns_match": set(df1.columns) == set(df2.columns),
        "shape_match": df1.shape == df2.shape,
    }

    if not result["columns_match"]:
        result["columns_only_in_csv1"] = list(set(df1.columns) - set(df2.columns))
        result["columns_only_in_csv2"] = list(set(df2.columns) - set(df1.columns))

    return result


def check_inputs_folder() -> dict:
    """
    Compare CSV files in checker/inputs folder.
    Requires exactly 2 CSV files in the folder.
    """
    inputs_dir = Path(__file__).parent / "inputs"

    if not inputs_dir.exists():
        raise FileNotFoundError(f"inputs folder not found: {inputs_dir}")

    csv_files = list(inputs_dir.glob("*.csv"))

    if len(csv_files) != 2:
        raise ValueError(f"inputs folder requires exactly 2 CSV files. Found: {len(csv_files)}")

    return check_csv_match(str(csv_files[0]), str(csv_files[1]))


def main():
    result = check_inputs_folder()

    print("=" * 50)
    print("CSV Comparison Result")
    print("=" * 50)
    print(f"\nCSV1: {result['csv1']['path']}")
    print(f"  Shape: {result['csv1']['shape']}")
    print(f"  Columns: {result['csv1']['columns']}")

    print(f"\nCSV2: {result['csv2']['path']}")
    print(f"  Shape: {result['csv2']['shape']}")
    print(f"  Columns: {result['csv2']['columns']}")

    print("\n" + "-" * 50)
    print(f"Columns match: {'⭕️' if result['columns_match'] else '❌'}")
    print(f"Shape match: {'⭕️' if result['shape_match'] else '❌'}")

    if not result["columns_match"]:
        if result.get("columns_only_in_csv1"):
            print(f"\nColumns only in CSV1: {result['columns_only_in_csv1']}")
        if result.get("columns_only_in_csv2"):
            print(f"Columns only in CSV2: {result['columns_only_in_csv2']}")


if __name__ == "__main__":
    main()
