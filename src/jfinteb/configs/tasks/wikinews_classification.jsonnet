{
  wikinews_classification: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikinews/clustering/validation.jsonl',
        },
      },
      val_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikinews/clustering/validation.jsonl',
        },
      },
      test_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikinews/clustering/test.jsonl',
        },
      },
    },
  },
}
