{
  chabsa_classification: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'HfClassificationDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'train',
          name: 'chabsa_classification',
        },
      },
      val_dataset: {
        class_path: 'HfClassificationDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'validation',
          name: 'chabsa_classification',
        },
      },
      test_dataset: {
        class_path: 'HfClassificationDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'test',
          name: 'chabsa_classification',
        },
      },
    },
  },
}
