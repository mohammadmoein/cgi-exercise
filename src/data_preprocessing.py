import pandas as pd
import category_encoders as ce
from sklearn.model_selection import train_test_split
from pathlib import Path
from src.constants import EN_NAME_DICT
from typing import List, Tuple
from sklearn.pipeline import make_pipeline


def read_excel_file(path: Path, nrows=317369) -> pd.DataFrame:
    assert path.suffix.endswith("xlsx"), "only supporting xlsx format"
    return pd.read_excel(path, nrows=nrows)


def drop_uninformative_colums(data_frame: pd.DataFrame, names: List) -> pd.DataFrame:
    return data_frame.drop(names, axis=1)


def remove_strip(data_frame: pd.DataFrame, col_name):
    return data_frame[col_name].astype("str").str.strip()


def extract_month_day(data_series: pd.Series):
    return data_series.str.extract(
        pat=r"(?P<month>\d{2})(?P<day>\d{2})", expand=True
    ).astype(int)


def preprocess_data(
    excel_file_path: Path,
    col_names_to_drop: List = [
        "Kuntanro",
        "Oulun kaupungin Y-tunnus",
        "Tosite numero",
        "Palveluluokka",
        "TILIN NIMI",
        "Toimittajan y-tunnus",
    ],
    nrows=317369,
):
    data_df = read_excel_file(excel_file_path, nrows=nrows)
    data_df = drop_uninformative_colums(data_df, col_names_to_drop)
    data_df.dropna(inplace=True)
    data_df[["Month", "Day"]] = extract_month_day(
        data_df["Tositepäivämäärä"].astype(str).str[2:]
    )
    data_df.drop("Tositepäivämäärä", axis=1, inplace=True)
    data_df["Toimittajan nimi"] = remove_strip(data_df, col_name="Toimittajan nimi")
    data_df.rename(columns=EN_NAME_DICT, inplace=True)
    return data_df


def categorical_encoding(
    data_frame: pd.DataFrame,
    categorical_low_cardinality_col_name: List,
    categorical_high_cardinality_col_name: List,
    high_cardinality_encoding_algorithm: str,
) -> pd.DataFrame:

    if high_cardinality_encoding_algorithm.lower() == "hashing":
        hce = ce.HashingEncoder(cols=categorical_high_cardinality_col_name)
    else:
        hce = ce.BinaryEncoder(cols=categorical_high_cardinality_col_name)

    lce = ce.OneHotEncoder(cols=categorical_low_cardinality_col_name)
    tranforms = make_pipeline(hce, lce, "passthrough")
    return tranforms.fit_transform(data_frame)


def build_train_test(
    data_frame: pd.DataFrame, test_size: float, seed: int
) -> Tuple[pd.DataFrame]:
    return train_test_split(data_frame, test_size=test_size, random_state=seed)
