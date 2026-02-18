import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
INPUT     = os.path.join(BASE_DIR, "data", "defence_per_long.csv")
OUTPUT    = os.path.join(BASE_DIR, "data", "defence_analysis.csv")

# ── 1. Load cleaned data ───────────────────────────────────────────────────────
df = pd.read_csv(INPUT)

# ── 2. Year-over-year change ───────────────────────────────────────────────────
df = df.sort_values(["Country", "Year"])
df["YoY_Change"] = df.groupby("Country")["Pct_GDP"].diff().round(3)

# ── 3. Annual ranking (1 = highest spender that year) ─────────────────────────
df["Annual_Rank"] = df.groupby("Year")["Pct_GDP"].rank(ascending=False).astype(int)

# ── 4. NATO 2% target flag ────────────────────────────────────────────────────
df["Meets_2pct_Target"] = df["Pct_GDP"] >= 2.0

# ── 5. Summary table per country ──────────────────────────────────────────────
summary = df.groupby("Country").agg(
    Latest_Year      = ("Year",            "max"),
    Latest_Pct_GDP   = ("Pct_GDP",         "last"),
    Average_Pct_GDP  = ("Pct_GDP",         "mean"),
    Max_Pct_GDP      = ("Pct_GDP",         "max"),
    Min_Pct_GDP      = ("Pct_GDP",         "min"),
    Years_Met_Target = ("Meets_2pct_Target","sum"),
    Total_Years      = ("Year",            "count"),
).round(3).reset_index()

summary["Pct_Years_Met_Target"] = (
    summary["Years_Met_Target"] / summary["Total_Years"] * 100
).round(1)

# ── 6. Biggest movers (2014 → 2024) ───────────────────────────────────────────
first_last = df.groupby("Country").agg(
    Start_Pct = ("Pct_GDP", "first"),
    End_Pct   = ("Pct_GDP", "last")
).reset_index()
first_last["Total_Change"] = (first_last["End_Pct"] - first_last["Start_Pct"]).round(3)
first_last = first_last.sort_values("Total_Change", ascending=False)

# ── 7. Print key insights ──────────────────────────────────────────────────────
print("\n── 2024 Rankings (Top 10) ───────────────────────────────")
top10 = df[df["Year"] == df["Year"].max()].sort_values("Pct_GDP", ascending=False).head(10)
print(top10[["Country", "Pct_GDP", "Annual_Rank"]].to_string(index=False))

print("\n── Countries Meeting 2% Target in 2024 ─────────────────")
meeting = df[(df["Year"] == df["Year"].max()) & (df["Meets_2pct_Target"])]
print(meeting[["Country", "Pct_GDP"]].to_string(index=False))

print("\n── Biggest Movers 2014–2024 ─────────────────────────────")
print(first_last[["Country", "Start_Pct", "End_Pct", "Total_Change"]].head(10).to_string(index=False))

print("\n── Biggest Decliners 2014–2024 ──────────────────────────")
print(first_last[["Country", "Start_Pct", "End_Pct", "Total_Change"]].tail(10).to_string(index=False))

# ── 8. Save ────────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT, index=False)
print(f"\n✓ Saved analysis to: {OUTPUT}")