{
  wikinews_classification: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikinews/classification/train.jsonl',
        },
      },
      val_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikinews/classification/validation.jsonl',
        },
      },
      test_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikinews/classification/test.jsonl',
        },
      },
    },
  },
}
