{
  economy_watchers_survey_reason: {
    class_path: 'ClusteringEvaluator',
    init_args: {
      val_dataset: {
        class_path: 'JsonlClusteringDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/reason/validation.jsonl',
        },
      },
      test_dataset: {
        class_path: 'JsonlClusteringDataset',
        init_args: {
          filename: 'data/economy-watchers-survey/reason/test.jsonl',
        },
      },
    },
  },
}
