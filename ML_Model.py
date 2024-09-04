from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from Encoding import training_data, training_labels, upcoming_encoded_final

# Exclude rows with NaN values from the training data and labels
training_data_cleaned = training_data.dropna()
training_labels_cleaned = training_labels.loc[training_data_cleaned.index]

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(training_data_cleaned, training_labels_cleaned, test_size=0.2, random_state=42)

# Define parameter grids for each model
param_grid_logreg = {
    'solver': ['liblinear', 'lbfgs'],
    'C': [0.01, 0.1, 1, 10],
    'max_iter': [100, 200, 300]
}

param_grid_rf = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

param_grid_gb = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 4, 5]
}

# Initialize the models
logreg = LogisticRegression()
rf = RandomForestClassifier()
gb = GradientBoostingClassifier()

# Initialize GridSearchCV for each model
grid_search_logreg = GridSearchCV(logreg, param_grid_logreg, cv=5, scoring='accuracy')
grid_search_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='accuracy')
grid_search_gb = GridSearchCV(gb, param_grid_gb, cv=5, scoring='accuracy')

# Fit the models
grid_search_logreg.fit(X_train, y_train)
grid_search_rf.fit(X_train, y_train)
grid_search_gb.fit(X_train, y_train)

# Print the best parameters and scores
print(f'Best parameters for Logistic Regression: {grid_search_logreg.best_params_}')
print(f'Best cross-validation score for Logistic Regression: {grid_search_logreg.best_score_}')

print(f'Best parameters for Random Forest: {grid_search_rf.best_params_}')
print(f'Best cross-validation score for Random Forest: {grid_search_rf.best_score_}')

print(f'Best parameters for Gradient Boosting: {grid_search_gb.best_params_}')
print(f'Best cross-validation score for Gradient Boosting: {grid_search_gb.best_score_}')

# Extract the best parameters from the grid search
best_params_logreg = grid_search_logreg.best_params_
best_params_rf = grid_search_rf.best_params_
best_params_gb = grid_search_gb.best_params_

# Train the models using the best parameters
logreg_best = LogisticRegression(**best_params_logreg)
rf_best = RandomForestClassifier(**best_params_rf)
gb_best = GradientBoostingClassifier(**best_params_gb)

logreg_best.fit(training_data_cleaned, training_labels_cleaned)
rf_best.fit(training_data_cleaned, training_labels_cleaned)
gb_best.fit(training_data_cleaned, training_labels_cleaned)

# Make predictions for the upcoming games
upcoming_features = upcoming_encoded_final[[col for col in upcoming_encoded_final.columns if 'Diff_' in col]]

logreg_probabilities = logreg_best.predict_proba(upcoming_features)[:, 1]
rf_probabilities = rf_best.predict_proba(upcoming_features)[:, 1]
gb_probabilities = gb_best.predict_proba(upcoming_features)[:, 1]

# Add the predictions to the upcoming games dataframe using .loc to avoid SettingWithCopyWarning
upcoming_encoded_final.loc[:, 'LogReg_HomeWinProbability'] = logreg_probabilities
upcoming_encoded_final.loc[:, 'RF_HomeWinProbability'] = rf_probabilities
upcoming_encoded_final.loc[:, 'GB_HomeWinProbability'] = gb_probabilities

# Save the predictions to CSV files without sorting
upcoming_encoded_final[['Home', 'Visitor', 'LogReg_HomeWinProbability']].to_csv('upcoming_predictions_logreg.csv', index=False)
upcoming_encoded_final[['Home', 'Visitor', 'RF_HomeWinProbability']].to_csv('upcoming_predictions_rf.csv', index=False)
upcoming_encoded_final[['Home', 'Visitor', 'GB_HomeWinProbability']].to_csv('upcoming_predictions_gb.csv', index=False)

# Print the predictions
print("Upcoming Predictions using Logistic Regression:")
print(upcoming_encoded_final[['Home', 'Visitor', 'LogReg_HomeWinProbability']])

print("Upcoming Predictions using Random Forest:")
print(upcoming_encoded_final[['Home', 'Visitor', 'RF_HomeWinProbability']])

print("Upcoming Predictions using Gradient Boosting:")
print(upcoming_encoded_final[['Home', 'Visitor', 'GB_HomeWinProbability']])