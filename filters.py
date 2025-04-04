import pandas as pd

def filter_games(
    df,
    team=None,
    home_away=None,
    min_win_pct=0.0,
    max_win_pct=1.0,
    min_win_streak=0,
    min_loss_streak=0,
    season=None
):
    result = df.copy()

    if team:
        result = result[result["team"].str.upper() == team.upper()]
    if home_away:
        result = result[result["home_away"] == home_away]
    if season:
        result = result[result["season"] == season]
    if min_win_pct is not None:
        result = result[result["team_win_pct"] >= min_win_pct]
    if max_win_pct is not None:
        result = result[result["team_win_pct"] <= max_win_pct]
    if min_win_streak > 0:
        result = result[result["team_win_streak"] >= min_win_streak]
    if min_loss_streak > 0:
        result = result[result["team_loss_streak"] >= min_loss_streak]

    return result

def calculate_summary(df):
    summary = {
        "Wins": int((df["result"] == "W").sum()),
        "Losses": int((df["result"] == "L").sum()),
        "Avg Win %": round(df["team_win_pct"].mean(), 3) if not df.empty else None,
        "Avg Win Streak": round(df["team_win_streak"].mean(), 2) if not df.empty else None,
        "Avg Loss Streak": round(df["team_loss_streak"].mean(), 2) if not df.empty else None,
    }
    return summary
