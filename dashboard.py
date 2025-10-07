import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Load Data
df = pd.read_csv("ipl_2025_auction_players.csv")

# Preprocessing
df['Base'] = pd.to_numeric(df['Base'], errors='coerce')
df['Sold'] = pd.to_numeric(df['Sold'], errors='coerce').fillna(0)
retained_players = df[df['Base'].isnull()]
df['Players'] = df.apply(lambda x: f"{x['Players']} (R)" if pd.isnull(x['Base']) else x['Players'], axis=1)
df['Team'] = df['Team'].replace('-', 'Unsold Players')
auction_players = df[~df['Base'].isnull()]

# Sidebar Filters
st.sidebar.title("Filters")
selected_team = st.sidebar.selectbox("Select Team", options=["All"] + sorted(df['Team'].unique().tolist()))

# Team Logos
def display_team_logo(team_name):
    team_logos = {
        "Chennai Super Kings": "logo/csk_logo.png",
        "Mumbai Indians": "logo/mi_logo.png",
        "Royal Challengers Bangalore": "logo/rcb_logo.png",
        "Kolkata Knight Riders": "logo/kkr_logo.png",
        "Rajasthan Royals": "logo/rr_logo.png",
        "Punjab Kings": "logo/pbks_logo.png",
        "Delhi Capitals": "logo/dc_logo.png",
        "Sunrisers Hyderabad": "logo/srh_logo.png",
        "Lucknow Super Giants": "logo/lsg_logo.png",
        "Gujarat Titans": "logo/gt_logo.png",
        "Unsold Players": None
    }
    logo_path = team_logos.get(team_name)
    if logo_path:
        full_path = os.path.join(os.getcwd(), logo_path)
        if os.path.exists(full_path):
            st.image(full_path, width=150, caption=team_name)

# Filtered Data
filtered_data = df[df['Team'] == selected_team] if selected_team != "All" else df

