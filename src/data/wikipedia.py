import argparse
import bz2
import random
import re
from pathlib import Path
from typing import Optional

import pandas as pd
from tqdm import tqdm

from . import P_DATA


def collect_pages(text, filter_template=None, filter_category=None):
    """
    :param text: the text of a wikipedia file dump.
    :param filter_template: template name to filter articles (e.g., '基礎情報 会社')
    :param filter_category: category name to filter articles (e.g., '経済')
    """
    # we collect individual lines, since str.join() is significantly faster
    # than concatenation
    page = []
    id = ""
    last_id = ""
    inText = False
    redirect = False
    tagRE = re.compile(r"(.*?)<(/?\w+)[^>]*>(?:([^<]*)(<.*?>)?)?")
    for line in text:
        if "<" not in line:  # faster than doing re.search()
            if inText:
                page.append(line)
            continue
        m = tagRE.search(line)
        if not m:
            continue
        tag = m.group(2)
        if tag == "page":
            page = []
            redirect = False
        elif tag == "id" and not id:
            id = m.group(3)
        elif tag == "title":
            title = m.group(3)
        elif tag == "redirect":
            redirect = True
        elif tag == "text":
            inText = True
            line = line[m.start(3) : m.end(3)]
            page.append(line)
            if m.lastindex == 4:  # open-close
                inText = False
        elif tag == "/text":
            if m.group(1):
                page.append(m.group(1))
            inText = False
        elif inText:
            page.append(line)
        elif tag == "/page":
            colon = title.find(":")
            if colon < 0 and id != last_id and not redirect:
                # Check if template filter is specified
                if filter_template is None and filter_category is None:
                    yield (title, page)
                    last_id = id
                else:
                    # Check if the specified template and/or category exists in the page
                    page_text = "".join(page)

                    # Check template condition
                    template_found = True  # Default to True if no template filter
                    if filter_template:
                        template_found = False
                        if f"{{{{{filter_template}" in page_text:
                            template_found = True

                    # Check category condition
                    category_found = True  # Default to True if no category filter
                    if filter_category:
                        category_found = f"[[Category:{filter_category}]]" in page_text

                    # Both conditions must be satisfied (AND condition)
                    if template_found and category_found:
                        yield (title, page)
                        last_id = id
            id = ""
            page = []
            inText = False
            redirect = False


def load_articles(filepath: str) -> list[tuple[str, str, str]]:
    lst: list[tuple[str, str, str]] = []
    with bz2.open(filepath, "rt", encoding="utf-8") as f:
        for title, page in tqdm(collect_pages(f, filter_template=None, filter_category="東証プライム上場企業")):
            lst.append((title, page))
    return lst


def load_industry_map(xlspath: str) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    df: pd.DataFrame = pd.read_excel(xlspath)
    df["コード"] = df["コード"].astype(str)
    dct_industry: dict[str, dict[str, str]] = {
        ds["コード"]: {f"industry{x}": ds[f"{x}業種区分"] for x in (17, 33)} for _, ds in df.iterrows()
    }
    dct_company: dict[str, str] = dict(zip(df["コード"], df["銘柄名"]))
    return dct_industry, dct_company


def extract_ticker(lst: list[str]) -> Optional[str]:
    for line in lst:
        line = line.replace("'", "")
        m = re.search(r"上場情報\s*\|\s*(取引所=)*(東証)*(プライム|1部)(市場)*\s*\|", line)
        if m and "プライム" in line:
            line = re.sub(r"\s", "", line)
            m = re.search(r"プライム(市場)*\|(コード=)*([A-Z0-9]{4})", line)
            assert m, line
            return m.group(3)


def cut_template(lst: list[str]) -> list[str]:
    start_index = None
    for i, line in enumerate(lst):
        if line.startswith("{{"):
            start_index = i
            break
    assert start_index is not None

    bracket_count = 0
    for i in range(start_index, len(lst)):
        line = lst[i]
        open_brackets = line.count("{{")
        close_brackets = line.count("}}")
        bracket_count += open_brackets - close_brackets
        if bracket_count == 0 and i > start_index:
            return lst[:start_index] + lst[i + 1 :]
    raise ValueError("対応する終了位置が見つかりませんでした。")


def cut_after_overview(lst: list[str]) -> list[str]:
    for i, line in enumerate(lst):
        if re.fullmatch(r"==.*?==\s*\n", line) and "概要" not in line:
            return lst[:i]


def _process_tags(line: str) -> str:
    line = re.sub(r"&lt;!--.*?--&gt;", "", line)
    line = re.sub(r"\{\{Sfn.*?\}\}", "", line)
    line = re.sub(r"&lt;ref.*?&gt;.*?&lt;/ref&gt;", "", line)
    line = re.sub(r"\[\[([^\|\[\]]*?)\]\]", r"\1", line)
    line = re.sub(r"\[\[[^\|\[\]]*?\|([^\|\[\]]*?)\]\]", r"\1", line)
    line = re.sub(r"\{\{[^\|\{\}]*?\|([^\|\{\}]*?)\}\}", r"\1", line)
    line = re.sub(r"\{\{[^\{]*?\}\}", "", line)
    line = re.sub(r"&lt;ref.*?/&gt;", "", line)
    line = line.replace("'''", "").replace("''", "")
    line = line.replace("&amp;", "&").strip()
    return line


