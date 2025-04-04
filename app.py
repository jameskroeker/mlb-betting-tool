import streamlit as st
import pandas as pd
from filters import filter_games, calculate_summary
from utils import export_filtered_df, plot_win_pct_distribution, plot_streak_distribution

# Load dataset
st.title("MLB Team Game Finder (2021–2024)")
data_file = "MLB_Team_Game_Data_2021_2024_RESET.csv"
df = pd.read_csv(data_file)
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.header("Filters")
team = st.sidebar.text_input("Team (abbreviation)")
home_away = st.sidebar.selectbox("Home/Away", ["", "home", "away"])
season_options = sorted(df['season'].dropna().unique())
season = st.sidebar.selectbox("Season", [None] + list(season_options))
min_win_pct = st.sidebar.slider("Min Win %", 0.0, 1.0, 0.5, 0.01)
max_win_pct = st.sidebar.slider("Max Win %", 0.0, 1.0, 1.0, 0.01)
min_win_streak = st.sidebar.slider("Min Win Streak", 0, 20, 0)
min_loss_streak = st.sidebar.slider("Min Loss Streak", 0, 20, 0)

# Apply filters
filtered_df = filter_games(
    df,
    team=team,
    home_away=home_away,
    min_win_pct=min_win_pct,
    max_win_pct=max_win_pct,
    min_win_streak=min_win_streak,
    min_loss_streak=min_loss_streak,
    season=season
)

# Results
st.subheader("Filtered Games")
st.write(f"🔎 {len(filtered_df)} result(s)")
st.dataframe(filtered_df.head(50))

# Summary stats
st.subheader("Summary")
summary = calculate_summary(filtered_df)
st.write(summary)

# Plots
with st.expander("📊 Visualizations"):
    plot_win_pct_distribution(filtered_df)
    plot_streak_distribution(filtered_df, streak_type='team_win_streak')
    plot_streak_distribution(filtered_df, streak_type='team_loss_streak')

# Export
if st.button("Download Results as CSV"):
    export_filtered_df(filtered_df, "filtered_results.csv")
    st.success("File saved as filtered_results.csv")
