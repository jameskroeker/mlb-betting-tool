import streamlit as st
import pandas as pd
from filters import filter_games, calculate_summary
from utils import export_filtered_df, plot_win_pct_distribution, plot_streak_distribution

# Load dataset
st.title("⚾ MLB Team Game Finder (2024 Enriched with Betting Data)")
data_file = "MLB_2024_Game_Data_FINAL_WORKSHEET.csv"
df = pd.read_csv(data_file)
df['date'] = pd.to_datetime(df['date'])

# Rename columns for consistency
df['team'] = df['team_x']

# Sidebar filters
st.sidebar.header("🔎 Search Filters")

st.sidebar.subheader("📅 Game Filters")
team = st.sidebar.text_input("Team (abbreviation)", help="Use team abbreviations like LAD, NYY, BOS")
home_away = st.sidebar.selectbox("Home or Away", ["All", "home", "away"])
if home_away == "All":
    home_away = None

st.sidebar.markdown("---")

# Section 2: Performance Filters
st.sidebar.subheader("📈 Performance Filters")
min_win_pct = st.sidebar.slider("Min Win %", 0.0, 1.0, 0.0, 0.01)
max_win_pct = st.sidebar.slider("Max Win %", 0.0, 1.0, 1.0, 0.01)
min_win_streak = st.sidebar.number_input("Min Win Streak", min_value=0, value=0)
min_loss_streak = st.sidebar.number_input("Min Loss Streak", min_value=0, value=0)

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

# Default guidance
if not st.session_state.search_clicked:
    st.markdown("### 👋 Welcome!")
    st.info("Use the filters in the sidebar to explore 2024 MLB game data enriched with betting insights. Click **Search** to begin.")

# Run query
if st.session_state.search_clicked:
    filtered_df = filter_games(
        df,
        team=team,
        home_away=home_away,
        min_win_pct=min_win_pct,
        max_win_pct=max_win_pct,
        min_win_streak=min_win_streak,
        min_loss_streak=min_loss_streak,
        season=None  # Only 2024
    )

    if filtered_df.empty:
        st.warning("No results found. Try adjusting your filters.")
    else:
        st.markdown("---")
        st.subheader("🎯 Filtered Games")
        st.write(f"🔎 {len(filtered_df)} result(s)")
        st.dataframe(filtered_df[['date', 'team', 'opponent', 'result', 'team_win_pct', 'team_win_streak', 'team_score', 'opp_score', 'hit_over', 'covered_runline', 'roi_$100_bet']].head(50))

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
