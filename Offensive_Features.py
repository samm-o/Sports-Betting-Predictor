import pandas as pd
import numpy as np

# Load the data
data_2023 = pd.read_csv('./Cleaned NFL Data/final_nfl_2023_data.csv')
data_2022 = pd.read_csv('./Cleaned NFL Data/final_nfl_2022_data.csv')

all_data = pd.concat([data_2023, data_2022])

# Calculate the average points scored by the home and visitor teams.
avg_points_scored_home = all_data.groupby('Home')['HomeScore'].mean()
avg_points_scored_visitor = all_data.groupby('Visitor')['VisitorScore'].mean()

# Calculate the average points allowed by the home and visitor teams.
avg_points_allowed_home = all_data.groupby('Home')['VisitorScore'].mean()
avg_points_allowed_visitor = all_data.groupby('Visitor')['HomeScore'].mean()

# Calculate the overall average points scored and allowed by combining the home and visitor averages.
overall_avg_points_scored = (avg_points_scored_home + avg_points_scored_visitor) / 2
overall_avg_points_allowed = (avg_points_allowed_home + avg_points_allowed_visitor) / 2

# Calculate the total number of wins for home and visitor teams.
home_wins = all_data.groupby('Home')['HomeWon'].sum()
visitor_wins = all_data.groupby('Visitor').apply(lambda x: len(x) - x['HomeWon'].sum())

# Calculate the total number of games played by each team as home and visitor.
total_games_home = all_data['Home'].value_counts()
total_games_visitor = all_data['Visitor'].value_counts()

# Calculate the overall number of wins and total games played by each team.
overall_wins = home_wins + visitor_wins
total_games = total_games_home + total_games_visitor

# Calculate the win rate for each team.
win_rate = overall_wins / total_games

# Average yards per play
avg_yards_per_play_home = all_data.groupby('Home')['Yards'].mean()
avg_yards_per_play_visitor = all_data.groupby('Visitor')['Yards'].mean()
overall_avg_yards_per_play = (avg_yards_per_play_home + avg_yards_per_play_visitor) / 2

# Average total yards per game
total_yards_per_game_home = all_data.groupby(['SeasonYear', 'Home'])['Yards'].sum() / all_data.groupby(['SeasonYear', 'Home']).size()
total_yards_per_game_visitor = all_data.groupby(['SeasonYear', 'Visitor'])['Yards'].sum() / all_data.groupby(['SeasonYear', 'Visitor']).size()
overall_avg_yards_per_game = (total_yards_per_game_home + total_yards_per_game_visitor).groupby(level=1).mean()

# Average pass completion rate
avg_pass_completion_rate_home = all_data.groupby('Home', group_keys=False).apply(lambda x: 1 - x['IsIncomplete'].mean())
avg_pass_completion_rate_visitor = all_data.groupby('Visitor', group_keys=False).apply(lambda x: 1 - x['IsIncomplete'].mean())
overall_avg_pass_completion_rate = (avg_pass_completion_rate_home + avg_pass_completion_rate_visitor) / 2

# Average touchdowns per game
avg_touchdowns_per_game_home = all_data.groupby(['SeasonYear', 'Home'])['IsTouchdown'].sum() / all_data.groupby(['SeasonYear', 'Home']).size()
avg_touchdowns_per_game_visitor = all_data.groupby(['SeasonYear', 'Visitor'])['IsTouchdown'].sum() / all_data.groupby(['SeasonYear', 'Visitor']).size()
overall_avg_touchdowns_per_game = (avg_touchdowns_per_game_home + avg_touchdowns_per_game_visitor).groupby(level=1).mean()

# Average rush success rate
avg_rush_success_rate_home = all_data.groupby('Home', group_keys=False).apply(lambda x: x['Yards'][x['IsRush'] == 1].mean())
avg_rush_success_rate_visitor = all_data.groupby('Visitor', group_keys=False).apply(lambda x: x['Yards'][x['IsRush'] == 1].mean())
overall_avg_rush_success_rate = (avg_rush_success_rate_home + avg_rush_success_rate_visitor) / 2

# Creating a dataframe for the new offensive features
offensive_features = pd.DataFrame({
    'AvgPointsScored': overall_avg_points_scored,
    'AvgPointsAllowed': overall_avg_points_allowed,
    'WinRate': win_rate,
    'AvgYardsPerPlay': overall_avg_yards_per_play.values,
    'AvgYardsPerGame': overall_avg_yards_per_game.values,
    'AvgPassCompletionRate': overall_avg_pass_completion_rate.values,
    'AvgTouchdownsPerGame': overall_avg_touchdowns_per_game.values,
    'AvgRushSuccessRate': overall_avg_rush_success_rate.values
})

# Reset the index of the team_features DataFrame and rename the index column to "Team".
offensive_features.reset_index(inplace=True)
offensive_features.rename(columns={'Home': 'Team'}, inplace=True)

print(offensive_features.head())