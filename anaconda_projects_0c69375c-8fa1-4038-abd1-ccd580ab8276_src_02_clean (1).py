import pandas as pd
import os

RAW_DIR   = "data/raw/"
CLEAN_DIR = "data/clean/"

os.makedirs(CLEAN_DIR, exist_ok=True)

all_years = []

for year in range(1991, 2025):
    filepath = os.path.join(RAW_DIR, f"atp_matches_{year}.csv")
    try:
        df_year = pd.read_csv(filepath, low_memory=False)
        df_year["year"] = year
        all_years.append(df_year)
        print(f"Loaded {year}: {len(df_year)} matches")
    except FileNotFoundError:
        print(f"Missing: {year}")

df = pd.concat(all_years, ignore_index=True)
print(f"\nTotal matches loaded: {len(df)}")

df = df[df["tourney_level"].isin(["G", "M"])]
print(f"Grand Slam + Masters matches: {len(df)}")

df["tourney_name"] = df["tourney_name"].replace({
    "Us Open": "US Open",
    "Australian Open-": "Australian Open"
})

serve_cols = [
    "w_ace", "w_df", "w_svpt", "w_1stIn", "w_1stWon", "w_2ndWon",
    "w_SvGms", "w_bpSaved", "w_bpFaced",
    "l_ace", "l_df", "l_svpt", "l_1stIn", "l_1stWon", "l_2ndWon",
    "l_SvGms", "l_bpSaved", "l_bpFaced"
]

df = df.dropna(subset=serve_cols + ["winner_rank", "loser_rank"])
print(f"Matches with complete stats: {len(df)}")

df["favourite_rank"] = df[["winner_rank", "loser_rank"]].min(axis=1)
df["underdog_rank"]  = df[["winner_rank", "loser_rank"]].max(axis=1)
df["rank_gap"]       = df["underdog_rank"] - df["favourite_rank"]

df["upset"] = (df["winner_rank"] > df["loser_rank"]).astype(int)

df["tourney_level_name"] = df["tourney_level"].map({
    "G": "Grand Slam",
    "M": "Masters 1000"
})

print(f"\nOverall upset rate: {df['upset'].mean():.1%}")
print(f"Grand Slam upset rate: {df[df['tourney_level']=="G"]['upset'].mean():.1%}")
print(f"Masters upset rate: {df[df['tourney_level']=="M"]['upset'].mean():.1%}")

out_path = os.path.join(CLEAN_DIR, "atp_clean.csv")
df.to_csv(out_path, index=False)
print(f"\nSaved clean data to {out_path}")
print(f"Final dataset: {len(df)} matches, {len(df.columns)} columns")
