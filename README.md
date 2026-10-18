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

The supported application is the FastAPI/SQLite workbench above. The legacy stack is separately checked for build, startup, protected-route rejection and unavailable-model behavior. It is not an end-to-end trained fraud service: role-based user workflows, historical batch imports, outbox workers, drift studies and prospective real-data validation remain outside the completed workbench scope. Docker Compose is not required for the workbench.

## Attribution

This branch extends the owner's existing code with AI-assisted implementation. Review and understand contributions before claiming ownership of specific methods. The synthetic generator and workbench were implemented for this project; third-party libraries retain their licenses. No new repository-wide license is asserted; the earlier README license badge was unsupported by a repository license file.

Background for the future simulator/validation study: https://fraud-detection-handbook.github.io/fraud-detection-handbook/ . Do not claim results on that simulator until it is actually integrated and evaluated.

## Real public-data evaluation

The [reproducible GitHub run](https://github.com/AliAkbar129/Fraudlens/actions/runs/39120684582) evaluated the original Worldline/ULB credit-card dataset (OpenML 1597): 284,807 rows before removing 1,081 exact duplicates. Time-ordered train/validation/calibration/test partitions contain 170,235 / 42,557 / 28,373 / 42,561 rows. The test period contains only 52 frauds.

Validation selected logistic regression over histogram gradient boosting. Held-out average precision is **0.701836**, ROC AUC **0.975016**. The descriptive 95% time-block bootstrap interval for AP is **[0.517027, 0.838312]** (300 resamples). At 10 retrospective reviews per observed hour, 60 reviews identify 33 of 52 frauds (55% precision, 63.46% recall). This ranking requires the completed hour; it is not an online alert policy.

See [machine-readable results](research_lab/evidence/ulb/evaluation.json), [raw test predictions](research_lab/evidence/ulb/test_predictions.csv.gz), and [protocol](research_lab/REAL_DATA_PROTOCOL.md). Reproduce with:

```bash
python -m research_lab.download_ulb
python -m research_lab.real_benchmark --data data/ulb/creditcard.arff --output research_lab/evidence/ulb
```

Two historical days cannot establish production performance. Customer IDs are absent, original PCA fitting provenance is unknown, and this evaluation does not model delayed labels. Calibration clips saturated scores; AP changes are not evidence of improved discrimination. Live transaction scoring remains synthetic because its features differ from ULB.

## Finalization verification

The research workflow passes seven tests. Legacy CI now checks 19 Python tests, targeted Python correctness diagnostics and type checking, PHP tests and PHPStan level 0, frontend lint/type checking, two utility tests and a production build. Fixes include deterministic graph-model evaluation, tensor-based graph explanations, strict SHAP feature schemas, dependency installation, API route registration, frontend API proxying and explicit unavailable-model failures. These checks do not establish production readiness or an exhaustive browser/security audit.

The Docker integration job builds the stack and checks healthy startup, gateway HTML, backend health, protected API HTTP 401, and unavailable-model HTTP 503. See the [CI history](https://github.com/AliAkbar129/Fraudlens/actions/workflows/ci.yml) for the result at the commit you use. The stack uses the PHP development server and localhost ports; it is for local integration only.

To reproduce that integration check (Docker Compose required):

```bash
cp docker/.env.example .env
python -c "import base64,secrets;open('.env','a').write('APP_KEY=base64:'+base64.b64encode(secrets.token_bytes(32)).decode()+'\n')"
docker compose up -d --build --wait --wait-timeout 180
```

Open http://127.0.0.1:8088 for the labelled legacy prototype. Use the Python setup at the top of this README for the functional decision workbench.
