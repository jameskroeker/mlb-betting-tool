import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def export_filtered_df(df, filename="filtered_results.csv"):
    df.to_csv(filename, index=False)
    print(f"✅ Exported to {filename}")

def plot_win_pct_distribution(df, title="Team Win % Distribution"):
    plt.figure(figsize=(8, 5))
    df['team_win_pct'].dropna().hist(bins=20, edgecolor='black')
    plt.xlabel("Win Percentage")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_streak_distribution(df, streak_type='team_win_streak', title=None):
    streak_data = df[streak_type].dropna().value_counts().sort_index()
    if streak_data.empty:
        st.write(f"No data to display for {streak_type.replace('_', ' ')}.")
        return
    plt.figure(figsize=(8, 5))
    streak_data.plot(kind='bar')
    plt.xlabel("Streak Length")
    plt.ylabel("Frequency")
    plt.title(title or f"{streak_type.replace('_', ' ').title()} Distribution")
    plt.grid(True)
    st.pyplot(plt.gcf())
