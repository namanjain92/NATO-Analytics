# NATO-Analytics

AI-Powered Defence Expenditure Intelligence
An end-to-end data pipeline that analyses NATO member defence expenditures as a percentage of GDP and uses the Claude AI API to generate contextual, expert-level country briefs, turning raw spending data into an intelligence-style report.

# Background

For over seven decades, the North Atlantic Treaty Organization (NATO) has been a cornerstone of international peace and stability. In an increasingly complex global security environment, shared defence investments are critical to maintaining readiness, interoperability, and collective resilience. The Alliance's 2% of GDP benchmark serves as a key indicator of each member's commitment to collective security.
This project goes beyond visualising the numbers. It uses AI to explain what those numbers mean geopolitically, and why they matter for the future of the Alliance.

# What This Project Does

1. Ingests and cleans NATO defence expenditure data (2014-2024) across 32 member countries
2. Analyses year-over-year changes, annual rankings, 2% target compliance, and biggest movers since 2014
3. Integrates the Claude AI API to auto-generate a contextual 3-4 sentence brief for every member country, explaining their spending trajectory, geopolitical context, and Alliance commitment
4. Outputs a structured CSV of AI-generated country commentaries ready for reporting

# How Claude AI Adds Value

Traditional data analysis produces numbers. Claude transforms those numbers into insight.
For each country, the pipeline feeds structured spending data into Claude with a policy-focused system prompt, and receives a professionally written brief in return, something no pandas script can produce on its own. The result reads like analysis from a think tank or defence policy organisation.

# Example output for Poland:

Poland stands as the Alliance's foremost contributor in terms of defence spending as a share of GDP, claiming the top position among all 32 member nations at an exceptional 3.79% in 2024. The remarkable 1.92 percentage point increase since 2014 reflects a sustained and deliberate commitment to national and collective defence, driven in large part by Poland's acute awareness of the evolving security landscape on NATO's eastern flank. By nearly doubling its relative investment over the past decade and exceeding the 2% guideline by a significant margin, Poland sends an unambiguous signal of resolve to allies.

This demonstrates prompt engineering - the system prompt was carefully designed to produce a consistent tone that is professional, informed, and appreciative of member nations' collective security commitments.

# Key Findings (2024)

1. Poland ranks #1 at 3.79% of GDP, up from 1.86% in 2014, illustrating a remarkable growth in defence investment and highlighting its role as one of the Alliance's most committed and resolute contributors to collective security. 
2. 19 of 32 members now meet the 2% target.
3. Latvia, Lithuania, and Estonia have demonstrated the most remarkable growth in defence investment since 2014, reflecting their steadfast commitment to collective security.

# Data Source

NATO official defence expenditure data (2014-2024), published annually at nato.int. Data is updated each year, allowing this pipeline to be rerun annually with minimal changes.

# Tools and Technologies

1. Python (pandas) for data cleaning and analysis
2. Claude API (Anthropic) for AI-generated narrative commentary
3. Power BI for interactive dashboard
4. python-dotenv for secure API key management
