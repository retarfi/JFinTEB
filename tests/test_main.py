import subprocess
import tempfile
from pathlib import Path

from evaluator.test_sts_evaluator import DummySTSDataset

from jfinteb.__main__ import main
from jfinteb.evaluators import STSEvaluator


def test_main(embedder):
    main(
        text_embedder=embedder,
        evaluators={"sts": STSEvaluator(val_dataset=DummySTSDataset(), test_dataset=DummySTSDataset())},
        save_dir=None,
        overwrite_cache=False,
    )


def test_main_cli():
    with tempfile.TemporaryDirectory() as f:
        # fmt: off
        command = [
            "python", "-m", "jfinteb",
            "--embedder", "tests.conftest.DummyTextEmbedder",
            "--embedder.model_kwargs", '{"torch_dtype": "torch.float16"}',
            "--save_dir", f,
            "--eval_include", '["jafin"]',
            "--log_predictions", "true",
        ]
        # fmt: on
        result = subprocess.run(command)
        assert result.returncode == 0
        assert (Path(f) / "jfinteb_config.yaml").exists()
        assert (Path(f) / "summary.json").exists()
