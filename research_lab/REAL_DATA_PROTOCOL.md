# ULB/Worldline retrospective evaluation

Dataset: original OpenML 1597, creditcard v1, 284,807 transactions. Source: https://www.openml.org/search?type=data&id=1597. Cite Dal Pozzolo et al., Calibrating Probability with Undersampling for Unbalanced Classification, IEEE CIDM 2015. OpenML licence field: Public. This repository does not redistribute the original transaction features.

The protocol was fixed before the first local test results; the GitHub Actions run reproduces it after a workspace reset. Remove exact duplicate rows and split chronologically at time quantiles 60/75/85 percent, retaining equal timestamps in one partition. Train scaling and models only on the first 60%; select balanced logistic regression or fixed histogram boosting on validation average precision; sigmoid calibration uses the next 10%; the final 15% is test. Features: Amount and published V1–V28. No invented card IDs or oversampling.

Report all models, amount-ranking and training-prevalence references. Metrics: average precision, AUROC, Brier for probabilities, top 5/10/25 reviews per observed hour, and 300-replicate 30-minute block-bootstrap AP interval. Budgets are retrospective rankings, not causal online policies. Partial hours remain partial. Only 52 frauds occur in this split's test set. Two days cannot establish long-term drift or label-delay performance; original PCA fitting provenance is unknown.

Run `python research_lab/download_ulb.py`, then `python research_lab/real_benchmark.py --data data/ulb/creditcard.arff`. The workflow saves measured JSON and all test predictions for 90 days; the publication step also commits the evidence to this branch. Live app scoring remains a separate explicitly synthetic model.
