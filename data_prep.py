import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA = os.path.join(BASE_DIR, "data", "defence_per.csv")
OUTPUT    = os.path.join(BASE_DIR, "data", "defence_per_long.csv")

# ── 1. Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv(RAW_DATA, encoding="latin1")
print(f"Loaded {df.shape[0]} countries × {df.shape[1] - 1} years")

# ── 2. Reshape to long format ──────────────────────────────────────────────────
df_long = df.melt(
    id_vars=["Country"],
    var_name="Year",
    value_name="Pct_GDP"
)

# ── 3. Clean Year column (handles "2024e" style estimates) ─────────────────────
df_long["Year"] = df_long["Year"].str.replace("e", "", regex=False).astype(int)

# ── 4. Clean Percentage column ─────────────────────────────────────────────────
# Convert to numeric, coerce any non-numeric entries (like ":") to NaN
df_long["Pct_GDP"] = pd.to_numeric(df_long["Pct_GDP"], errors="coerce")

# ── 5. Sort ────────────────────────────────────────────────────────────────────
df_long = df_long.sort_values(["Country", "Year"]).reset_index(drop=True)

# ── 6. Validation report ───────────────────────────────────────────────────────
print("\n── Data Validation ──────────────────────────────────────")
print(f"Countries : {df_long['Country'].nunique()}")
print(f"Year range: {df_long['Year'].min()} – {df_long['Year'].max()}")
print(f"Missing values (Pct_GDP): {df_long['Pct_GDP'].isna().sum()}")
print(f"Value range: {df_long['Pct_GDP'].min():.2f}% – {df_long['Pct_GDP'].max():.2f}%")

# Flag any suspiciously high or low values
outliers = df_long[df_long["Pct_GDP"] > 5]
if not outliers.empty:
    print(f"\n⚠ Possible outliers (>5% GDP):")
    print(outliers)

# ── 7. Save ────────────────────────────────────────────────────────────────────
df_long.to_csv(OUTPUT, index=False)
print(f"\n✓ Saved cleaned data to: {OUTPUT}")