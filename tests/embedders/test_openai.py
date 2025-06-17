from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pytest
from pytest_mock import MockerFixture

from jfinteb.embedders import OpenAIEmbedder

OUTPUT_DIM = 1536  # the maximum dim of default model `text-embedding-3-small`
TEXT = "任意のテキスト"


@pytest.fixture(scope="function")
def mock_openai_embedder(mocker: MockerFixture):
    mocker.patch("jfinteb.embedders.openai_embedder.OpenAI")
    return OpenAIEmbedder(model="text-embedding-3-small")


@dataclass
class MockData:
    data: list


@dataclass
class MockEmbedding:
    embedding: list


class MockOpenAIClientEmbedding:
    def create(input: str | Iterable[str] | Iterable[int] | Iterable[Iterable[int]], model: str, **kwargs):
        if not input:
            raise ValueError("Empty string not allowed")
        if model == "text-embedding-ada-002":
            assert "dimensions" not in kwargs
            dimensions = OUTPUT_DIM
        else:
            assert "dimensions" in kwargs
            dimensions = kwargs.get("dimensions")
        if isinstance(input, str):
            input = [input]
        elif isinstance(input, Iterable):
            assert len(input) > 0
            if isinstance(input[0], int):
                # a list of token IDs is one sentence
                input = [input]
        return MockData(data=[MockEmbedding(embedding=[0.1] * dimensions)] * len(input))


@pytest.mark.usefixtures("mock_openai_embedder")
class TestOpenAIEmbedder:
    @pytest.fixture(autouse=True)
    def setup_class(cls, mocker: MockerFixture, mock_openai_embedder: OpenAIEmbedder):
        cls.model = mock_openai_embedder
        cls.mock_create = mocker.patch.object(cls.model.client, "embeddings", new=MockOpenAIClientEmbedding)

    def test_encode(self):
        embeddings = self.model.encode(TEXT)
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (OUTPUT_DIM,)

    def test_encode_multiple(self):
        embeddings = self.model.encode([TEXT] * 3)
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (3, OUTPUT_DIM)

    def test_get_output_dim(self):
        assert self.model.get_output_dim() == OUTPUT_DIM

    def test_token_count(self):
        # test if the right tiktoken encoding instance is being used
        assert len(self.model.encoding.encode(TEXT)) == 6

    def test_truncate(self):
        assert len(self.model.encode_and_truncate_text(TEXT)) == 6
        assert (
            len(self.model.encode_and_truncate_text(TEXT * self.model.max_token_length)) == self.model.max_token_length
        )

    def test_nonexistent_model(self):
        with pytest.raises(AssertionError):
            _ = OpenAIEmbedder(model="model")

    def test_model_dim(self):
        assert OpenAIEmbedder(model="text-embedding-3-large").dim == 3072
        assert OpenAIEmbedder(model="text-embedding-3-small").dim == 1536
        assert OpenAIEmbedder(model="text-embedding-ada-002").dim == 1536

    def test_model_max_token_length(self):
        assert OpenAIEmbedder(model="text-embedding-3-large").max_token_length == 8191
        assert OpenAIEmbedder(model="text-embedding-3-small").max_token_length == 8191
        assert OpenAIEmbedder(model="text-embedding-ada-002").max_token_length == 8191

    def test_model_encoder(self):
        assert OpenAIEmbedder(model="text-embedding-3-large").encoding.name == "cl100k_base"
        assert OpenAIEmbedder(model="text-embedding-3-small").encoding.name == "cl100k_base"
        assert OpenAIEmbedder(model="text-embedding-ada-002").encoding.name == "cl100k_base"

    def test_ada_002_dim(self):
        # check that no `dimensions` argument is set for model "text-embedding-ada-002"
        #   else an assertion error will be raised in MockOpenAIClientEmbedding
        #   and model "text-embedding-ada-002" has a fixed output dimension
        embeddings = OpenAIEmbedder(model="text-embedding-ada-002", dim=2 * OUTPUT_DIM).encode("任意のテキスト")
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (OUTPUT_DIM,)

        embeddings = OpenAIEmbedder(model="text-embedding-ada-002", dim=OUTPUT_DIM // 2).encode("任意のテキスト")
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (OUTPUT_DIM,)

    def test_dim_over_max(self):
        assert OpenAIEmbedder(dim=2 * OUTPUT_DIM).dim == OUTPUT_DIM

    def test_dim_smaller(self):
        assert OpenAIEmbedder(dim=OUTPUT_DIM // 2).dim == OUTPUT_DIM // 2

    def test_empty_string(self):
        embedder = OpenAIEmbedder()
        # check that an empty string is replaced by " ", else a ValueError will be raised.
        assert all(np.equal(embedder.encode(""), embedder.encode(" ")))
