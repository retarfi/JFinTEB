import random
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from . import BAR_FMT, P_DATA

BASE_URL: str = "https://ja.wikinews.org"


def get_article_urls(url: str) -> tuple[list[str], Optional[str]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article_urls = []
    for link in soup.find("ul", {"class": "mw-allpages-chunk"}).find_all("a"):
        href = link.get("href")
        if (
            href
            and href.startswith("/wiki/")
            and not href.startswith("/wiki/%E5%88%A5%E7%A8%AE:")
            and not href.startswith(
                "/wiki/%E5%8D%8A%E9%9A%8E%E5%8F%8A%E3%81%B3%E5%8D%8A%E9%9A%8E%E3%82%92%E5%90%AB%E3%82%80"
            )
        ):
            article_urls.append(BASE_URL + href)
    next_url_cands = soup.find("div", {"class": "mw-allpages-nav"}).find_all("a")
    next_url_cands = [x for x in next_url_cands if "次のページ" in x.text]
    if len(next_url_cands) > 1:
        print(next_url_cands)
        raise AssertionError
    if len(next_url_cands) == 0:
        next_url = None
    else:
        next_url = BASE_URL + next_url_cands[0].get("href")
    return article_urls, next_url


def get_all_article_urls() -> list[str]:
    page_url = "https://ja.wikinews.org/wiki/%E7%89%B9%E5%88%A5:%E3%83%9A%E3%83%BC%E3%82%B8%E4%B8%80%E8%A6%A7"
    print("Paging for index...")
    article_urls = []
    while True:
        # print("paging for index:", page_url)
        article_urls_new, page_url = get_article_urls(page_url)
        article_urls.extend(article_urls_new)
        if not page_url:
            break
        time.sleep(1)
    return article_urls


def get_article_content(article_url: str) -> Optional[dict[str, str]]:
    response = requests.get(article_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("div", {"id": "mw-normal-catlinks"})
    if not tag:
        print(f"Article {article_url} has no category links.")
        return None
    lst_category: list[str] = [x["title"].lstrip("カテゴリ:") for x in tag.find("ul").find_all("a")]
    if len({"政治", "経済"} & set(lst_category)) == 0:
        return None
    title = soup.find("h1", {"class": "firstHeading"}).text
    content = "".join([x.text for x in soup.find("div", {"id": "mw-content-text"}).find_all("p")[1:]])
    data: dict[str, str] = {
        "title": title,
        "text": content.replace("\n", ""),
        "categories": lst_category,
    }
    return data


def to_classification(lst_data: dict[str, str]) -> None:
    train_ratio: float = 0.7
    dev_ratio: float = 0.1

    data: list[dict[str, str]] = []
    for x in lst_data:
        set_category = {"政治", "経済"} & set(x["categories"])
        if len(set_category) != 1:
            continue
        data.append({"text": x["text"], "label": list(set_category)[0]})

    n_train: int = int(len(data) * train_ratio)
    n_dev: int = int(len(data) * dev_ratio)
    p_save: Path = P_DATA / "wikinews" / "classification"
    p_save.mkdir(parents=True, exist_ok=True)
    for lst, split in zip(
        [data[:n_train], data[n_train : n_train + n_dev], data[n_train + n_dev :]],
        ["train", "validation", "test"],
    ):
        if len(lst) > 0:
            pd.DataFrame(lst).to_json(p_save / f"{split}.jsonl", orient="records", force_ascii=False, lines=True)
    print(f"Saved classification data to {p_save}")


def to_retrieval(lst_data: dict[str, str]) -> None:
    dev_ratio: float = 0.2
    shuffle: bool = True
    seed: int = 42

    p_save: Path = P_DATA / "wikinews" / "retrieval"
    p_save.mkdir(parents=True, exist_ok=True)

    lst_queries: list[dict[str, str]] = [
        {"query": x["title"], "relevant_docs": [i + 1]} for i, x in enumerate(lst_data)
    ]
    lst_docs: list[dict[str, str]] = [{"docid": i + 1, "text": x["text"]} for i, x in enumerate(lst_data)]
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


def create_wikinews_dataset() -> None:
    article_urls: list[str] = get_all_article_urls()

    lst_data: dict[str, str] = []
    for article_url in tqdm(article_urls, bar_format=BAR_FMT):
        data: Optional[dict[str, str]] = get_article_content(article_url)
        if data:
            lst_data.append(data)
        time.sleep(0.8)

    to_classification(lst_data)
    to_retrieval(lst_data)


if __name__ == "__main__":
    create_wikinews_dataset()
