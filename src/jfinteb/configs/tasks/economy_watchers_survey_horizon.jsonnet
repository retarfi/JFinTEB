{
  economy_watchers_survey_horizon: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/horizon/train.jsonl',
        },
      },
      val_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/horizon/validation.jsonl'
        },
      },
      test_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/horizon/test.jsonl',
        },
      },
    },
  },
}
