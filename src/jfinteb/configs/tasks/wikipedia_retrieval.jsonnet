{
  wikipedia_retrieval: {
    class_path: 'RetrievalEvaluator',
    init_args: {
      val_query_dataset: {
        class_path: 'JsonlRetrievalQueryDataset',
        init_args: {
          filename: 'data/wikipedia/retrieval/query-validation.jsonl'
        },
      },
      test_query_dataset: {
        class_path: 'JsonlRetrievalQueryDataset',
        init_args: {
          filename: 'data/wikipedia/retrieval/query-test.jsonl'
        },
      },
      doc_dataset: {
        class_path: 'JsonlRetrievalDocDataset',
        init_args: {
          filename: 'data/wikipedia/retrieval/docs.jsonl',
        },
      },
      doc_chunk_size: 10000,
    },
  },
}
