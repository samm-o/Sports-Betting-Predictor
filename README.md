# NFL 2024 Moneyline Predictions

Welcome to the NFL 2024 Moneyline Predictions project! This project aims to predict the outcomes of NFL games using machine learning models. The predictions are displayed on a web application, where users can view matchups split into weeks along with confidence scores from three different models.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Data Preparation](#data-preparation)
- [Machine Learning Models](#machine-learning-models)
- [Web Application](#web-application)
- [Installation](#installation)
- [Usage](#usage)

## Overview

This project uses historical NFL data to train machine learning models that predict the outcomes of upcoming games. The predictions are displayed on a web application, where users can view matchups split into weeks along with confidence scores from three different models: Logistic Regression, Random Forest, and Gradient Boosting.

## Features

- **Weekly Matchups**: View matchups split into weeks, with each week displaying the games and their predicted outcomes.
- **Confidence Scores**: Each matchup card displays confidence scores from three different models: Logistic Regression, Random Forest, and Gradient Boosting.
- **Defensive and Offensive Features**: The models are trained using various defensive and offensive features extracted from historical data.

## Data Preparation

The data preparation involves several steps, including data cleaning, feature extraction, and encoding. The following files are used for data preparation:

- **[Data Scraper.py](Data%20Scraper.py)**: Scrapes raw NFL data from various sources.
- **[Defensive_Features.py](Defensive_Features.py)**: Extracts defensive features such as average points defended, average conceded plays, and more.
- **[Offensive_Features.py](Offensive_Features.py)**: Extracts offensive features such as average points scored, win rate, and more.
- **[Encoding.py](Encoding.py)**: Encodes categorical variables for use in machine learning models.

## Machine Learning Models

The machine learning models are trained using the prepared data. The following file is used for training the models:

- **[ML_Model.py](ML_Model.py)**: Trains Logistic Regression, Random Forest, and Gradient Boosting models using the extracted features. The predictions are saved to CSV files.

## Web Application

The web application is built using React and Flask. The following files are used for the web application:

- **[nfl-predictions/src/components/Matchup.js](nfl-predictions/src/components/Matchup.js)**: Displays individual matchup cards with confidence scores.
- **[nfl-predictions/src/components/MatchupList.js](nfl-predictions/src/components/MatchupList.js)**: Groups matchups by week and renders them.
- **[nfl-predictions/src/App.css](nfl-predictions/src/App.css)**: Styles for the web application.
- **[nfl-predictions/src/components/Matchup.css](nfl-predictions/src/components/Matchup.css)**: Styles for the matchup cards.

### Screenshots

![image](https://github.com/user-attachments/assets/76c50fe5-3c22-48ca-8eac-adb3cdb11171)


## Installation

To install and run the project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/nfl-predictions.git
   cd nfl-predictions
2. Install the dependencies:
    ```sh
    npm install
3. Start the flask backend server -> Start the React development server
    ```sh
    python app.py
    npm start

## Usage

Once the servers are running, open your browser and navigate to http://localhost:3000 to view the web application. You can browse through the weekly matchups and view the confidence scores for each game.