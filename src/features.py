import pandas as pd
from sklearn.model_selection import train_test_split



def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Missing TotalCharges: naye customers, 0 rakh dete hain
    df["total_charges"] = df["total_charges"].fillna(0)

    # Target: Yes/No -> 1/0 (API ke liye churn column maujood nahi hota)
    if "churn" in df.columns:
        df["churn"] = (df["churn"] == "Yes").astype(int)

    # Naye features
    df["avg_monthly_spend"] = df["total_charges"] / df["tenure_months"].clip(lower=1)

    service_cols = ["online_security", "online_backup", "device_protection",
                    "tech_support", "streaming_tv", "streaming_movies"]
    df["num_services"] = sum((df[c] == "Yes").astype(int) for c in service_cols)

    df["is_new_customer"] = (df["tenure_months"] <= 12).astype(int)
    df["has_protection"] = ((df["online_security"] == "Yes") |
                            (df["tech_support"] == "Yes")).astype(int)

    return df


def get_train_test():
    from db import load_dataset

    df = build_features(load_dataset())

    X = df.drop(columns=["customer_id", "churn"])
    y = df["churn"]

    # Categorical columns ko one-hot encode
    X = pd.get_dummies(X, drop_first=True)

    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_train_test()
    print("Train:", X_train.shape, "Test:", X_test.shape)
    print("Churn rate train:", round(y_train.mean(), 3))