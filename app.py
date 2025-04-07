import streamlit as st
import pandas as pd
from filters import filter_games, calculate_summary
from utils import export_filtered_df, plot_win_pct_distribution, plot_streak_distribution

# Load dataset
st.title("⚾ MLB Team Game Finder (2024 Enriched with Betting Data)")
data_file = "MLB_2024_Game_Data_FINAL_WORKSHEET.csv"
df = pd.read_csv(data_file)

# Fix and standardize column names
df['date'] = pd.to_datetime(df['date_x'])
df.rename(columns={'date_x': 'date', 'team_x': 'team'}, inplace=True)

# Sidebar filters
st.sidebar.header("🔎 Search Filters")
st.sidebar.subheader("📅 Game Filters")

team = st.sidebar.text_input("Team (abbreviation)", help="Use team abbreviations like LAD, NYY, BOS")
home_away = st.sidebar.selectbox("Home or Away", ["All", "home", "away"])
if home_away == "All":
    home_away = None

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Performance Filters")

min_win_pct = st.sidebar.slider("Min Win %", 0.0, 1.0, 0.0, 0.01)
max_win_pct = st.sidebar.slider("Max Win %", 0.0, 1.0, 1.0, 0.01)

min_win_streak = st.sidebar.number_input("Min Win Streak", min_value=0, value=0)
min_loss_streak = st.sidebar.number_input("Min Loss Streak", min_value=0, value=0)

# 🆕 Betting-related filter
favorite_filter = st.sidebar.selectbox("Favorite Status", ["All", "Favorite", "Underdog"])

# Search + Reset button logic
filtered_df = pd.DataFrame()
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Search"):
        st.session_state.search_clicked = True
with col2:
    if st.button("Reset"):
        st.session_state.search_clicked = False

# Default message before searching
if not st.session_state.search_clicked:
    st.markdown("### 👋 Welcome!")
    st.info("Use the filters in the sidebar to explore 2024 MLB game data enriched with betting insights. Click **Search** to begin.")

# Run query and apply filters
if st.session_state.search_clicked:
    filtered_df = filter_games(
        df,
        team=team,
        home_away=home_away,
        min_win_pct=min_win_pct,
        max_win_pct=max_win_pct,
        min_win_streak=min_win_streak,
        min_loss_streak=min_loss_streak,
        season=None
    )

    # Apply betting status filter
    if favorite_filter == "Favorite":
        filtered_df = filtered_df[filtered_df["was_favorite"] == True]
    elif favorite_filter == "Underdog":
        filtered_df = filtered_df[filtered_df["was_favorite"] == False]

    if filtered_df.empty:
        st.warning("No results found. Try adjusting your filters.")
   Script execution error
File "/mount/src/mlb-betting-tool/app.py", line 75
     else:
          ^
IndentationError: unindent does not match any outer indentation level
