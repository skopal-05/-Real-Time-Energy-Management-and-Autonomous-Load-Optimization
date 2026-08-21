# Module 7 - Explainable AI and Performance Evaluation

## Scope

This module implements the complete Week 7 work assigned to Person 1 and
Person 2:

- forecasting and decision-pipeline performance evaluation;
- baseline-versus-optimized benchmarking;
- model monitoring and drift detection;
- safe retraining candidate evaluation;
- global feature importance;
- exact Shapley-value explanations; and
- Isolation Forest anomaly detection.

Person 3's `integration/` final controller and end-to-end test are intentionally
not included. The standalone runner reads existing artifacts only to validate
Person 1/2 components with representative project data.

## Structure

```text
evaluation/
  performance_evaluator.py
  metrics.py
  benchmark.py
  evaluation_validator.py
retraining/
  retraining_pipeline.py
  model_monitor.py
  retraining_validator.py
explainability/
  shap_analyzer.py
  feature_importance.py
  explanation_generator.py
anomaly_detection/
  isolation_forest.py
  anomaly_detector.py
  anomaly_validator.py
outputs/
  performance/
  explanations/
  anomalies/
  reports/
tests/
  test_person_1.py
  test_person_2.py
run_person_1_2.py
```

## Person 1

### Performance evaluation

Forecasts are evaluated using MAE, MSE, RMSE, MAPE, SMAPE, WAPE, R2, bias,
and maximum error. MAPE ignores zero-valued actual samples while SMAPE and
WAPE provide complementary zero-safe percentage measures.

RMSE remains model-specific because the seven targets use different units.
Only dimensionless WAPE, SMAPE, and R2 are summarized across models.

The pipeline report also measures:

- recommendation setpoint and constraint coverage from Module 4;
- scenario count, ranks, score spread, and selected scenario from Module 5;
- key baseline-versus-optimized energy, cost, and carbon indicators from
  Module 6.

### Monitoring and retraining

The Model Monitor checks relative MAE/RMSE degradation, absolute R2 decline,
an R2 quality floor, and standardized feature-mean drift. A retraining trigger
includes explicit reasons.

The Retraining Pipeline uses a holdout comparison. It never modifies Module 3
models by default. A candidate is persisted only when it is accepted and the
caller explicitly supplies `promotion_path`.

## Person 2

### Explainability

The SHAP Analyzer computes exact single-reference Shapley values by enumerating
all feature coalitions. Module 3 models have only three to six features, so this
requires at most 64 coalition predictions per sample. Every explanation checks
the additive identity:

```text
prediction = base value + sum(feature contributions)
```

Native Random Forest feature importance provides the global ranking. The
Explanation Generator combines it with local SHAP contributions and creates
structured, readable summaries.

### Anomaly detection

Isolation Forest learns normal multivariate operating behavior without anomaly
labels. Outputs contain a normalized anomaly score, raw score, label, Boolean
flag, and source values for every checked record.

## Run

From the project root:

```bash
python3 "Module 7 - Explainable AI & Performance Evaluation/run_person_1_2.py"
```

Run tests:

```bash
python3 -m unittest discover \
  -s "Module 7 - Explainable AI & Performance Evaluation/tests" \
  -v
```

Expected: `Ran 21 tests` followed by `OK`.

## Outputs

- `outputs/performance/performance_report.json`
- `outputs/performance/model_monitoring.json`
- `outputs/performance/retraining_report.json`
- `outputs/explanations/feature_importance.json`
- `outputs/explanations/shap_explanations.json`
- `outputs/anomalies/anomaly_report.json`
- `outputs/reports/person_1_2_summary.json`

## Compatibility finding

The current Module 3 Joblib artifacts were created with scikit-learn 1.9.0 but
the available project runtime uses 1.7.1. The runner captures those warnings in
the performance report. Results can be reviewed, but production deployment
should retrain and save the models using one pinned environment.
