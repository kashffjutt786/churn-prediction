import joblib
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
from features import get_train_test

_, X_test, _, y_test = get_train_test()
model = joblib.load("src/model.joblib")
proba = model.predict_proba(X_test)[:, 1]

for t in np.arange(0.3, 0.75, 0.05):
    pred = (proba >= t).astype(int)
    print(f"t={t:.2f}  precision={precision_score(y_test, pred):.3f}  "
          f"recall={recall_score(y_test, pred):.3f}  f1={f1_score(y_test, pred):.3f}")