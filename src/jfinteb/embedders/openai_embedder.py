from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import tiktoken
from loguru import logger
from openai import OpenAI

from jfinteb.embedders.base import TextEmbedder


@dataclass
class OpenAIEmbedderConfig:
    max_output_dim: int
    encoder_name: str
    max_token_length: int


OPENAI_EMBEDDERS = {
    # https://platform.openai.com/docs/guides/embeddings/embedding-models
    "text-embedding-3-large": OpenAIEmbedderConfig(3072, "cl100k_base", 8191),
    "text-embedding-3-small": OpenAIEmbedderConfig(1536, "cl100k_base", 8191),
    "text-embedding-ada-002": OpenAIEmbedderConfig(1536, "cl100k_base", 8191),
}


class OpenAIEmbedder(TextEmbedder):
    """Embedder via OpenAI API."""

    def __init__(self, model: str = "text-embedding-3-small", dim: int | None = None) -> None:
        """Setup.
        model and dim: see https://platform.openai.com/docs/models/embeddings
        `text-embedding-3-large` model: max 3072 dim
        `text-embedding-3-small` model: max 1536 dim
        `text-embedding-ada-002` model: max 1536 dim

        OpenAI embeddings have been normalized to length 1. See
            https://platform.openai.com/docs/guides/embeddings/which-distance-function-should-i-use

        As OpenAI embedding APIs don't allow an empty string as input, we replace an
        empty string with a space " " to avoid error.

        Args:
            model (str, optional): Name of an OpenAI embedding model.
                Defaults to "text-embedding-3-small".
            dim (int, optional): Output dimension. Defaults to 1536.
        """
        self.client = OpenAI()  # API key written in .env
        assert model in OPENAI_EMBEDDERS.keys(), f"`model` must be one of {list(OPENAI_EMBEDDERS.keys())}!"
        self.model = model
        model_config = OPENAI_EMBEDDERS[model]
        self.encoding = tiktoken.get_encoding(model_config.encoder_name)
        self.max_token_length = model_config.max_token_length
        if not dim or model == "text-embedding-ada-002":
            self.dim = model_config.max_output_dim
        else:
            if dim > model_config.max_output_dim:
                self.dim = model_config.max_output_dim
                logger.warning(f"The maximum dimension of model {self.model} is {self.dim}, " f"use dim={self.dim}.")
            else:
                self.dim = dim

        self.convert_to_tensor = False
        self.convert_to_numpy = True

    def encode(self, text: str | list[str], prefix: str | None = None) -> np.ndarray:
        kwargs = {"dimensions": self.dim} if self.model != "text-embedding-ada-002" else {}
        # specifying `dimensions` is not allowed for "text-embedding-ada-002"

        # 必要に応じてテキストを前処理（空文字列の処理など）
        if isinstance(text, str):
            processed_text = self.preprocess_text(text, prefix)

            # 単一テキストの場合の処理
            result = np.asarray(
                [
                    data.embedding
                    for data in self.client.embeddings.create(
                        input=[processed_text],
                        model=self.model,
                        **kwargs,
                    ).data
                ]
            )
            return result.reshape(-1)
        else:
            processed_texts = [self.preprocess_text(t, prefix) for t in text]

            # OpenAIのAPIの制限に基づいてバッチサイズを調整
            # 制限は300,000トークン
            MAX_API_TOKENS = 100000

            # テキストごとのトークン数を取得
            text_token_counts = [len(self.encoding.encode(t)) for t in processed_texts]

            # バッチ処理のための初期化
            all_embeddings = []
            current_batch = []
            current_tokens = 0

            # トークン数に基づいてバッチを作成
            for i, (t, token_count) in enumerate(zip(processed_texts, text_token_counts)):
                # このテキストを追加するとトークン制限を超える場合
                is_over_limit = current_tokens + token_count > MAX_API_TOKENS
                if is_over_limit and current_batch:
                    # 現在のバッチを処理
                    batch_size = len(current_batch)
                    logger.debug(f"Processing batch with {batch_size} texts, " f"{current_tokens} tokens")
                    batch_result = self.client.embeddings.create(
                        input=current_batch,  # current_batchは既にリスト形式
                        model=self.model,
                        **kwargs,
                    )
                    embeddings = [data.embedding for data in batch_result.data]
                    all_embeddings.extend(embeddings)

                    # 新しいバッチを開始
                    current_batch = [t]
                    current_tokens = token_count
                else:
                    # 現在のバッチにテキストを追加
                    current_batch.append(t)
                    current_tokens += token_count

            # 最後のバッチを処理
            if current_batch:
                batch_size = len(current_batch)
                logger.debug(f"Processing final batch with {batch_size} texts, " f"{current_tokens} tokens")
                batch_result = self.client.embeddings.create(
                    input=current_batch,  # current_batchは既にリスト形式
                    model=self.model,
                    **kwargs,
                )
                embeddings = [data.embedding for data in batch_result.data]
                all_embeddings.extend(embeddings)

            # 結果を返す
            result = np.asarray(all_embeddings)
            return result

    def get_output_dim(self) -> int:
        return self.dim

    def preprocess_text(self, text: str, prefix: str | None = None) -> str:
        """テキストを前処理して、APIに送信する前に必要な調整を行う

        Args:
            text: 処理するテキスト
            prefix: プレフィックス（OpenAIでは使用しない）

        Returns:
            前処理済みのテキスト
        """
        # 空文字列の処理
        if not text:
            text = " "
            logger.warning("Found empty string!")

        # プレフィックスは無視（コメントを残す）
        # Ignore prefix in OpenAIEmbedder

        # トークン数をチェックし、必要に応じて切り詰める
        tokens = self.encoding.encode(text)
        if len(tokens) > self.max_token_length:
            # 切り詰めが必要な場合は、トークンを切り詰めて再度デコード
            truncated_tokens = tokens[: self.max_token_length]
            text = self.encoding.decode(truncated_tokens)
            logger.debug(f"Text truncated from {len(tokens)} to {self.max_token_length} tokens")

        return text

    def encode_and_truncate_text(self, text: str, prefix: str | None = None) -> list[int]:
        """後方互換性のために残す（使用されない）"""
        # Refer to OpenAI's cookbook for token counting
        # return a list of token IDs
        if not text:
            text = " "
            logger.warning("Found empty string!")
        # Ignore prefix in OpenAIEmbedder
        return self.encoding.encode(text)[: self.max_token_length]
