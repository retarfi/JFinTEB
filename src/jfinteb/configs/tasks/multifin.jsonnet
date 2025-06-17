{
  multifin_ja: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'HfClassificationDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'train',
          name: 'multifin_ja',
        },
      },
      val_dataset: {
        class_path: 'HfClassificationDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'validation',
          name: 'multifin_ja',
        },
      },
      test_dataset: {
        class_path: 'HfClassificationDataset',
        init_args: {
          path: 'retarfi/JFinTEB',
          split: 'test',
          name: 'multifin_ja',
        },
      },
    },
  },
}
