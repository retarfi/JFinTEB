model=$1

echo "Running model: $model"

echo "start"
date "+%Y-%m-%d %H:%M:%S"
echo ""

poetry run python -m jfinteb \
  --embedder SentenceBertEmbedder \
  --embedder.model_name_or_path "$model" \
  --embedder.model_kwargs '{"torch_dtype": "torch.float16"}' \
  --embedder.device cuda \
  --save_dir "results/${model//\//_}" \
  --overwrite_cache false \
  --evaluators src/jfinteb/configs/jfinteb.jsonnet \
  --eval_exclude "['amazon_review_classification', 'mrtydi', 'jaqket', 'esci']"

echo ""
date "+%Y-%m-%d %H:%M:%S"
echo "end"