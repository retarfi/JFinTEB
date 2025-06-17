# Leaderboard
This leaderboard shows the results of JFinTEB evaluations. The scores are all multiplied by 100.

## Summary

The summary shows the average scores within each task. The average score is the average of scores by dataset.

| Model                             | Avg.      | Classification   | Retrieval   | Clustering   |
|:----------------------------------|:----------|:-----------------|:------------|:-------------|
| sarashina-embedding-v1-1b         | **80.95** | **81.73**        | 93.46       | 26.23        |
| ruri-v3-130m                      | 79.07     | 79.33            | 92.25       | 24.80        |
| jina-embeddings-v3                | 79.02     | 77.42            | **94.03**   | 28.59        |
| GLuCoSE-base-ja-v2                | 78.55     | 78.97            | 91.15       | 25.69        |
| ruri-v3-70m                       | 77.68     | 78.33            | 90.56       | 22.29        |
| ruri-v3-310m                      | 77.20     | 75.60            | 92.70       | 26.42        |
| multilingual-e5-base              | 76.18     | 78.02            | 86.70       | 23.13        |
| multilingual-e5-large             | 72.07     | 67.85            | 91.73       | 27.18        |
| text-embedding-3-large            | 71.95     | 66.88            | 92.66       | **29.63**    |
| ruri-v3-30m                       | 70.78     | 66.70            | 90.45       | 24.76        |
| multilingual-e5-small             | 68.53     | 65.33            | 85.43       | 26.60        |
| text-embedding-3-small            | 67.32     | 62.45            | 87.04       | 27.39        |
| bert-base-japanese-fin-additional | 59.34     | 79.09            | 39.93       | 18.49        |
| bert-base-japanese                | 57.24     | 78.33            | 36.00       | 15.65        |

## Classification
| Model                             | Avg.      | chABSA    | Domain    | Horizon   | Sentiment   | Wikinews   | Industry17   |
|:----------------------------------|:----------|:----------|:----------|:----------|:------------|:-----------|:-------------|
| sarashina-embedding-v1-1b         | **81.73** | **96.03** | 78.11     | 82.80     | 55.94       | 94.57      | **82.93**    |
| multilingual-e5-large             | 79.67     | 93.93     | 74.63     | 81.90     | 53.34       | 95.17      | 79.05        |
| ruri-v3-310m                      | 79.36     | 95.56     | 77.09     | 83.04     | 53.91       | 94.34      | 72.19        |
| ruri-v3-130m                      | 79.33     | 90.34     | 77.73     | 82.64     | 54.94       | 94.56      | 75.79        |
| bert-base-japanese-fin-additional | 79.09     | 94.88     | 75.43     | 81.55     | 51.01       | 93.94      | 77.70        |
| GLuCoSE-base-ja-v2                | 78.97     | 92.76     | 76.41     | 80.75     | 49.78       | 94.97      | 79.13        |
| ruri-v3-30m                       | 78.54     | 91.10     | 76.92     | 80.03     | 51.50       | 94.14      | 77.54        |
| bert-base-japanese                | 78.33     | 93.01     | 73.63     | 82.04     | 51.28       | 93.52      | 76.50        |
| ruri-v3-70m                       | 78.33     | 92.60     | 76.91     | 81.54     | 52.07       | 93.94      | 72.92        |
| text-embedding-3-large            | 78.08     | 93.40     | **80.55** | **84.53** | **57.48**   | 94.11      | 58.40        |
| multilingual-e5-base              | 78.02     | 92.06     | 77.38     | 81.69     | 50.29       | 94.75      | 71.91        |
| jina-embeddings-v3                | 77.42     | 92.50     | 77.31     | 82.99     | 51.04       | 95.58      | 65.10        |
| multilingual-e5-small             | 76.45     | 90.42     | 77.91     | 77.50     | 46.99       | **96.00**  | 69.88        |
| text-embedding-3-small            | 73.67     | 87.46     | 78.81     | 80.88     | 52.06       | 91.25      | 51.52        |

## Retrieval
| Model                             | Avg.      | JaFIn     | PFMT      | Wikinews   | Wikipedia   |
|:----------------------------------|:----------|:----------|:----------|:-----------|:------------|
| jina-embeddings-v3                | **94.03** | **86.43** | **98.45** | 92.70      | 98.54       |
| sarashina-embedding-v1-1b         | 93.46     | 86.30     | 95.49     | 93.29      | **98.75**   |
| ruri-v3-310m                      | 92.70     | 85.27     | 95.67     | 93.14      | 96.72       |
| text-embedding-3-large            | 92.66     | 84.34     | 95.94     | 92.88      | 97.49       |
| ruri-v3-130m                      | 92.25     | 84.13     | 95.40     | **93.52**  | 95.93       |
| multilingual-e5-large             | 91.73     | 81.80     | 95.62     | 91.53      | 97.97       |
| GLuCoSE-base-ja-v2                | 91.15     | 78.31     | 97.83     | 91.67      | 96.80       |
| ruri-v3-70m                       | 90.56     | 82.08     | 95.17     | 93.13      | 91.86       |
| ruri-v3-30m                       | 90.45     | 81.16     | 93.69     | 92.88      | 94.06       |
| text-embedding-3-small            | 87.04     | 76.01     | 94.95     | 89.66      | 87.53       |
| multilingual-e5-base              | 86.70     | 70.47     | 94.28     | 88.73      | 93.31       |
| multilingual-e5-small             | 85.43     | 66.95     | 96.77     | 84.25      | 93.73       |
| bert-base-japanese-fin-additional | 39.93     | 35.26     | 49.96     | 52.69      | 21.79       |
| bert-base-japanese                | 36.00     | 31.59     | 40.84     | 57.44      | 14.11       |

## Clustering
| Model                             | Avg.      | Reason    |
|:----------------------------------|:----------|:----------|
| text-embedding-3-large            | **29.63** | **29.63** |
| jina-embeddings-v3                | 28.59     | 28.59     |
| text-embedding-3-small            | 27.39     | 27.39     |
| multilingual-e5-large             | 27.18     | 27.18     |
| multilingual-e5-small             | 26.60     | 26.60     |
| ruri-v3-310m                      | 26.42     | 26.42     |
| sarashina-embedding-v1-1b         | 26.23     | 26.23     |
| GLuCoSE-base-ja-v2                | 25.69     | 25.69     |
| ruri-v3-130m                      | 24.80     | 24.80     |
| ruri-v3-30m                       | 24.76     | 24.76     |
| multilingual-e5-base              | 23.13     | 23.13     |
| ruri-v3-70m                       | 22.29     | 22.29     |
| bert-base-japanese-fin-additional | 18.49     | 18.49     |
| bert-base-japanese                | 15.65     | 15.65     |

