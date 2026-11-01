import json
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
from features import get_train_test

X_train, X_test, y_train, y_test = get_train_test()

# Imbalance handle karne ke liye: No / Yes ka ratio
pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

models = {
    "LogisticRegression": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    ),
    "RandomForest": RandomForestClassifier(
        n_estimators=300, max_depth=8, class_weight="balanced",
        random_state=42, n_jobs=-1,
    ),
    "XGBoost": XGBClassifier(
        n_estimators=300, max_depth=4, learning_rate=0.05,
        scale_pos_weight=pos_weight, eval_metric="logloss",
        random_state=42,
    ),
}

results = []
fitted = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)

    results.append({
        "model": name,
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "precision": round(precision_score(y_test, pred), 4),
        "recall": round(recall_score(y_test, pred), 4),
        "f1": round(f1_score(y_test, pred), 4),
    })
    fitted[name] = model

results_df = pd.DataFrame(results).sort_values("roc_auc", ascending=False)
print(results_df.to_string(index=False))

best_name = results_df.iloc[0]["model"]
print("\nBest model:", best_name)

joblib.dump(fitted[best_name], "src/model.joblib")
json.dump(list(X_train.columns), open("src/feature_columns.json", "w"))
results_df.to_csv("notebooks/model_comparison.csv", index=False)