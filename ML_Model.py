from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from Encoding import training_data, training_labels

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