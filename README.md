# NBA MVP Predictor

## Overview
This project leveraged webscraping to collect data on over 30 seasons of NBA teams, players, and MVP winners. The data was then cleaned, filtered, and merged to create a comprehensive database that was ideal for predictive modeling. A RandomForest model with 50 predictors was developed to predict the NBA MVP standings for the upcoming NBA season with 73% accuracy. The model was backtested to evaluate performance and reduce overfitting to ensure accuracy.

## Technologies
- Python
- Pandas
- BS4
- Requests
- Scikit-Learn
- Matplotlib

## Data Collection and Preparation
The data was collected through webscraping using BeautifulSoup4 and Requests. Data on NBA teams, players, and MVP winners were collected from over 30 seasons of NBA history. The data was cleaned, filtered, and merged using Pandas.

## Model Development and Validation
A RandomForest model with 50 predictors was developed using Scikit-Learn. The model was then backtested to evaluate its performance and reduce overfitting. The final model had an accuracy rate of 73%.

## Results
The RandomForest model was able to accurately predict the NBA MVP standings for the upcoming NBA season with an accuracy rate of 73%. This project demonstrates the power of webscraping and machine learning in predicting future outcomes in sports.
