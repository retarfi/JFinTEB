{
  economy_watchers_survey_domain: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/domain/train.jsonl',
        },
      },
      val_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/domain/validation.jsonl'
        },
      },
      test_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/domain/test.jsonl',
        },
      },
    },
  },
}