def process_tags(lst: list[str]) -> str:
    output = []
    for line in lst:
        if (
            line == "\n"
            or re.match(r"&lt;/*gallery&gt;\n", line)
            or (re.fullmatch(r"==.*?==\n", line) and "概要" in line)
            or re.fullmatch(r"(\[\[)*(ファイル|File|file):.*?(\]\])*\n", line)
        ):
            continue
        output.append(_process_tags(line))
    return "".join(_process_tags("".join(output)))


def process_data(lst_articles: list[tuple[str, list[str]]], xlspath: str) -> list[dict[str, str]]:
    dct_industry: dict[str, dict[str, str]]
    dct_company: dict[str, str]
    dct_industry, dct_company = load_industry_map(xlspath)
    industry_categories: list[str] = list(list(dct_industry.values())[0].keys())

    data: list[dict[str, str]] = []
    for title, page in lst_articles:
        ticker = extract_ticker(page)
        if not ticker:
            continue
        if ticker not in dct_industry.keys():
            print(f"Ticker {ticker} not found in industry map for {title}. Skipping.")
            continue
        page = cut_after_overview(page)
        page = [line for line in page if not line.startswith("{{") or not line.endswith("}}\n")]
        for _ in range(10):
            if any(line.startswith("{{") for line in page):
                page = cut_template(page)
            else:
                break
        else:
            raise ValueError(title)
        text: str = process_tags(page)
        dct: dict[str, str] = {
            "ticker": ticker,
            "company-name": dct_company[ticker],
            "text": text,
        }
        for category in industry_categories:
            dct[category] = dct_industry[ticker][category]
        data.append(dct)
    data = sorted(data, key=lambda x: x["ticker"])
    return data


def to_classification(
    data: list[dict[str, str]],
    train_ratio: float,
    dev_ratio: float,
    shuffle: bool = True,
    seed: int = 42,
) -> None:
    train_ratio: float = 0.7
    dev_ratio: float = 0.1

    for industry in ("industry17", "industry33"):
        p_save: Path = P_DATA / "wikipedia" / industry
        p_save.mkdir(parents=True, exist_ok=True)

        lst_data: list[dict[str, str]] = []
        for dct in data:
            if dct[industry] == "-":
                continue
            lst_data.append({"text": dct["text"], "label": dct[industry]})

        if shuffle:
            random.seed(seed)
            random.shuffle(lst_data)

        length: int = len(lst_data)
        n_train: int = int(length * train_ratio)
        n_dev: int = int(length * dev_ratio)
        for lst, split in zip(
            [
                lst_data[:n_train],
                lst_data[n_train : n_train + n_dev],
                lst_data[n_train + n_dev :],
            ],
            ["train", "validation", "test"],
        ):
            pd.DataFrame(lst).to_json(
                p_save / f"{split}.jsonl",
                orient="records",
                force_ascii=False,
                lines=True,
            )
        print(f"Saved {industry} data to {p_save}")


def to_retrieval(
    data: list[dict[str, str]],
    dev_ratio: float = 0.2,
    shuffle: bool = True,
    seed: int = 42,
) -> None:
    p_save: Path = P_DATA / "wikipedia" / "retrieval"
    p_save.mkdir(parents=True, exist_ok=True)

    lst_queries: list[dict[str, str]] = []
    lst_docs: list[dict[str, str]] = []

    for i, dct in enumerate(data):
        lst_queries.append({"query": dct["company-name"], "relevant_docs": [i + 1]})
        lst_docs.append({"docid": i + 1, "text": dct["text"]})

    if shuffle:
        random.seed(seed)
        random.shuffle(lst_docs)

    n_dev: int = int(len(lst_queries) * dev_ratio)
    for lst, split in zip([lst_queries[:n_dev], lst_queries[n_dev:]], ["validation", "test"]):
        pd.DataFrame(lst).to_json(
            p_save / f"query-{split}.jsonl",
            orient="records",
            force_ascii=False,
            lines=True,
        )

    pd.DataFrame(lst_docs).to_json(p_save / "docs.jsonl", orient="records", force_ascii=False, lines=True)
    print(f"Saved retrieval data to {p_save}")


def create_wikipedia_dataset(filepath: str, xlspath: str) -> None:
    lst_articles: list[tuple[str, str, list[str]]] = load_articles(filepath)
    data: list[dict[str, str]] = process_data(lst_articles, xlspath)

    to_classification(data)
    to_retrieval(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Wikipedia dataset for classification and retrieval tasks.")
    parser.add_argument(
        "--filepath",
        type=str,
        default="data/jawiki-20250601-pages-articles.xml.bz2",
        help="Path to the Wikipedia dump file.",
    )
    parser.add_argument(
        "--xlspath",
        type=str,
        default="data/data_j.xls",
        help="Path to the Excel file containing industry information.",
    )
    args = parser.parse_args()
    create_wikipedia_dataset(args.filepath, args.xlspath)
