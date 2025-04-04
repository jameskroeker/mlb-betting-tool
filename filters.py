import pandas as pd

def filter_games(df, team=None, home_away=None, min_win_pct=None, max_win_pct=None,
                 min_win_streak=None, min_loss_streak=None, season=None):
    result = df.copy()
    if team:
        result = result[result['team'].str.upper() == team.upper()]
    if home_away:
        result = result[result['home_away'] == home_away]
    if min_win_pct is not None:
        result = result[result['team_win_pct'] >= min_win_pct]
    if max_win_pct is not None:
        result = result[result['team_win_pct'] <= max_win_pct]
    if min_win_streak:
        result = result[result['team_win_streak'] >= min_win_streak]
    if min_loss_streak:
        result = result[result['team_loss_streak'] >= min_loss_streak]
    if season:
        result = result[result['season'] == season]
    return result

def calculate_summary(df):
    if df.empty:
        return {
            "total_games": 0,
            "win_count": 0,
            "loss_count": 0,
            "win_rate": None
        }
    win_count = (df['result'] == 'W').sum()
    loss_count = (df['result'] == 'L').sum()
    total = len(df)
    win_rate = win_count / total if total > 0 else None
    return {
        "total_games": total,
        "win_count": win_count,
        "loss_count": loss_count,
        "win_rate": round(win_rate, 3)
    }