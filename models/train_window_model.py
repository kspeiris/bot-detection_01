from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

WINDOW_FILE = PROJECT_ROOT / "data" / "window_features.csv"
MODEL_FILE = PROJECT_ROOT / "models" / "window_bot_model.pkl"
LOGISTIC_MODEL_FILE = PROJECT_ROOT / "models" / "window_logistic_model.pkl"
IMPORTANCE_PLOT = PROJECT_ROOT / "models" / "window_feature_importance.png"
METRICS_FILE = PROJECT_ROOT / "models" / "window_metrics.json"
ARTIFACTS = [MODEL_FILE, LOGISTIC_MODEL_FILE, IMPORTANCE_PLOT]
DROP_COLUMNS = ["analysis_unit_id", "session_id", "actor_type", "bot_type", "label", "start_time", "window_size_seconds", "window_index"]


def reset_artifacts(message, extra=None):
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    for artifact in ARTIFACTS:
        artifact.unlink(missing_ok=True)

    payload = {
        "status": "unavailable",
        "message": message,
        "dataset_rows": 0,
        "train_rows": 0,
        "test_rows": 0,
        "held_out_sessions": [],
        "label_counts": {},
        "logistic_accuracy": None,
        "random_forest_accuracy": None,
    }
    if extra:
        payload.update(extra)
    METRICS_FILE.write_text(json.dumps(payload, indent=2))


def load_dataset():
    if not WINDOW_FILE.exists():
        print(f"Window feature file not found: {WINDOW_FILE}")
        return None
    df = pd.read_csv(WINDOW_FILE)
    if df.empty:
        print("Window feature file is empty. Run feature extraction first.")
        return None
    session_counts = df.groupby("label")["session_id"].nunique()
    if len(session_counts) < 2 or session_counts.min() < 2:
        print("Need at least 2 unique sessions per class for grouped window training.")
        print(session_counts.to_string())
        return None
    return df


def grouped_split(df):
    feature_columns = [column for column in df.columns if column not in DROP_COLUMNS]
    session_labels = df[["session_id", "label"]].drop_duplicates().sort_values(["label", "session_id"])
    held_out_sessions = session_labels.groupby("label").tail(1)["session_id"].tolist()
    train_df = df[~df["session_id"].isin(held_out_sessions)]
    test_df = df[df["session_id"].isin(held_out_sessions)]
    return train_df[feature_columns], test_df[feature_columns], train_df["label"], test_df["label"], feature_columns, held_out_sessions


def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()
    print(f"=== {name} Accuracy ===")
    print(f"{accuracy:.4f}")
    print(f"Predictions: {list(y_pred)}")
    print(f"Actual: {list(y_test)}")
    return accuracy


def save_feature_importance(model, feature_names):
    IMPORTANCE_PLOT.parent.mkdir(parents=True, exist_ok=True)
    importances = pd.Series(model.feature_importances_, index=feature_names).sort_values()
    plt.figure(figsize=(9, 7))
    plt.barh(importances.index, importances.values)
    plt.xlabel("Importance")
    plt.title("Window Random Forest Feature Importance")
    plt.tight_layout()
    plt.savefig(IMPORTANCE_PLOT, dpi=150)
    plt.close()
    print(f"Saved window feature importance plot to {IMPORTANCE_PLOT}")


def main():
    df = load_dataset()
    if df is None:
        reset_artifacts("Window training data is unavailable or incomplete.")
        return

    X_train, X_test, y_train, y_test, feature_columns, held_out_sessions = grouped_split(df)
    print(f"Held-out sessions: {held_out_sessions}")

    logistic_model = LogisticRegression(max_iter=1000, random_state=42)
    logistic_model.fit(X_train, y_train)
    logistic_accuracy = evaluate_model("Window Logistic Regression", logistic_model, X_test, y_test)
    LOGISTIC_MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(logistic_model, LOGISTIC_MODEL_FILE)

    rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_accuracy = evaluate_model("Window Random Forest", rf_model, X_test, y_test)
    joblib.dump(rf_model, MODEL_FILE)
    save_feature_importance(rf_model, feature_columns)

    print("=== Window Model Comparison ===")
    print(f"Logistic Regression: {logistic_accuracy:.4f}")
    print(f"Random Forest: {rf_accuracy:.4f}")

    METRICS_FILE.write_text(
        json.dumps(
            {
                "status": "ready",
                "message": "Window model trained successfully.",
                "dataset_rows": int(len(df)),
                "train_rows": int(len(X_train)),
                "test_rows": int(len(X_test)),
                "held_out_sessions": held_out_sessions,
                "label_counts": {str(label): int(count) for label, count in df["label"].value_counts().to_dict().items()},
                "logistic_accuracy": round(float(logistic_accuracy), 4),
                "random_forest_accuracy": round(float(rf_accuracy), 4),
                "feature_columns": feature_columns,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
