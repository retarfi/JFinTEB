{
  economy_watchers_survey_sentiment: {
    class_path: 'ClassificationEvaluator',
    init_args: {
      train_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/sentiment/train.jsonl',
        },
      },
      val_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/sentiment/validation.jsonl'
        },
      },
      test_dataset: {
        class_path: 'JsonlClassificationDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/sentiment/test.jsonl',
        },
      },
    },
  },
}
