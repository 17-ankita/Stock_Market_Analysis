import pandas as pd
import numpy as np

df = pd.read_csv("stock_market_analysis.csv")

print("=" * 70)
print("STOCK MARKET ANALYSIS REPORT")
print("=" * 70)

print("\nDataset Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

# ---------------- BASIC KPIs ----------------
total_companies = len(df)
total_industries = df["Industry"].nunique()
total_regions = df["Headquarters"].nunique()
avg_market_cap = df["Market_Capital"].mean()
avg_roce = df["ROCE"].mean()
avg_profit = df["Profit_Percent"].mean()
avg_website_score = df["Website_Design_Score"].mean()

print("\n" + "=" * 70)
print("KEY PERFORMANCE INDICATORS")
print("=" * 70)

print(f"Total Companies              : {total_companies}")
print(f"Total Industries             : {total_industries}")
print(f"Total Regions                : {total_regions}")
print(f"Average Market Capital       : ₹{avg_market_cap:,.2f} Cr")
print(f"Average ROCE                 : {avg_roce:.2f}%")
print(f"Average Profit %             : {avg_profit:.2f}%")
print(f"Average Website Design Score : {avg_website_score:.2f}")

# ---------------- INDUSTRY ANALYSIS ----------------
print("\n" + "=" * 70)
print("INDUSTRY-WISE MARKET LANDSCAPE")
print("=" * 70)

industry = (
    df.groupby("Industry")
    .agg(
        Companies=("Company", "count"),
        Total_Market_Capital=("Market_Capital", "sum"),
        Avg_Market_Capital=("Market_Capital", "mean"),
        Avg_ROCE=("ROCE", "mean"),
        Avg_Profit=("Profit_Percent", "mean"),
        Avg_Website_Score=("Website_Design_Score", "mean")
    )
    .reset_index()
    .sort_values("Companies", ascending=False)
)

industry = industry.round(2)
print(industry.to_string(index=False))

# ---------------- CLIENT POTENTIAL ----------------
print("\n" + "=" * 70)
print("CLIENT POTENTIAL ANALYSIS")
print("=" * 70)

client_potential = df[
    ["Company", "Industry", "Headquarters", "Market_Capital", "ROCE", "Profit_Percent"]
].sort_values(["ROCE", "Profit_Percent"], ascending=False)

print(client_potential.head(15).to_string(index=False))

# ---------------- REGIONAL ANALYSIS ----------------
print("\n" + "=" * 70)
print("REGIONAL OPPORTUNITIES")
print("=" * 70)

region = (
    df.groupby("Headquarters")
    .agg(
        Companies=("Company", "count"),
        Avg_Market_Capital=("Market_Capital", "mean"),
        Total_Market_Capital=("Market_Capital", "sum"),
        Avg_ROCE=("ROCE", "mean"),
        Avg_Profit=("Profit_Percent", "mean")
    )
    .reset_index()
    .sort_values("Companies", ascending=False)
)

region = region.round(2)
print(region.to_string(index=False))

# ---------------- WEBSITE QUALITY ----------------
print("\n" + "=" * 70)
print("WEBSITE QUALITY ASSESSMENT")
print("=" * 70)

website_quality = (
    df.groupby("Website_Design_Type")
    .agg(
        Companies=("Company", "count"),
        Avg_Website_Score=("Website_Design_Score", "mean"),
        Avg_UX_Score=("UX_Score", "mean"),
        Avg_Performance=("Performance_Score", "mean"),
        Total_Design_Issues=("Design_Issues", "sum")
    )
    .reset_index()
    .sort_values("Avg_Website_Score", ascending=False)
)

website_quality = website_quality.round(2)
print(website_quality.to_string(index=False))

# ---------------- UX VS PERFORMANCE ----------------
print("\n" + "=" * 70)
print("UX VS PERFORMANCE ANALYSIS")
print("=" * 70)

ux_corr = df["UX_Score"].corr(df["Performance_Score"])
design_corr = df["Website_Design_Score"].corr(df["Performance_Score"])

print(f"Correlation between UX Score and Performance Score: {ux_corr:.3f}")
print(f"Correlation between Website Design Score and Performance Score: {design_corr:.3f}")

# ---------------- PROBLEM IDENTIFICATION ----------------
print("\n" + "=" * 70)
print("PROBLEM IDENTIFICATION")
print("=" * 70)

low_website = df[df["Website_Design_Score"] < 70]
high_issues = df[df["Design_Issues"] > df["Design_Issues"].mean()]
low_performance = df[df["Performance_Score"] < 70]

print(f"Companies with website score below 70: {len(low_website)}")
print(f"Companies with above-average design issues: {len(high_issues)}")
print(f"Companies with performance score below 70: {len(low_performance)}")

# ---------------- OPPORTUNITY MAPPING ----------------
print("\n" + "=" * 70)
print("OPPORTUNITY FOR INMOGIC TECHNOLOGIES")
print("=" * 70)

opportunities = df[
    (df["Website_Design_Score"] < 70) |
    (df["Performance_Score"] < 70) |
    (df["Design_Issues"] > df["Design_Issues"].mean())
][
    ["Company", "Industry", "Headquarters", "Website_Design_Score", "Performance_Score", "Design_Issues"]
].sort_values(["Website_Design_Score", "Performance_Score"])

print(opportunities.head(20).to_string(index=False))

print("\n" + "=" * 70)
print("KEY INSIGHTS SUMMARY")
print("=" * 70)

print("""
1. Industry-wise analysis helps identify dominant sectors such as Manufacturing, IT, and Financial Services.
2. ROCE and Profit % help find financially strong companies for premium client targeting.
3. Regional analysis highlights cities with high company concentration and market potential.
4. Website design score reveals companies with weak digital presence.
5. UX and performance analysis supports data-driven website improvement proposals.
6. Companies with low website score and high design issues are strong prospects for Inmogic Technologies.
""")