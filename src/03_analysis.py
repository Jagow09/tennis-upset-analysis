import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

CLEAN_DIR  = "data/clean/"
OUTPUT_DIR = "output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(CLEAN_DIR, "atp_clean.csv"))
RANK_GAP_THRESHOLD = 10
df = df[df["rank_gap"] >= RANK_GAP_THRESHOLD].copy()
df = df[df["surface"] != "Carpet"]
print(f"Loaded {len(df)} matches")

# ── Upset by level ────────────────────────────────────────────────────────────
upset_by_level = (
    df.groupby("tourney_level_name")["upset"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "upset_rate", "count": "total_matches"})
    .reset_index()
    .sort_values("upset_rate", ascending=False)
)
print("\nUpset rates by tournament level:")
print(upset_by_level)
upset_by_level.to_csv(os.path.join(OUTPUT_DIR, "upset_by_level.csv"), index=False)

# ── Upset by surface ──────────────────────────────────────────────────────────
upset_by_surface = (
    df.groupby("surface")["upset"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "upset_rate", "count": "total_matches"})
    .reset_index()
    .sort_values("upset_rate", ascending=False)
)
print("\nUpset rates by surface:")
print(upset_by_surface)
upset_by_surface.to_csv(os.path.join(OUTPUT_DIR, "upset_by_surface.csv"), index=False)

# ── Upset by surface and level ────────────────────────────────────────────────
upset_by_surface_level = (
    df.groupby(["surface", "tourney_level_name"])["upset"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "upset_rate", "count": "total_matches"})
    .reset_index()
    .sort_values("upset_rate", ascending=False)
)
print("\nUpset rates by surface and level:")
print(upset_by_surface_level)
upset_by_surface_level.to_csv(
    os.path.join(OUTPUT_DIR, "upset_by_surface_level.csv"), index=False
)

# ── Upset by tournament ───────────────────────────────────────────────────────
upset_by_tournament = (
    df.groupby(["tourney_name", "tourney_level_name"])["upset"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "upset_rate", "count": "total_matches"})
    .reset_index()
    .sort_values("upset_rate", ascending=False)
)
upset_by_tournament = upset_by_tournament[
    upset_by_tournament["total_matches"] >= 100
]
print("\nUpset rates by tournament:")
print(upset_by_tournament.to_string())
upset_by_tournament.to_csv(
    os.path.join(OUTPUT_DIR, "upset_by_tournament.csv"), index=False
)

# ── Upset by round ────────────────────────────────────────────────────────────
round_order = ["R128", "R64", "R32", "R16", "QF", "SF", "F"]
upset_by_round = (
    df.groupby(["round", "tourney_level_name"])["upset"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "upset_rate", "count": "total_matches"})
    .reset_index()
)
upset_by_round["round"] = pd.Categorical(
    upset_by_round["round"], categories=round_order, ordered=True
)
upset_by_round = upset_by_round.sort_values(["round", "tourney_level_name"])
print("\nUpset rates by round:")
print(upset_by_round)
upset_by_round.to_csv(os.path.join(OUTPUT_DIR, "upset_by_round.csv"), index=False)

# ── Upset by ranking gap ──────────────────────────────────────────────────────
df["rank_gap_bucket"] = pd.cut(
    df["rank_gap"],
    bins=[10, 25, 50, 100, 200, 500, 2000],
    labels=["10-25", "26-50", "51-100", "101-200", "201-500", "500+"]
)
upset_by_gap = (
    df.groupby("rank_gap_bucket", observed=True)["upset"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "upset_rate", "count": "total_matches"})
    .reset_index()
)
print("\nUpset rates by ranking gap:")
print(upset_by_gap)
upset_by_gap.to_csv(os.path.join(OUTPUT_DIR, "upset_by_gap.csv"), index=False)

# ── Logistic regression model ─────────────────────────────────────────────────
df_model = df.copy()
df_model = pd.get_dummies(
    df_model,
    columns=["surface", "round", "tourney_level_name"],
    drop_first=True
)

feature_cols = ["rank_gap"]
for col in df_model.columns:
    if (col.startswith("surface_") or
        col.startswith("round_") or
        col.startswith("tourney_level_name_")):
        feature_cols.append(col)

df_model = df_model.dropna(subset=feature_cols + ["upset"])

X = df_model[feature_cols]
y = df_model["upset"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

model = LogisticRegression(
    random_state=42,
    max_iter=1000,
    class_weight="balanced"
)
model.fit(X_train, y_train)

print("\nModel performance on test set:")
print(classification_report(y_test, model.predict(X_test)))

coefficients = pd.DataFrame({
    "feature":     feature_cols,
    "coefficient": model.coef_[0]
}).sort_values("coefficient", ascending=False)

print("\nModel coefficients:")
print(coefficients)
coefficients.to_csv(
    os.path.join(OUTPUT_DIR, "model_coefficients.csv"), index=False
)

print("\nAnalysis complete!")
