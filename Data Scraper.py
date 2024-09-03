import numpy as np
import pandas as pd
from maps import team_mapping

# Load the data
pd_2023 = pd.read_csv('./Raw NFL Data/nfl-2023.csv')
pd_2022 = pd.read_csv('./Raw NFL Data/nfl-2022.csv')
scores_2023 = pd.read_csv('./Raw NFL Data/nfl-2023-scores.csv')
scores_2022 = pd.read_csv('./Raw NFL Data/nfl-2022-scores.csv')

# Convert the 'GameDate' format in play-by-play data to match the 'Date' format in scores dataset
pd_2023['GameDate'] = pd.to_datetime(pd_2023['GameDate']).dt.strftime('%m/%d/%Y')
pd_2022['GameDate'] = pd.to_datetime(pd_2022['GameDate']).dt.strftime('%m/%d/%Y')

# Replace team names with abbreviations in scores data
scores_2023['Visitor'] = scores_2023['Visitor'].map(team_mapping)
scores_2023['Home'] = scores_2023['Home'].map(team_mapping)
scores_2022['Visitor'] = scores_2022['Visitor'].map(team_mapping)
scores_2022['Home'] = scores_2022['Home'].map(team_mapping)

# Filter DataFrames to include only overlapping date ranges
start_date_2023 = max(pd_2023['GameDate'].min(), scores_2023['Date'].min())
end_date_2023 = min(pd_2023['GameDate'].max(), scores_2023['Date'].max())

start_date_2022 = max(pd_2022['GameDate'].min(), scores_2022['Date'].min())
end_date_2022 = min(pd_2022['GameDate'].max(), scores_2022['Date'].max())

pd_2023_filtered = pd_2023[(pd_2023['GameDate'] >= start_date_2023) & (pd_2023['GameDate'] <= end_date_2023)]
scores_2023_filtered = scores_2023[(scores_2023['Date'] >= start_date_2023) & (scores_2023['Date'] <= end_date_2023)]

pd_2022_filtered = pd_2022[(pd_2022['GameDate'] >= start_date_2022) & (pd_2022['GameDate'] <= end_date_2022)]
scores_2022_filtered = scores_2022[(scores_2022['Date'] >= start_date_2022) & (scores_2022['Date'] <= end_date_2022)]

# Merge play-by-play data with scores data based on the date and each side's team abbreviation
merged_2023_data = pd_2023_filtered.merge(scores_2023_filtered, left_on=['GameDate', 'OffenseTeam', 'DefenseTeam'], right_on=['Date', 'Visitor', 'Home'], how='left')
merged_2023_data = merged_2023_data.merge(scores_2023_filtered, left_on=['GameDate', 'OffenseTeam', 'DefenseTeam'], right_on=['Date', 'Home', 'Visitor'], how='left', suffixes=('', '_reverse'))

merged_2022_data = pd_2022_filtered.merge(scores_2022_filtered, left_on=['GameDate', 'OffenseTeam', 'DefenseTeam'], right_on=['Date', 'Visitor', 'Home'], how='left')
merged_2022_data = merged_2022_data.merge(scores_2022_filtered, left_on=['GameDate', 'OffenseTeam', 'DefenseTeam'], right_on=['Date', 'Home', 'Visitor'], how='left', suffixes=('', '_reverse'))

# Combine columns to handle reverse matches
for column in ['Week', 'Visitor', 'VisitorScore', 'Home', 'HomeScore', 'OT']:
    merged_2023_data[column] = merged_2023_data[column].combine_first(merged_2023_data[column + '_reverse'])
    merged_2022_data[column] = merged_2022_data[column].combine_first(merged_2022_data[column + '_reverse'])
    
# Drop unnecessary columns
columns_to_drop = [column + '_reverse' for column in ['Week', 'Visitor', 'VisitorScore', 'Home', 'HomeScore', 'OT']]
merged_2023_data = merged_2023_data.drop(columns=columns_to_drop)
merged_2022_data = merged_2022_data.drop(columns=columns_to_drop)

# Drop OffenseTeam and DefenseTeam columns
merged_2023_data = merged_2023_data.drop(columns=['OffenseTeam', 'DefenseTeam'])
merged_2022_data = merged_2022_data.drop(columns=['OffenseTeam', 'DefenseTeam'])

# Add the "HomeWon" column
merged_2023_data['HomeWon'] = merged_2023_data['HomeScore'] > merged_2023_data['VisitorScore']
merged_2022_data['HomeWon'] = merged_2022_data['HomeScore'] > merged_2022_data['VisitorScore']

# Print the merged data to check for NaN values
merged_2023_data.to_csv('./Cleaned NFL Data/final_nfl_2023_data.csv', index=False)
merged_2022_data.to_csv('./Cleaned NFL Data/final_nfl_2022_data.csv', index=False)