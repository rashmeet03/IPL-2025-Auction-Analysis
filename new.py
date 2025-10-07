import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder

# Load Data
df = pd.read_csv("ipl_2025_auction_players.csv")

# Preprocessing
df['Base'] = pd.to_numeric(df['Base'], errors='coerce')
df['Sold'] = pd.to_numeric(df['Sold'], errors='coerce').fillna(0)

# Define Player Status
def player_status(row):
    if pd.isna(row['Base']):
        return "Retained"
    elif row['Sold'] == 0:
        return "Unsold"
    else:
        return "Sold"

df['Sold_Status'] = df.apply(player_status, axis=1)
df['Auction_Status'] = df.apply(lambda x: "Retained" if pd.isna(x['Base']) else "Auctioned", axis=1)

# Remove "-" from Team and ensure total teams are 10
df = df[df['Team'] != "-"]

# Exclude TBA players
df = df[df['Players'] != "TBA"]

# Dashboard Layout
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: orange;'>IPL 2025 Auction Analysis</h1>", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.image("logo/ipl_logo.png", use_column_width=True)
st.sidebar.markdown("### Filters")

# Conditionally show filters based on selections
auctioned_retained = st.sidebar.selectbox("Auctioned or Retained", options=["All", "Auctioned", "Retained"])
if auctioned_retained == "Retained":
    sold_unsold = "All"
    selected_team = st.sidebar.selectbox("Team", options=["All"] + sorted(df['Team'].unique().tolist()))
elif auctioned_retained == "Auctioned":
    sold_unsold = st.sidebar.selectbox("Sold or Unsold", options=["All", "Sold", "Unsold"])
    if sold_unsold != "Unsold":
        selected_team = st.sidebar.selectbox("Team", options=["All"] + sorted(df['Team'].unique().tolist()))
    else:
        selected_team = "All"
else:
    sold_unsold = st.sidebar.selectbox("Sold or Unsold", options=["All", "Sold", "Unsold"])
    selected_team = st.sidebar.selectbox("Team", options=["All"] + sorted(df['Team'].unique().tolist()))

player_type = st.sidebar.selectbox("Type", options=["All"] + df['Type'].unique().tolist())

if st.sidebar.button("Clear"):
    selected_team, auctioned_retained, player_type, sold_unsold = "All", "All", "All", "All"

# Filter Data
filtered_data = df.copy()
if selected_team != "All":
    filtered_data = filtered_data[filtered_data['Team'] == selected_team]
if auctioned_retained == "Auctioned":
    filtered_data = filtered_data[filtered_data['Auction_Status'] == "Auctioned"]
elif auctioned_retained == "Retained":
    filtered_data = filtered_data[filtered_data['Auction_Status'] == "Retained"]
if player_type != "All":
    filtered_data = filtered_data[filtered_data['Type'] == player_type]
if sold_unsold == "Sold":
    filtered_data = filtered_data[filtered_data['Sold_Status'] == "Sold"]
elif sold_unsold == "Unsold":
    filtered_data = filtered_data[filtered_data['Sold_Status'] == "Unsold"]

# Ensure filtered_data isn't empty
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
else:
    # Metrics
    total_players = len(df)
    retained_players_count = len(df[df['Auction_Status'] == "Retained"])
    auctioned_players = len(df[df['Auction_Status'] == "Auctioned"])
    sold_players = len(df[df['Sold_Status'] == "Sold"])
    total_spent = df['Sold'].sum()
    highest_bid = df['Sold'].max()
    highest_bid_player = df[df['Sold'] == highest_bid]['Players'].values[0] if highest_bid > 0 else "N/A"

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Players", total_players)
    col2.metric("Retained Players", retained_players_count)
    col3.metric("Auctioned Players", auctioned_players)
    col4.metric("Total Sold Players", sold_players)
    col5.metric("Total Amount Spent (Crores)", f"{total_spent:.2f}")
    col6.metric("Highest Bid (Cr)", f"{highest_bid:.2f}", highest_bid_player)

    # Graphs and Table
    col1, col2 = st.columns([2, 1])
    with col1:
        # Players Count Bar Graph
        if player_type == "All":
            type_counts = filtered_data.groupby(['Type', 'Sold_Status']).size().unstack(fill_value=0).reset_index()
            if "Sold" not in type_counts.columns:
                type_counts["Sold"] = 0
            if "Unsold" not in type_counts.columns:
                type_counts["Unsold"] = 0
            if not type_counts.empty:
                fig = px.bar(type_counts, x="Type", y=["Sold", "Unsold"], barmode="group", title="Players Count")
                st.plotly_chart(fig, use_container_width=True)

        # Team-wise Spending Graph
        team_spending = filtered_data.groupby('Team')['Sold'].sum().reset_index()
        team_spending = team_spending.sort_values(by='Sold', ascending=False)
        if not team_spending.empty:
            team_spending_chart = px.bar(team_spending, x='Team', y='Sold', title="Team-wise Spending", labels={"Sold": "Amount Spent (Cr)"})
            st.plotly_chart(team_spending_chart, use_container_width=True)

        # Player Type Distribution Pie Chart (only for All types)
        if player_type == "All":
            type_distribution = filtered_data['Type'].value_counts()
            if not type_distribution.empty:
                pie_chart = px.pie(type_distribution, values=type_distribution.values, names=type_distribution.index, title="Players per Category", labels={"values": "Count"})
                st.plotly_chart(pie_chart, use_container_width=True)

        # Base Price of Players Pie Chart
        auctioned_data = filtered_data[filtered_data['Auction_Status'] == "Auctioned"]
        if not auctioned_data.empty:
            base_price_distribution = auctioned_data['Base'].value_counts()
            if not base_price_distribution.empty():
                base_pie_chart = px.pie(base_price_distribution, values=base_price_distribution.values, names=base_price_distribution.index, title="Base Price of Players", labels={"values": "Players"})
                st.plotly_chart(base_pie_chart, use_container_width=True)

    with col2:
        # Table
        st.markdown("### Player Details")
        gb = GridOptionsBuilder.from_dataframe(filtered_data[['Players', 'Team', 'Type', 'Base', 'Sold']])
        gb.configure_pagination(enabled=True, paginationPageSize=10)
        gb.configure_column("Base", headerName="Base Price (Cr)")
        gb.configure_column("Sold", headerName="Sold Price (Cr)")
        grid_options = gb.build()
        AgGrid(filtered_data[['Players', 'Team', 'Type', 'Base', 'Sold']], gridOptions=grid_options, height=400, theme='alpine')

    # Top Players Table
    st.markdown("### Top Players")
    top_players = filtered_data.sort_values(by="Sold", ascending=False).head(5)
    if not top_players.empty:
        st.table(top_players[['Players', 'Team', 'Type', 'Sold']].style.format({"Sold": "₹{:.2f} crore"}))

    # Total Purse Spent vs Base Price
    if not filtered_data['Base'].nunique() < 2:
        st.markdown("### Total Purse Spent vs Base Price")
        base_price_vs_spent = filtered_data.groupby('Base')['Sold'].sum().reset_index()
        if not base_price_vs_spent.empty:
            line_chart = px.line(base_price_vs_spent, x='Base', y='Sold', title="Total Purse Spent vs Base Price", labels={"Base": "Base Price", "Sold": "Sold Price Sum"})
            st.plotly_chart(line_chart, use_container_width=True)
