from streamlit.runtime.scriptrunner import rerun
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

home_away = st.sidebar.selectbox("Home/Away", ["All", "home", "away"])
if home_away == "All":
    home_away = None

season_options = ['All Seasons'] + sorted(df['season'].dropna().unique().tolist())
season = st.sidebar.selectbox("Season", season_options)
if season == 'All Seasons':
    season = None

min_win_pct = st.sidebar.slider("Min Win %", 0.0, 1.0, 0.0, 0.01)
max_win_pct = st.sidebar.slider("Max Win %", 0.0, 1.0, 1.0, 0.01)

min_win_streak = st.sidebar.number_input("Min Win Streak", min_value=0, value=0)
min_loss_streak = st.sidebar.number_input("Min Loss Streak", min_value=0, value=0)

# Button logic
search_clicked = False
filtered_df = pd.DataFrame()

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Search"):
        search_clicked = True

with col2:
    if st.button("Reset"):
        rerun()

# Run query only after clicking Search
if search_clicked:
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

    if filtered_df.empty:
        st.warning("No results found. Try adjusting your filters.")
    else:
        st.subheader("Filtered Games")
        st.write(f"🔎 {len(filtered_df)} result(s)")
        st.dataframe(filtered_df.head(50))

        st.subheader("Summary")
        summary = calculate_summary(filtered_df)
        st.write(summary)

        with st.expander("📊 Visualizations"):
            plot_win_pct_distribution(filtered_df)
            plot_streak_distribution(filtered_df, streak_type='team_win_streak')
            plot_streak_distribution(filtered_df, streak_type='team_loss_streak')

        # Download Button
        st.download_button(
            label="Download CSV of Results",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_results.csv",
            mime="text/csv",
            key="download_button"
        )
