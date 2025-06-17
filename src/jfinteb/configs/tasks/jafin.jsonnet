{
  jafin: {
    class_path: 'RetrievalEvaluator',
    init_args: {
      val_query_dataset: {
        class_path: 'HfRetrievalQueryDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'validation',
          name: 'jafin-query',
        },
      },
      test_query_dataset: {
        class_path: 'HfRetrievalQueryDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'test',
          name: 'jafin-query',
        },
      },
      doc_dataset: {
        class_path: 'HfRetrievalDocDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'corpus',
          name: 'jafin-corpus',
        },
      },
      doc_chunk_size: 10000,
    },
  },
}
