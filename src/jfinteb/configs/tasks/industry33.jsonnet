{
  industry33: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikipedia/industry33/train.jsonl',
        },
      },
      val_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikipedia/industry33/validation.jsonl',
        },
      },
      test_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/wikipedia/industry33/test.jsonl',
        },
      },
    },
  },
}
