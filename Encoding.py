import pandas as pd
import numpy as np

from Offensive_Features import offensive_features, all_data
from Defensive_Features import defensive_features

# Load the data
file_path = './2024 NFL Schedule.csv'
upcoming_games = pd.read_csv(file_path)

# Merging with the existing combined features
team_features_complete = offensive_features.merge(defensive_features, on='Team')

upcoming_encoded_home = upcoming_games.merge(team_features_complete, left_on='Home', right_on='Team', how='left')
upcoming_encoded_both = upcoming_encoded_home.merge(team_features_complete, left_on='Visitor', right_on='Team', suffixes=('_Home', '_Visitor'), how='left')

# Calculate the difference in features as this might be a more predictive representation
for col in ['AvgPointsScored', 'AvgPointsAllowed', 'WinRate', 'AvgPointsDefended', 'AvgConcededPlays', 'AvgForcedTurnovers',
            'AvgYardsPerPlay', 'AvgYardsPerGame', 'AvgPassCompletionRate', 'AvgTouchdownsPerGame', 'AvgRushSuccessRate',
            'AvgYardsAllowedPerPlay', 'AvgYardsAllowedPerGame', 'AvgPassCompletionAllowedRate', 'AvgTouchdownsAllowedPerGame', 'AvgRushSuccessAllowedRate']:
    upcoming_encoded_both[f'Diff_{col}'] = upcoming_encoded_both[f'{col}_Home'] - upcoming_encoded_both[f'{col}_Visitor']

# Selecting only the difference columns and the teams for clarity
upcoming_encoded_final = upcoming_encoded_both[['Home', 'Visitor'] + [col for col in upcoming_encoded_both.columns if 'Diff_' in col]]

# Merge play-by-play data with team features for home teams
training_encoded_home = all_data.merge(team_features_complete, left_on='Home', right_on='Team', how='left')
# Merge the result with team features for visitor teams
training_encoded_both = training_encoded_home.merge(team_features_complete, left_on='Visitor', right_on='Team', suffixes=('_Home', '_Visitor'), how='left')

# Calculate the difference in features
for col in ['AvgPointsScored', 'AvgPointsAllowed', 'WinRate', 'AvgPointsDefended', 'AvgConcededPlays', 'AvgForcedTurnovers',
            'AvgYardsPerPlay', 'AvgYardsPerGame', 'AvgPassCompletionRate', 'AvgTouchdownsPerGame', 'AvgRushSuccessRate',
            'AvgYardsAllowedPerPlay', 'AvgYardsAllowedPerGame', 'AvgPassCompletionAllowedRate', 'AvgTouchdownsAllowedPerGame', 'AvgRushSuccessAllowedRate']:
    training_encoded_both[f'Diff_{col}'] = training_encoded_both[f'{col}_Home'] - training_encoded_both[f'{col}_Visitor']

# Filtering out the required columns
training_data = training_encoded_both[[col for col in training_encoded_both.columns if 'Diff_' in col]]
training_labels = training_encoded_both['HomeWon']

