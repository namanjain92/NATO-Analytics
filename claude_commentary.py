import os
import pandas as pd
import anthropic
from dotenv import load_dotenv

# ── Load API key ───────────────────────────────────────────────────────────────
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT    = os.path.join(BASE_DIR, "data", "defence_analysis.csv")
OUTPUT   = os.path.join(BASE_DIR, "data", "country_commentaries.csv")

# ── Load analysis data ─────────────────────────────────────────────────────────
df = pd.read_csv(INPUT)

# ── Filter out the NATO Total row (not a country) ─────────────────────────────
countries_df = df[df["Country"] != "NATO Total"].copy()

# ── Get 2024 snapshot per country ─────────────────────────────────────────────
latest_year = countries_df["Year"].max()
latest      = countries_df[countries_df["Year"] == latest_year].copy()

# ── Get 2014 starting values ───────────────────────────────────────────────────
earliest_year = countries_df["Year"].min()
earliest      = countries_df[countries_df["Year"] == earliest_year][["Country", "Pct_GDP"]].rename(
    columns={"Pct_GDP": "Start_Pct"}
)

# ── Merge ──────────────────────────────────────────────────────────────────────
snapshot = latest.merge(earliest, on="Country")
snapshot["Total_Change"] = (snapshot["Pct_GDP"] - snapshot["Start_Pct"]).round(3)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a senior policy analyst writing country briefs for a NATO defence expenditure report.
Your tone is informed, professional, and appreciative of the collective security commitments 
made by Alliance members. Highlight the significance of defence investments for global peace 
and stability. Acknowledge the efforts of countries meeting or trending toward the 2% GDP target.
Be concise — each brief should be 3–4 sentences maximum.
"""

# ── Function to generate commentary for one country ───────────────────────────
def generate_commentary(row):
    meets_target = "meets" if row["Pct_GDP"] >= 2.0 else "does not yet meet"
    direction    = "increase" if row["Total_Change"] >= 0 else "decrease"

    prompt = f"""
Country: {row['Country']}
2024 Defence Spending: {row['Pct_GDP']:.2f}% of GDP
2014 Defence Spending: {row['Start_Pct']:.2f}% of GDP
Total change since 2014: {abs(row['Total_Change']):.2f}% {direction}
2024 Alliance Rank: #{int(row['Annual_Rank'])} out of 32 member countries
NATO 2% Target: This country {meets_target} the target in 2024

Write a 3-4 sentence brief on this country's defence spending trajectory and what it 
signals about their commitment to the Alliance.
"""
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# ── Generate commentaries for all countries ────────────────────────────────────
print(f"Generating commentaries for {len(snapshot)} countries...\n")

commentaries = []
for _, row in snapshot.iterrows():
    print(f"  Processing: {row['Country']}...")
    commentary = generate_commentary(row)
    commentaries.append({
        "Country":     row["Country"],
        "Pct_GDP":     row["Pct_GDP"],
        "Annual_Rank": row["Annual_Rank"],
        "Start_Pct":   row["Start_Pct"],
        "Total_Change": row["Total_Change"],
        "Meets_Target": row["Pct_GDP"] >= 2.0,
        "Commentary":  commentary
    })
    print(f"  ✓ Done\n")

# ── Save ───────────────────────────────────────────────────────────────────────
output_df = pd.DataFrame(commentaries)
output_df.to_csv(OUTPUT, index=False)
print(f"✓ All commentaries saved to: {OUTPUT}")