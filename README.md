# JFinTEB: Japanese Financial Text Embedding Benchmark

<h4 align="center">
    <p>
        <b>README</b> |
        <a href="./leaderboard.md">leaderboard</a> |
        <a href="./submission.md">submission guideline</a>
    </p>
</h4>

JFinTEB is a financial benchmark for evaluating Japanese text embedding models.

This is an easy-to-use evaluation script designed for JFinTEB evaluation.

JFinTEB leaderboard is [here](leaderboard.md). If you would like to submit your model, please refer to the [submission guideline](submission.md).

## Quick start

```bash
git clone git@github.com:retarfi/JFinTEB
cd JFinTEB
poetry install
poetry run pytest tests
```

The following command evaluate the specified model on the all the tasks in JFinTEB.

```bash
poetry run python -m jfinteb \
  --embedder SentenceBertEmbedder \
  --embedder.model_name_or_path "<model_name_or_path>" \
  --save_dir "output/<model_name_or_path>"
```

> [!NOTE]
> In order to gurantee the robustness of evaluation, a validation dataset is mandatorily required for hyperparameter tuning.
> For a dataset that doesn't have a validation set, we set the validation set the same as the test set.

By default, the evaluation tasks are read from `src/jfinteb/configs/jfinteb.jsonnet`.
If you want to evaluate the model on a specific task, you can specify the task via `--evaluators` option with the task config.

```bash
poetry run python -m jfinteb \
  --evaluators "src/configs/tasks/jsts.jsonnet" \
  --embedder SentenceBertEmbedder \
  --embedder.model_name_or_path "<model_name_or_path>" \
  --save_dir "output/<model_name_or_path>"
```

> [!NOTE]
> If you want to exclude some tasks, use `--eval_exclude "`. Similarly, you can also use `--eval_include` to include only evaluation datasets you want.

> [!NOTE]
> If you want to log model predictions to further analyze the performance of your model, you may want to use `--log_predictions true` to enable all evaluators to log predictions. It is also available to set whether to log in the config of evaluators.

## Multi-GPU support

There are two ways to enable multi-GPU evaluation.

* New class `DataParallelSentenceBertEmbedder` ([here](src/jfinteb/embedders/data_parallel_sbert_embedder.py)).

```bash
poetry run python -m jfinteb \
  --evaluators "src/configs/tasks/jsts.jsonnet" \
  --embedder DataParallelSentenceBertEmbedder \
  --embedder.model_name_or_path "<model_name_or_path>" \
  --save_dir "output/<model_name_or_path>"
```

* With `torchrun`, multi-GPU in [`TransformersEmbedder`](src/jfinteb/embedders/transformers_embedder.py) is available. For example,

```bash
MODEL_NAME=<model_name_or_path>
MODEL_KWARGS="\{\'torch_dtype\':\'torch.bfloat16\'\}"
torchrun \
    --nproc_per_node=$GPUS_PER_NODE --nnodes=1 \
    src/jfinteb/__main__.py --embedder TransformersEmbedder \
    --embedder.model_name_or_path ${MODEL_NAME} \
    --embedder.pooling_mode cls \
    --embedder.batch_size 4096 \
    --embedder.model_kwargs ${MODEL_KWARGS} \
    --embedder.max_seq_length 512 \
    --save_dir "output/${MODEL_NAME}" \
    --evaluators src/jfinteb/configs/jfinteb.jsonnet
```

Note that the batch size here is global batch size (`per_device_batch_size` × `n_gpu`).

## Acknowledgements

This project is based on [JMTEB (Japanese Massive Text Embedding Benchmark)](https://github.com/sbintuitions/JMTEB) by [SB Intuitions](https://github.com/sbintuitions). We gratefully acknowledge their foundational work in Japanese text embedding evaluation.

The original JMTEB project is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/), and this project follows the same license terms.

If you use JMTEB or this benchmark, please cite the original dataset:

```
@misc{jmteb,
    author = {Li, Shengzhe and Ohagi, Masaya and Ri, Ryokan},
    title = {{J}{M}{T}{E}{B}: {J}apanese {M}assive {T}ext {E}mbedding {B}enchmark},
    howpublished = {\url{https://huggingface.co/datasets/sbintuitions/JMTEB}},
    year = {2024},
}
```
