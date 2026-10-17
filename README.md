# FraudLens — Decision Lab and legacy prototype

This repository now contains an executable **local synthetic-data research workbench** in `research_lab/`, alongside the earlier Laravel/React/Flutter prototype. It is not an enterprise deployment or validated bank fraud detector.

## Run the measured workbench

Python 3.12, from repository root:

```bash
python -m venv .venv
# Activate .venv for your shell.
python -m pip install -r research_lab/requirements.txt
python -m research_lab.experiment
python -m pytest -q research_lab/tests
python -m uvicorn research_lab.api:app --host 127.0.0.1 --port 8011
```

Open http://127.0.0.1:8011. The responsive workbench shows measured model comparisons, scores new transactions, saves cases in SQLite, enforces case transitions and revision checks, and displays an audit trail. The mutation key defaults to `local-demo-only` for localhost use; override `FRAUD_LAB_KEY`. This is not a role-based production authorization system.

`FRAUD_MODEL` and `FRAUD_DB` override artifact/database paths. Model artifacts are trusted local files, never arbitrary uploads. Historical replay requires increasing timestamps. Duplicate ID/content submissions return the original result; conflicting reuse is rejected.

## Research protocol

A small seed-controlled local generator produces 45 days of transactions with stylized amount/time fraud mechanisms. It is **not** the Fraud Detection Handbook simulator and does not represent a real bank. The baseline is an engineering milestone toward the larger planned study.

Use chronological train/validation/test periods. Two-day label availability constrains training and model selection. Features use only previous transaction history; labels never enter the predictor. Compare rules, logistic regression and histogram gradient boosting using average precision and precision/recall at 5, 10 and 25 daily reviews. The selected model is chosen by validation average precision, not test performance.

An actual seed-42 run is in `research_lab/evidence/synthetic_seed42.json`, including the full comparison and limitations. Scores are not independently calibrated probabilities. Reviewed fraudulent amounts are simulated sums, not recovered money. One seeded run does not establish statistical significance.

## Legacy code status

The original React screens include mock demonstrations; they are now labelled as a legacy prototype. API failures no longer masquerade as successful empty responses. The legacy hybrid scoring endpoints now refuse fixed predictions; model-loader fabricated metrics were removed. PHP scoring failures throw rather than recording zero fraud risk. The Laravel transaction wraps scoring and rolls back on this exception; it does not silently retain a successfully scored transaction.

The new workbench deliberately does not pretend to integrate every legacy component. Laravel/MySQL integration, role-based users, historical batch imports, outbox workers, drift studies and real-data validation remain unfinished. The old Docker Compose deployment is not the workbench's setup and was not validated in this environment; PHP and Docker were unavailable.

## Attribution

This branch extends the owner's existing code with AI-assisted implementation. Review and understand contributions before claiming ownership of specific methods. The synthetic generator and workbench were implemented for this project; third-party libraries retain their licenses. No new repository-wide license is asserted; the earlier README license badge was unsupported by a repository license file.

Background for the future simulator/validation study: https://fraud-detection-handbook.github.io/fraud-detection-handbook/ . Do not claim results on that simulator until it is actually integrated and evaluated.
