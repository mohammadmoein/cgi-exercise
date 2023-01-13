from pathlib import Path
import pandas as pd
import click
from loguru import logger
from cli_pack.utils import PathPath
from src.data_preprocessing import preprocess_data, categorical_encoding,build_train_test
from typing import List


@click.group()
def data():
    pass


@data.command("parse")
@click.option(
    "--excel-file-path",
    "-s",
    help="path to data excel file",
    type=PathPath(),
)
@click.option(
    "--dest-dir",
    "-d",
    help="the destination dir to save the processed dataset",
    type=PathPath(),
)
@click.option(
    "--col-name",
    "-c",
    multiple=True,
    default=(
        "Kuntanro",
        "Oulun kaupungin Y-tunnus",
        "Tosite numero",
        "Palveluluokka",
        "TILIN NIMI",
        "Toimittajan y-tunnus",
    ),
)
@click.option(
    "--nrows",
    default=317369,
    help="number of rows to be read from the excel file",
    type=int,
)
def parse(excel_file_path: Path, dest_dir: Path, col_name: List, nrows: int) -> None:
    data_df = preprocess_data(
        excel_file_path, col_names_to_drop=list(col_name), nrows=nrows
    )
    try:
        assert data_df.isna().any().any() == False
        data_df.to_csv(
            dest_dir.joinpath("processed_data").with_suffix(".csv"), index=False
        )
        logger.info(
            f"{excel_file_path.stem} was pre-processed and saved under {dest_dir}"
        )

    except AssertionError as e:
        logger.exception(e)


@data.command("split")
@click.option(
    "--src-file", "-s", type=PathPath(), help="path to file that is processed"
)
@click.option(
    "--dest-dir",
    "-d",
    help="the destination dir to save the processed dataset",
    type=PathPath(),
)
@click.option(
    "--seed",
    default=33,
    help="seed value to to random split",
    type=int,
)
@click.option(
    "--test-size",
    default=0.2,
    help="test size in a value of between 0 and 1",
    type=float,
)
def split(src_file:Path, dest_dir:Path, seed:int, test_size:float):
    assert src_file.suffix.endswith("csv"), "not supported other format than csv"
    data_df = pd.read_csv(src_file)
    train_df,test_df = build_train_test(data_df,test_size=test_size,seed=seed)
    dest_dir = dest_dir.joinpath(f'seed_{seed}')
    dest_dir.mkdir(exist_ok=True,parents=True)
    train_df.to_csv(dest_dir.joinpath('train.csv'),index=False)
    test_df.to_csv(dest_dir.joinpath('test.csv'),index=False)
    logger.info(f'test/train : {seed} is saved {dest_dir}')

@data.command("encode")
@click.option("--src-file", "-s", help="path to processed data", type=PathPath())
@click.option(
    "--categorical-low-cardinality-col-names",
    "--lcn",
    multiple=True,
    help="categorical variable col name with low cardinality",
    default=("Municipality", "Vendor country code"),
)
@click.option(
    "--dest-dir",
    "-d",
    help="the destination dir to save the processed dataset",
    type=PathPath(),
)
@click.option(
    "--categorical-high-cardinality-col-names",
    "--lcn",
    multiple=True,
    help="categorical variable col name with high cardinality",
    default=("Cost center", "Vendor name", "Day", "Month"),
)
@click.option(
    "--algorithm",
    "-alg",
    help="algorithm to handle high cardinality categorical values",
    type=click.Choice(["hashing", "binary"]),
    required=True,
)
def encode(
    src_file,
    dest_dir,
    categorical_low_cardinality_col_names,
    categorical_high_cardinality_col_names,
    algorithm,
):
    logger.info('Starting encoding categorical to numeric values')
    data_df = pd.read_csv(src_file)
    data_df = categorical_encoding(
        data_df,
        categorical_low_cardinality_col_name=list(categorical_low_cardinality_col_names),
        categorical_high_cardinality_col_name=list(categorical_high_cardinality_col_names),
        high_cardinality_encoding_algorithm=algorithm,
    )
    dest_path = dest_dir.joinpath('encoded_dataset').with_suffix('.csv')
    data_df.to_csv(dest_path,index=False)
    logger.info(f'Encoded dataset is saved under {dest_path}')
    #     data_frame: pd.DataFrame,
    # categorical_low_cardinality_col_name: List,
    # categorical_high_cardinality_col_name: List,
    # high_cardinality_encoding_algorithm: str,
    # categorical_encoding
