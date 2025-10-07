# IPL 2025 Auction Analysis Dashboard

## Links
- [Live Dashboard](ipl-2025-auction-analysis-flame.vercel.app/)
---

## Overview
This Power BI project analyzes the **IPL 2025 Auction** data, providing key insights into player acquisitions, spending patterns, and team compositions. The interactive dashboard enables users to explore player statistics, team strategies, and auction outcomes.

---

## Problem Statement
The IPL 2025 Auction involves acquiring and managing players across multiple teams based on their performance, type, and base price. Analyzing this auction data helps stakeholders:
1. Understand team-wise spending patterns and strategies.
2. Compare retained versus auctioned players.
3. Identify trends in unsold players.
4. Evaluate the distribution of player types across teams.

This dashboard is designed to provide actionable insights into the auction process, helping teams, analysts, and fans understand the dynamics of the IPL auction.

---

## Source of Data
- **Source**: [IPL 2025 Mega Auction Dataset on Kaggle](https://www.kaggle.com/datasets/souviksamanta1053/ipl-2025-mega-auction-dataset)
- **Dataset Format**: CSV file containing details of players, teams, types, base prices and sold prices
- **Key Fields**:
  - `Players`: Player name.
  - `Team`: Team the player belongs to.
  - `Type`: Player type (e.g., BAT, BOWL, AR).
  - `Base`: Base price of the player.
  - `Sold`: Final sold price during the auction.

---

## Dashboard Preview
<img src="https://github.com/rashmeet03/IPL-2025-Auction-Analysis/blob/main/logo/Dashboard.png" alt="Dashboard Preview" width="600">



---

## Features

### Visualizations
1. **Key Metrics**:
   - **Total Retained Players**: Total number of players retained across all teams.
   - **Total Players Bought in Auction**: Number of players acquired through the auction process.
   - **Total Amount Spent**: Total spending by all teams.
   - **Player Distribution**: Counts of batsmen, bowlers, and all-rounders displayed in one card.

2. **Charts**:
   - **Player Type Distribution**: Pie chart showing proportions of Batsmen, Bowlers, and All-Rounders.
   - **Team Spending Comparison**: Clustered bar chart comparing spending across teams.
   - **Sold vs Unsold Players**: Bar chart categorizing sold and unsold players.
   - **Top 5 Most Expensive Players**: Highlighting the top 5 players by sold price.

3. **Interactive Slicers**:
   - Filter data by **Team**, **Type**, and **Sold/Unsold** status.

4. **Clear Filters Button**:
   - Reset all slicers and filters to the default state with one click.

---

## DAX Measures
Here are all the DAX measures used in this project:

```DAX
TotalRetainedPlayers =
COUNTROWS(
    FILTER(YourTable, [Retained_or_Auctioned] = "Retained")
)
```
```DAX
TotalAuctionedPlayers =
COUNTROWS(
    FILTER(YourTable, [Retained_or_Auctioned] = "Auctioned")
)
```
```DAX
TotalAmountSpent = SUM(YourTable[Sold])
```

## Contact

For any questions or suggestions, feel free to reach out:

- **Name**: Rashmeet Singh
- **Email**: rashu.25103@gmail.com
- **LinkedIn**: [Click here](https://www.linkedin.com/in/rashmeet-singh-763a06207/)
