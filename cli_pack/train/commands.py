from pathlib import Path
import pandas as pd
import click
from loguru import logger
from cli_pack.utils import PathPath
from src.train import build_train_model
from typing import List,Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import json

MODELS = {"RF":RandomForestClassifier,"KNN":KNeighborsClassifier,"DT":DecisionTreeClassifier}
@click.group()
def magik():
    pass


@magik.command("train")
@click.option(
    "--train-csv-path",
    "-tr",
    help="path to train csv file",
    type=PathPath(),
)
@click.option(
    "--test-csv-path",
    "-te",
    help="path to test csv file",
    type=PathPath(),
)
@click.option(
    "--target",
    "-t",
    help="taret column name",
    type=str,
    multiple=True,
    required=True
)
@click.option(
    "--model",

    type=click.Choice(["RF","DT","KNN"]),
    default="RF",   
    help="Path to hparams config file"
)
@click.option(
    "--hparams-config",
    "-hp",
    type=PathPath(),
    help="Path to hparams config file"
)
@click.option(
    "--dest-dir",
    "-d",
    help="dir to save trained model and test result",
    type=PathPath(),
)
def train(train_csv_path: Path, test_csv_path: Path, target: Tuple, model:str,hparams_config:Path,dest_dir:Path) -> None:
    logger.debug(target)
    model = MODELS[model]
    hp_dict = json.load(open(hparams_config))
    build_train_model(model,train_csv_path,test_csv_path,targets=list(target),hparams=hp_dict,cv=2,dest_path=dest_dir)
