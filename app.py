import streamlit as st
import pandas as pd
from filters import filter_games, calculate_summary
from utils import export_filtered_df, plot_win_pct_distribution, plot_streak_distribution

# Load dataset
st.title("⚾ MLB Team Game Finder (2021–2024)")
data_file = "MLB_Team_Game_Data_2021_2024_RESET.csv"
df = pd.read_csv(data_file)
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.header("🔎 Search Filters")

# Section 1: Game Filters
st.sidebar.subheader("📅 Game Filters")

team = st.sidebar.text_input("Team (abbreviation)", help="Use team abbreviations like LAD, NYY, BOS")
home_away = st.sidebar.selectbox("Home or Away", ["All", "home", "away"])
if home_away == "All":
    home_away = None

season_options = ['All Seasons'] + sorted(df['season'].dropna().unique().tolist())
season = st.sidebar.selectbox("Season", season_options)
if season == 'All Seasons':
    season = None

st.sidebar.markdown("---")

# Section 2: Performance Filters
st.sidebar.subheader("📈 Performance Filters")

min_win_pct = st.sidebar.slider("Min Win %", 0.0, 1.0, 0.0, 0.01, help="Minimum team win percentage")
max_win_pct = st.sidebar.slider("Max Win %", 0.0, 1.0, 1.0, 0.01, help="Maximum team win percentage")

min_win_streak = st.sidebar.number_input("Min Win Streak", min_value=0, value=0, help="Minimum number of consecutive wins")
min_loss_streak = st.sidebar.number_input("Min Loss Streak", min_value=0, value=0, help="Minimum number of consecutive losses")

# Button logic
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

# Run query only after clicking Search
if st.session_state.search_clicked:
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
        st.markdown("---")
        st.subheader("🎯 Filtered Games")
        st.write(f"🔎 {len(filtered_df)} result(s)")
        st.dataframe(filtered_df[['date', 'team', 'opponent', 'result', 'team_win_pct']].head(50))

        st.markdown("---")
        st.subheader("📊 Summary Stats")
        summary = calculate_summary(filtered_df)
        st.write(summary)

        with st.expander("📈 Visualizations"):
            plot_win_pct_distribution(filtered_df)
            plot_streak_distribution(filtered_df, streak_type='team_win_streak')
            plot_streak_distribution(filtered_df, streak_type='team_loss_streak')

        st.download_button(
            label="Download CSV of Results",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_results.csv",
            mime="text/csv",
            key="download_button"
        )
