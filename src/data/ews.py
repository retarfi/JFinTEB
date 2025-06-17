import argparse
import random
from pathlib import Path
from typing import Any

from datasets import Dataset, DatasetDict, concatenate_datasets, load_dataset

from . import P_DATA

COL_TEXT: str = "text"
COL_LABEL: str = "label"
COLUMNS: list[str] = ["id", COL_TEXT, COL_LABEL]


def load_dataset_from_hf(tense: str, version: str, col_text: str) -> Dataset:
    splits: tuple[str] = ("train", "validation", "test")
    dsd: DatasetDict = load_dataset("retarfi/economy-watchers-survey", tense, revision=version)
    ds: Dataset = concatenate_datasets([dsd[split] for split in splits])
    ds = ds.rename_column(col_text, COL_TEXT)
    ds = filter_short_text(ds, min_length=10)
    return ds


def filter_short_text(ds: Dataset, min_length: int) -> Dataset:
    return ds.filter(lambda x: len(x[COL_TEXT]) >= min_length)


def sample(lst: list[Any], num_samples: int, seed: int) -> list[Any]:
    assert len(lst) >= num_samples
    random.seed(seed)
    return random.sample(lst, num_samples)


def query_samples(
    ds: Dataset,
    labels: tuple[str, ...],
    num_each_label: int,
    seed: int,
    train_ratio: float = 0.7,
    dev_ratio: float = 0.1,
) -> DatasetDict:
    df: Dataset = ds.to_pandas()
    dct_counter: dict[str, int] = df[COL_LABEL].value_counts().to_dict()
    assert all(dct_counter[label] >= num_each_label for label in labels)
    n_train: int = int(num_each_label * train_ratio)
    n_dev: int = int(num_each_label * dev_ratio)
    train_data: list[int] = []
    dev_data: list[int] = []
    test_data: list[int] = []
    for label in labels:
        idx: list[int] = df[df[COL_LABEL] == label].index.tolist()
        idx_sample: list[int] = sample(idx, num_each_label, seed)
        train_data.extend(idx_sample[:n_train])
        dev_data.extend(idx_sample[n_train : n_train + n_dev])
        test_data.extend(idx_sample[n_train + n_dev :])
    dsd: DatasetDict = DatasetDict(
        {
            split: ds.select(sorted(data)).select_columns(COLUMNS)
            for split, data in zip(("train", "validation", "test"), (train_data, dev_data, test_data))
            if len(data) > 0
        }
    )
    return dsd


def domain(ds_current: Dataset, ds_future: Dataset, seed: int) -> DatasetDict:
    labels: tuple[str, ...] = ("家計動向", "企業動向", "雇用")
    ds_q: Dataset = concatenate_datasets(
        [ds.rename_column("関連", COL_LABEL).select_columns(COLUMNS) for ds in (ds_current, ds_future)]
    )
    dsd: DatasetDict = query_samples(ds_q, labels, num_each_label=2000, seed=seed)
    return dsd


def horizon(ds_current: Dataset, ds_future: Dataset, seed: int) -> DatasetDict:
    labels: tuple[str, str] = ("現状", "先行き")
    ds_all: Dataset = concatenate_datasets(
        [
            ds.add_column(COL_LABEL, [label] * len(ds)).select_columns(COLUMNS)
            for ds, label in zip((ds_current, ds_future), labels)
        ]
    )
    dsd: DatasetDict = query_samples(ds_all, labels, num_each_label=5000, seed=seed)
    return dsd


def reason(ds: Dataset, seed: int) -> Dataset:
    # Clustering
    labels: tuple[str, ...] = (
        "来客数の動き",
        "販売量の動き",
        "お客様の様子",
        "受注量や販売量の動き",
        "単価の動き",
        "取引先の様子",
        "求人数の動き",
        "競争相手の様子",
        "受注価格や販売価格の動き",
        "周辺企業の様子",
        "求職者数の動き",
        "採用者数の動き",
        "雇用形態の様子",
    )
    dsd: DatasetDict = query_samples(
        ds.rename_column("判断の理由", COL_LABEL),
        labels,
        num_each_label=1000,
        train_ratio=0.0,
        dev_ratio=0.5,
        seed=seed,
    )
    return dsd


def sentiment(ds_current: Dataset, ds_future: Dataset, seed: int) -> DatasetDict:
    labels: tuple[str, ...] = ("×", "▲", "□", "○", "◎")
    ds_q_current: Dataset = ds_current.rename_column("景気の現状判断", COL_LABEL)
    ds_q_future: Dataset = ds_future.rename_column("景気の先行き判断", COL_LABEL)
    ds_q: Dataset = concatenate_datasets([ds_q_current.select_columns(COLUMNS), ds_q_future.select_columns(COLUMNS)])
    dsd: DatasetDict = query_samples(ds_q, labels, num_each_label=2000, seed=seed)
    return dsd


def save_as_jsonl(dsd: DatasetDict, p_save: Path) -> None:
    p_save.mkdir(exist_ok=True, parents=True)
    for split in dsd.keys():
        dsd[split].to_json(p_save / f"{split}.jsonl", force_ascii=False)


def create_ews_dataset(tasks: list[str], ews_version: str) -> None:
    seed: int = 42
    p_save: Path = P_DATA / "economy-watchers-survey"
    p_save.mkdir(exist_ok=True, parents=True)

    ds_current: Dataset = load_dataset_from_hf("current", ews_version, "追加説明及び具体的状況の説明")
    ds_future: Dataset = load_dataset_from_hf("future", ews_version, "景気の先行きに対する判断理由")

    for task in tasks:
        dsd: DatasetDict
        if task == "domain":
            dsd = domain(ds_current, ds_future, seed=seed)
        elif task == "reason":
            dsd = reason(ds_current, seed=seed)
        elif task == "sentiment":
            dsd = sentiment(ds_current, ds_future, seed=seed)
        elif task == "horizon":
            dsd = horizon(ds_current, ds_future, seed=seed)
        else:
            raise ValueError(f"Unknown task: {task}")
        save_as_jsonl(dsd, p_save / task)
        print(f"Saved domain dataset to {p_save / task}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create EWS dataset")
    choices_task: list[str] = ["domain", "horizon", "reason", "sentiment"]
    parser.add_argument(
        "--tasks",
        nargs="+",
        type=str,
        choices=choices_task,
        default=choices_task,
        help="Tasks to create dataset for ({})".format(", ".join(choices_task)),
    )
    parser.add_argument(
        "--ews_version",
        type=str,
        default="2025.05.0",
        help="Version of the Economy Watchers Survey dataset to use",
    )
    args: argparse.Namespace = parser.parse_args()
    create_ews_dataset(tasks=args.tasks, ews_version=args.ews_version)
