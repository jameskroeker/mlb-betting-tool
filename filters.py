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
    win_games = df[df["result"] == "W"]
    loss_games = df[df["result"] == "L"]

    avg_win_margin = (win_games["team_score"] - win_games["opp_score"]).mean() if not win_games.empty else None
    avg_loss_margin = (loss_games["opp_score"] - loss_games["team_score"]).mean() if not loss_games.empty else None

    summary = {
        "Wins": int((df["result"] == "W").sum()),
        "Losses": int((df["result"] == "L").sum()),
        "Avg Win %": round(df["team_win_pct"].mean(), 3) if not df.empty else None,
        "Avg Win Streak": round(df["team_win_streak"].mean(), 2) if not df.empty else None,
        "Avg Loss Streak": round(df["team_loss_streak"].mean(), 2) if not df.empty else None,
        "Avg Margin of Victory": round(avg_win_margin, 2) if avg_win_margin is not None else None,
        "Avg Margin of Defeat": round(avg_loss_margin, 2) if avg_loss_margin is not None else None,
        "Max Win Streak": int(df["team_win_streak"].max()) if not df.empty else None,
        "Max Loss Streak": int(df["team_loss_streak"].max()) if not df.empty else None
    }
    return summary
