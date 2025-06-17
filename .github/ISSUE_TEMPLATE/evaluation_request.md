---
name: Evaluation Request
about: モデル評価・リーダーボード追加のリクエスト
title: "[EVAL REQUEST] "
labels: "eval request"
assignees: ''

---

## モデルの基本情報
**name**: 
**type**: <!-- バックボーンモデル，例えば BERT, LLaMA... -->
**size**:
**lang**: ja / multilingual

## モデル詳細
<!-- 
学習手法，学習データなど，モデルの詳細について記載してください
-->


## seen/unseen申告
JFinTEBの評価データセットの中，training splitをモデル学習に使用した，またはvalidation setとして，ハイパラチューニングやearly stoppingに使用したデータセット名をチェックしてください。
* Classification
  * [ ] chABSA Classification
  * [ ] Economy Watchers Survey Domain
  * [ ] Economy Watchers Survey Horizon
  * [ ] Economy Watchers Survey Sentiment
  * [ ] Wikinews Classification
  * [ ] Industry17
* Retrieval
  * [ ] JaFIn
  * [ ] pfmt-bench-fin-ja
  * [ ] Wikinews Retrieval
  * [ ] Wikipedia Retrieval
* Clustering
  * [ ] Economy Watchers Survey Reason
* [ ] 申告しません


## 評価スクリプト
<!-- 
可能であれば評価用のスクリプトを記入してください。
モデルに合わせた特殊なセッティングは必ず書いてください。
-->

## その他の情報
