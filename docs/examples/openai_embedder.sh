model=$1

export OPENAI_API_KEY=<your_openai_api_key>

echo "Running OpenAI model: $model"

echo "start"
date "+%Y-%m-%d %H:%M:%S"
echo ""

poetry run python -m jfinteb \
  --embedder OpenAIEmbedder \
  --embedder.model "$model" \
  --save_dir "results/${model//\//_}" \
  --overwrite_cache false \
  --evaluators src/jfinteb/configs/jfinteb.jsonnet

echo ""
date "+%Y-%m-%d %H:%M:%S"
echo "end"