import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Stock Market Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
    color: #f8fafc;
}
section[data-testid="stSidebar"] {
    background: #020617;
}
h1 {
    color: #38bdf8 !important;
    font-weight: 800 !important;
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    border: 1px solid rgba(56,189,248,0.25);
    padding: 18px;
    border-radius: 18px;
}
button[data-baseweb="tab"] {
    background: #1e293b !important;
    color: white !important;
    border-radius: 12px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #0284c7, #38bdf8) !important;
}
</style>
""", unsafe_allow_html=True)


def apply_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=20, color="white")
    )
    return fig


@st.cache_data
def load_data():
    df = pd.read_excel("stock_market_analysis.xlsx")

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("/", "_")
        .str.replace("%", "Percent")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    rename_map = {
        "Company_Name": "Company",
        "Name": "Company",
        "Industry_Type": "Industry",
        "Sector": "Industry",
        "Headquarter": "Headquarters",
        "Location": "Headquarters",
        "Market_Cap": "Market_Capital",
        "Market_Capital_Cr": "Market_Capital",
        "Market_Capital_Crore": "Market_Capital",
        "Profit_Percent_": "Profit_Percent",
        "Profit": "Profit_Percent",
        "Average_Profit": "Profit_Percent",
        "Website_Design": "Website_Design_Score",
        "Website_Design_Score_": "Website_Design_Score",
        "Website_Score": "Website_Design_Score",
        "Design_Type": "Website_Design_Type",
        "Website_Type": "Website_Design_Type",
        "Design_Issue": "Design_Issues",
        "Issues": "Design_Issues",
        "UX": "UX_Score",
        "UX_Score_": "UX_Score",
        "Performance": "Performance_Score",
        "Performance_Score_": "Performance_Score"
    }

    df = df.rename(columns=rename_map)

    if "Company" not in df.columns:
        df["Company"] = "Company " + (df.index + 1).astype(str)

    if "Industry" not in df.columns:
        df["Industry"] = "Unknown Industry"

    if "Headquarters" not in df.columns:
        df["Headquarters"] = "Unknown Region"

    if "Market_Capital" not in df.columns:
        df["Market_Capital"] = 0

    if "ROCE" not in df.columns:
        df["ROCE"] = 0

    if "Profit_Percent" not in df.columns:
        df["Profit_Percent"] = 0

    if "Website_Design_Score" not in df.columns:
        df["Website_Design_Score"] = 0

    if "Website_Design_Type" not in df.columns:
        df["Website_Design_Type"] = "Not Available"

    if "Design_Issues" not in df.columns:
        df["Design_Issues"] = 0

    if "UX_Score" not in df.columns:
        df["UX_Score"] = df["Website_Design_Score"]

    if "Performance_Score" not in df.columns:
        df["Performance_Score"] = df["Website_Design_Score"]

    numeric_cols = [
        "Market_Capital",
        "ROCE",
        "Profit_Percent",
        "Website_Design_Score",
        "Design_Issues",
        "UX_Score",
        "Performance_Score"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


df = load_data()

st.sidebar.title("Stock Market Filters")

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    sorted(df["Industry"].dropna().unique()),
    default=sorted(df["Industry"].dropna().unique())
)

region_filter = st.sidebar.multiselect(
    "Select Headquarters",
    sorted(df["Headquarters"].dropna().unique()),
    default=sorted(df["Headquarters"].dropna().unique())
)

design_filter = st.sidebar.multiselect(
    "Select Website Design Type",
    sorted(df["Website_Design_Type"].dropna().unique()),
    default=sorted(df["Website_Design_Type"].dropna().unique())
)

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Headquarters"].isin(region_filter)) &
    (df["Website_Design_Type"].isin(design_filter))
].copy()

st.title("Stock Market Analysis Dashboard")

st.markdown("""
This dashboard analyzes **stock market companies with market capitalization below ₹500 crore**.
It focuses on market landscape, client potential, regional opportunities, website quality,
UX performance, and opportunities for Inmogic Technologies.
""")

total_companies = len(filtered_df)
total_industries = filtered_df["Industry"].nunique()
total_regions = filtered_df["Headquarters"].nunique()
avg_market_cap = filtered_df["Market_Capital"].mean() if total_companies > 0 else 0
avg_roce = filtered_df["ROCE"].mean() if total_companies > 0 else 0
avg_profit = filtered_df["Profit_Percent"].mean() if total_companies > 0 else 0
avg_website = filtered_df["Website_Design_Score"].mean() if total_companies > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Companies", total_companies)
col2.metric("Industries", total_industries)
col3.metric("Regions", total_regions)
col4.metric("Avg Market Cap", f"₹{avg_market_cap:,.1f} Cr")

col5, col6, col7 = st.columns(3)
col5.metric("Avg ROCE", f"{avg_roce:.1f}%")
col6.metric("Avg Profit %", f"{avg_profit:.1f}%")
col7.metric("Avg Website Score", f"{avg_website:.1f}/100")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Market Landscape",
    "Client Potential",
    "Regional Opportunities",
    "Website Quality",
    "Inmogic Opportunities"
])

with tab1:
    st.subheader("Market Landscape")

    col1, col2 = st.columns(2)

    with col1:
        industry_count = filtered_df["Industry"].value_counts().reset_index()
        industry_count.columns = ["Industry", "Companies"]

        fig = px.bar(
            industry_count,
            x="Industry",
            y="Companies",
            title="Company Count by Industry",
            text="Companies",
            color="Industry"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        market_by_industry = (
            filtered_df.groupby("Industry")["Market_Capital"]
            .sum()
            .reset_index()
            .sort_values("Market_Capital", ascending=False)
        )

        fig = px.bar(
            market_by_industry,
            x="Industry",
            y="Market_Capital",
            title="Total Market Capital by Industry",
            text_auto=".1f",
            color="Industry"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

with tab2:
    st.subheader("Client Potential Analysis")

    col1, col2 = st.columns(2)

    with col1:
        top_roce = filtered_df.sort_values("ROCE", ascending=False).head(10)

        fig = px.bar(
            top_roce,
            x="Company",
            y="ROCE",
            title="Top Companies by ROCE",
            text_auto=".1f",
            color="ROCE"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        top_profit = filtered_df.sort_values("Profit_Percent", ascending=False).head(10)

        fig = px.bar(
            top_profit,
            x="Company",
            y="Profit_Percent",
            title="Top Companies by Profit %",
            text_auto=".1f",
            color="Profit_Percent"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    st.markdown("### High Potential Client Scorecard")
    st.dataframe(
        filtered_df[
            ["Company", "Industry", "Headquarters", "Market_Capital", "ROCE", "Profit_Percent"]
        ].sort_values(["ROCE", "Profit_Percent"], ascending=False),
        use_container_width=True
    )

with tab3:
    st.subheader("Regional Opportunities")

    col1, col2 = st.columns(2)

    with col1:
        region_count = filtered_df["Headquarters"].value_counts().reset_index()
        region_count.columns = ["Headquarters", "Companies"]

        fig = px.bar(
            region_count.head(15),
            x="Headquarters",
            y="Companies",
            title="Top Regions by Company Count",
            text="Companies",
            color="Headquarters"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        region_market = (
            filtered_df.groupby("Headquarters")["Market_Capital"]
            .mean()
            .reset_index()
            .sort_values("Market_Capital", ascending=False)
            .head(15)
        )

        fig = px.bar(
            region_market,
            x="Headquarters",
            y="Market_Capital",
            title="Average Market Capital by Headquarters",
            text_auto=".1f",
            color="Market_Capital"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

with tab4:
    st.subheader("Website Quality Assessment")

    col1, col2 = st.columns(2)

    with col1:
        design_score = (
            filtered_df.groupby("Industry")["Website_Design_Score"]
            .mean()
            .reset_index()
            .sort_values("Website_Design_Score", ascending=False)
        )

        fig = px.bar(
            design_score,
            x="Industry",
            y="Website_Design_Score",
            title="Average Website Design Score by Industry",
            text_auto=".1f",
            color="Website_Design_Score"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        design_issues = (
            filtered_df.groupby("Website_Design_Type")["Design_Issues"]
            .sum()
            .reset_index()
            .sort_values("Design_Issues", ascending=False)
        )

        fig = px.bar(
            design_issues,
            x="Website_Design_Type",
            y="Design_Issues",
            title="Website Design Type vs Design Issues",
            text_auto=".0f",
            color="Website_Design_Type"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    fig = px.scatter(
        filtered_df,
        x="UX_Score",
        y="Performance_Score",
        color="Website_Design_Type",
        size="Market_Capital",
        hover_data=["Company", "Industry", "Headquarters"],
        title="UX Score vs Performance Score"
    )
    st.plotly_chart(apply_theme(fig), use_container_width=True)

with tab5:
    st.subheader("Opportunity for Inmogic Technologies")

    opportunity_df = filtered_df[
        (filtered_df["Website_Design_Score"] < 70) |
        (filtered_df["Performance_Score"] < 70) |
        (filtered_df["Design_Issues"] >= filtered_df["Design_Issues"].mean())
    ].copy()

    col1, col2 = st.columns(2)

    with col1:
        opportunity_industry = opportunity_df["Industry"].value_counts().reset_index()
        opportunity_industry.columns = ["Industry", "Potential Clients"]

        fig = px.bar(
            opportunity_industry,
            x="Industry",
            y="Potential Clients",
            title="Potential Clients by Industry",
            text="Potential Clients",
            color="Industry"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        opportunity_region = opportunity_df["Headquarters"].value_counts().reset_index().head(15)
        opportunity_region.columns = ["Headquarters", "Potential Clients"]

        fig = px.bar(
            opportunity_region,
            x="Headquarters",
            y="Potential Clients",
            title="Potential Clients by Region",
            text="Potential Clients",
            color="Headquarters"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    st.markdown("### Potential Inmogic Target Companies")
    st.dataframe(
        opportunity_df[
            ["Company", "Industry", "Headquarters", "Website_Design_Score", "Performance_Score", "Design_Issues"]
        ],
        use_container_width=True
    )

st.divider()

with st.expander("View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

with st.expander("View Detected Column Names"):
    st.write(list(df.columns))