{
  pfmt_bench_fin_ja: {
    class_path: 'RetrievalEvaluator',
    init_args: {
      val_query_dataset: {
        class_path: 'HfRetrievalQueryDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'validation',
          name: 'pfmt_bench_fin_ja-query',
        },
      },
      test_query_dataset: {
        class_path: 'HfRetrievalQueryDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'test',
          name: 'pfmt_bench_fin_ja-query',
        },
      },
      doc_dataset: {
        class_path: 'HfRetrievalDocDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'corpus',
          name: 'pfmt_bench_fin_ja-corpus',
        },
      },
      doc_chunk_size: 10000,
    },
  },
}
