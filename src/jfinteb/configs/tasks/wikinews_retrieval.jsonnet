{
  wikinews_retrieval: {
    class_path: 'RetrievalEvaluator',
    init_args: {
      val_query_dataset: {
        class_path: 'JsonlRetrievalQueryDataset',
        init_args: {
          filename: 'data/wikinews/retrieval/query-validation.jsonl'
        },
      },
      test_query_dataset: {
        class_path: 'JsonlRetrievalQueryDataset',
        init_args: {
          filename: 'data/wikinews/retrieval/query-test.jsonl'
        },
      },
      doc_dataset: {
        class_path: 'JsonlRetrievalDocDataset',
        init_args: {
          filename: 'data/wikinews/retrieval/docs.jsonl',
        },
      },
      doc_chunk_size: 10000,
    },
  },
}
