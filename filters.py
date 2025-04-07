import pandas as pd

def filter_games(df, team=None, home_away=None, min_win_pct=0.0, max_win_pct=1.0, min_win_streak=0, min_loss_streak=0, season=None):
    df_filtered = df.copy()

    if team:
        df_filtered = df_filtered[df_filtered['team'] == team.upper()]
    if home_away:
        df_filtered = df_filtered[df_filtered['home_away'] == home_away]
    if season:
        df_filtered = df_filtered[df_filtered['season'] == season]

    df_filtered = df_filtered[
        (df_filtered['team_win_pct'] >= min_win_pct) &
        (df_filtered['team_win_pct'] <= max_win_pct) &
        (df_filtered['team_win_streak'] >= min_win_streak) &
        (df_filtered['team_loss_streak'] >= min_loss_streak)
    ]

    return df_filtered


def calculate_summary(df):
    if df.empty:
        return {}

    summary = {}

    # Win/loss
    summary['win_count'] = int((df['result'] == 'W').sum())
    summary['loss_count'] = int((df['result'] == 'L').sum())

    # Performance
    summary['avg_win_pct'] = round(df['team_win_pct'].mean(), 3)
    summary['avg_win_margin'] = round((df[df['result'] == 'W']['team_score'] - df[df['result'] == 'W']['opp_score']).mean(), 2)
    summary['avg_loss_margin'] = round((df[df['result'] == 'L']['team_score'] - df[df['result'] == 'L']['opp_score']).mean(), 2)

    # Betting outcomes
    if 'hit_over' in df.columns:
        summary['hit_over_rate'] = f"{(df['hit_over'].mean() * 100):.1f}%"
    if 'covered_runline' in df.columns:
        summary['covered_runline_rate'] = f"{(df['covered_runline'].mean() * 100):.1f}%"
    if 'was_favorite' in df.columns:
        fav_wins = df[(df['was_favorite'] == True) & (df['result'] == 'W')]
        total_fav = df[df['was_favorite'] == True]
        summary['favorite_win_rate'] = f"{(len(fav_wins) / len(total_fav) * 100):.1f}%" if len(total_fav) > 0 else "N/A"
    if 'roi_$100_bet' in df.columns:
        summary['avg_roi_on_$100'] = f"${df['roi_$100_bet'].mean():.2f}"

    return summary
