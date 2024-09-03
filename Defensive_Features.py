import pandas as pd
import numpy as np

# Load the data
data_2023 = pd.read_csv('./Cleaned NFL Data/final_nfl_2023_data.csv')
data_2022 = pd.read_csv('./Cleaned NFL Data/final_nfl_2022_data.csv')
all_data = pd.concat([data_2023, data_2022])

# A play is considered successful for the offense if it results in a touchdown or doesn't result in a turnover.
# Create a new column 'SuccessfulPlay' in the all_data DataFrame to represent this.
all_data['SuccessfulPlay'] = all_data['IsTouchdown'] | (~all_data['IsInterception'] & ~all_data['IsFumble'])

# Calculate the average rate of successful plays conceded when playing at home.
avg_conceded_plays_home = all_data.groupby('Home')['SuccessfulPlay'].mean()

# Calculate the average rate of successful plays conceded when playing as a visitor.
avg_conceded_plays_visitor = all_data.groupby('Visitor')['SuccessfulPlay'].mean()

# Calculate the overall average rate of successful plays conceded for each team.
overall_avg_conceded_plays = (avg_conceded_plays_home + avg_conceded_plays_visitor) / 2

# 3. Average forced turnovers:
# Create a new column 'Turnover' that indicates if a play resulted in a turnover (either interception or fumble).
all_data['Turnover'] = all_data['IsInterception'] | all_data['IsFumble']

# Calculate the average rate of turnovers forced when playing at home.
avg_forced_turnovers_home = all_data.groupby('Home')['Turnover'].mean()

# Calculate the average rate of turnovers forced when playing as a visitor.
avg_forced_turnovers_visitor = all_data.groupby('Visitor')['Turnover'].mean()

# Calculate the overall average rate of turnovers forced for each team.
overall_avg_forced_turnovers = (avg_forced_turnovers_home + avg_forced_turnovers_visitor) / 2

# 1. Average yards allowed per play
avg_yards_allowed_per_play_home = all_data.groupby('Home')['Yards'].mean()
avg_yards_allowed_per_play_visitor = all_data.groupby('Visitor')['Yards'].mean()
overall_avg_yards_allowed_per_play = (avg_yards_allowed_per_play_home + avg_yards_allowed_per_play_visitor) / 2

# 2. Average total yards allowed per game
total_yards_allowed_per_game_home = all_data.groupby(['SeasonYear', 'Home'])['Yards'].sum() / all_data.groupby(['SeasonYear', 'Home']).size()
total_yards_allowed_per_game_visitor = all_data.groupby(['SeasonYear', 'Visitor'])['Yards'].sum() / all_data.groupby(['SeasonYear', 'Visitor']).size()
overall_avg_yards_allowed_per_game = (total_yards_allowed_per_game_home + total_yards_allowed_per_game_visitor).groupby(level=1).mean()

# 3. Average pass completion allowed rate
avg_pass_completion_allowed_rate_home = all_data.groupby('Home').apply(lambda x: 1 - x['IsIncomplete'].mean())
avg_pass_completion_allowed_rate_visitor = all_data.groupby('Visitor').apply(lambda x: 1 - x['IsIncomplete'].mean())
overall_avg_pass_completion_allowed_rate = (avg_pass_completion_allowed_rate_home + avg_pass_completion_allowed_rate_visitor) / 2

# 4. Average touchdowns allowed per game
avg_touchdowns_allowed_per_game_home = all_data.groupby(['SeasonYear', 'Home'])['IsTouchdown'].sum() / all_data.groupby(['SeasonYear', 'Home']).size()
avg_touchdowns_allowed_per_game_visitor = all_data.groupby(['SeasonYear', 'Visitor'])['IsTouchdown'].sum() / all_data.groupby(['SeasonYear', 'Visitor']).size()
overall_avg_touchdowns_allowed_per_game = (avg_touchdowns_allowed_per_game_home + avg_touchdowns_allowed_per_game_visitor).groupby(level=1).mean()

# 5. Average rush success allowed rate
avg_rush_success_allowed_rate_home = all_data.groupby('Home').apply(lambda x: x['Yards'][x['IsRush'] == 1].mean())
avg_rush_success_allowed_rate_visitor = all_data.groupby('Visitor').apply(lambda x: x['Yards'][x['IsRush'] == 1].mean())
overall_avg_rush_success_allowed_rate = (avg_rush_success_allowed_rate_home + avg_rush_success_allowed_rate_visitor) / 2

# Calculate the average points allowed by the home and visitor teams.
avg_points_allowed_home = all_data.groupby('Home')['VisitorScore'].mean()
avg_points_allowed_visitor = all_data.groupby('Visitor')['HomeScore'].mean()
overall_avg_points_allowed = (avg_points_allowed_home + avg_points_allowed_visitor) / 2

# Creating a dataframe for the new defensive features
defensive_features = pd.DataFrame({
    'AvgPointsDefended': overall_avg_points_allowed,
    'AvgConcededPlays': overall_avg_conceded_plays.values,
    'AvgForcedTurnovers': overall_avg_forced_turnovers.values,
    'AvgYardsAllowedPerPlay': overall_avg_yards_allowed_per_play.values,
    'AvgYardsAllowedPerGame': overall_avg_yards_allowed_per_game.values,
    'AvgPassCompletionAllowedRate': overall_avg_pass_completion_allowed_rate.values,
    'AvgTouchdownsAllowedPerGame': overall_avg_touchdowns_allowed_per_game.values,
    'AvgRushSuccessAllowedRate': overall_avg_rush_success_allowed_rate.values
})

defensive_features.reset_index(inplace=True)
defensive_features.rename(columns={'Home': 'Team'}, inplace=True)

print(defensive_features.head())