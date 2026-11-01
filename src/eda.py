import matplotlib.pyplot as plt
import seaborn as sns
from db import load_dataset

df = load_dataset()

print("Shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum()[df.isnull().sum() > 0])
print("\nChurn distribution:")
print(df["churn"].value_counts(normalize=True).round(3))

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

sns.countplot(data=df, x="churn", ax=axes[0, 0])
axes[0, 0].set_title("Churn Distribution")

sns.countplot(data=df, x="contract", hue="churn", ax=axes[0, 1])
axes[0, 1].set_title("Churn by Contract")

sns.histplot(data=df, x="tenure_months", hue="churn", bins=30, ax=axes[1, 0])
axes[1, 0].set_title("Tenure vs Churn")

sns.boxplot(data=df, x="churn", y="monthly_charges", ax=axes[1, 1])
axes[1, 1].set_title("Monthly Charges vs Churn")

plt.tight_layout()
plt.savefig("notebooks/eda_overview.png", dpi=120)
plt.show()