# Team Specific Analysis
if selected_team != "All":
    st.markdown(f"### {selected_team} Analysis")
    display_team_logo(selected_team)

    team_data = filtered_data[filtered_data['Team'] == selected_team]

    if selected_team == "Unsold Players":
        st.markdown("#### Unsold Players")
        unsold_data = team_data[['Players', 'Base']].sort_values(by='Base', ascending=False)
        st.table(unsold_data.style.format({"Base": "₹{:.2f} crore"}).background_gradient(cmap="Oranges", subset="Base"))
    else:
        st.markdown("#### Team Insights")
        action = st.radio("Choose an option to display", options=["Squad", "Analysis", "Highlights"], horizontal=True)

        if action == "Squad":

            st.markdown("#### Squad Details")
             # Squad Breakdown
            batsmen_data = team_data[team_data['Type'] == 'BAT'][['Players', 'Sold']].sort_values(by='Sold', ascending=False)
            allrounders_data = team_data[team_data['Type'] == 'AR'][['Players', 'Sold']].sort_values(by='Sold', ascending=False)
            bowlers_data = team_data[team_data['Type'] == 'BOWL'][['Players', 'Sold']].sort_values(by='Sold', ascending=False)

            tabs = st.tabs(["Batsmen", "All-Rounders", "Bowlers"])
            with tabs[0]:
                st.table(batsmen_data.style.format({"Sold": "₹{:.2f} crore"}).background_gradient(cmap="YlGn", subset="Sold"))
            with tabs[1]:
                st.table(allrounders_data.style.format({"Sold": "₹{:.2f} crore"}).background_gradient(cmap="YlOrRd", subset="Sold"))
            with tabs[2]:
                st.table(bowlers_data.style.format({"Sold": "₹{:.2f} crore"}).background_gradient(cmap="Blues", subset="Sold"))
            # Select Playing XI with Checkboxes
            st.markdown("### Select Your Playing XI")
            squad = team_data['Players'].tolist()
            selected_players = []

            for player in squad:
                if st.checkbox(player, key=player):
                    selected_players.append(player)

            if len(selected_players) > 11:
                st.error("You can select a maximum of 11 players!")
            else:
                st.markdown("### Your Selected Playing XI")
                st.table(pd.DataFrame({"Playing XI": selected_players}))

           

        elif action == "Analysis":
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Spending Distribution")
                spending_by_type = team_data.groupby('Type')['Sold'].sum()
                st.plotly_chart(px.pie(spending_by_type, values=spending_by_type.values, names=spending_by_type.index,
                                       title="Spending by Player Type", custom_data=[spending_by_type.values],
                                       labels={'values': 'Total Value'}).update_traces(textinfo='value+label',
                                       texttemplate='%{label}: %{value} cr',
                                       hovertemplate='<b>%{label}</b><br>Total Value: %{value} cr'),
                               use_container_width=True)

                st.markdown("#### Player Type Counts")
                type_counts = team_data['Type'].value_counts()
                st.plotly_chart(px.bar(type_counts, x=type_counts.index, y=type_counts.values,
                                       title="Player Type Counts",
                                       labels={"x": "Player Type", "y": "Count"}),
                               use_container_width=True)

            with col2:
                st.markdown("#### Top Spending Players")
                top_players = team_data.sort_values(by="Sold", ascending=False).head(5)
                st.plotly_chart(px.bar(top_players, x="Players", y="Sold",
                                       title="Top 5 Players by Spending",
                                       labels={"Sold": "Money Spent (₹ crore)", "Players": "Player"},
                                       color="Type", hover_data=["Type"]),
                               use_container_width=True)

                st.markdown("#### Auction Spending Trends")
                spending_trends = team_data.groupby('Type')['Sold'].sum().reset_index()
                st.plotly_chart(px.line(spending_trends, x='Type', y='Sold',
                                        title="Spending Trends by Player Type",
                                        labels={"Sold": "Money Spent (₹ crore)", "Type": "Player Type"}),
                               use_container_width=True)

        elif action == "Highlights":
            st.markdown("#### Top Highlights")
            st.markdown("**Top 5 Expensive Players**")
            top_players = team_data.sort_values(by="Sold", ascending=False).head(5)
            st.table(top_players[['Players', 'Sold']].style.format({"Sold": "₹{:.2f} crore"}).background_gradient(cmap="YlOrBr", subset="Sold"))

            st.markdown("**Retained Players**")
            retained = retained_players[retained_players['Team'] == selected_team][['Players', 'Sold']]
            st.table(retained.style.format({"Sold": "₹{:.2f} crore"}).background_gradient(cmap="Purples", subset="Sold"))

else:
    st.markdown("### Overall Auction Analysis")

    # Retentions Section
    st.markdown("## I. Retentions")

    # Number of Players Retained and Purse Spent
    retention_summary = retained_players.groupby('Team').agg(
        retained_count=('Players', 'count'),
        purse_spent=('Sold', 'sum')
    ).reset_index()
    st.markdown("### Retention Summary")
    st.table(retention_summary.style.format({"purse_spent": "₹{:.2f} crore"}))

    # Slots Left and Purse Left
    total_slots = 25
    purse_limit = 120
    retention_summary['slots_left'] = total_slots - retention_summary['retained_count']
    retention_summary['purse_left'] = purse_limit - retention_summary['purse_spent']
    st.markdown("### Slots and Purse Left")
    st.table(retention_summary[['Team', 'slots_left', 'purse_left']].style.format({"purse_left": "₹{:.2f} crore"}))

    # Total Spending Graph on Retained Players
    st.markdown("### Total Spending on Retained Players")
    st.plotly_chart(px.bar(retention_summary, x='Team', y='purse_spent',
                           title="Total Spending on Retentions",
                           labels={"purse_spent": "Money Spent (₹ crore)", "Team": "Team"}))

    # Top 5 Expensive Retentions
    top_retained = retained_players.sort_values(by='Sold', ascending=False).head(5)
    st.markdown("### Top 5 Expensive Retentions")
    st.table(top_retained[['Players', 'Team', 'Sold']].style.format({"Sold": "₹{:.2f} crore"}))

    # Retained Players of Each Team
    st.markdown("### Retained Players by Team")
    for team in sorted(retained_players['Team'].unique()):
        team_retained = retained_players[retained_players['Team'] == team][['Players', 'Sold']]
        st.markdown(f"#### {team}")
        st.table(team_retained.style.format({"Sold": "₹{:.2f} crore"}))
