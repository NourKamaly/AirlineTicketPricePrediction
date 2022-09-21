# AirlineTicketPricePrediction from End to End
This machine learning project aims to do 2 main things separately:
1. Predicting the airline ticket price (regression problem).
2. Classifying the ticket price range into 4 categories: cheap, moderate, expensive, very expensive.

These two parts rely on 10 features: date, airline, ch code (airline code), num code, time taken, stop, arrival time, type, route.

Data format: comma separated values file. 
# Project Lifecycle
1. Data Analysis
2. Preprocessing
3. Modeling
4. Testing
5. Models Analysis (not done yet)
6. Deployment on heroku

Project can be found at: https://github.com/NourKamaly/AirlineTicketPricePrediction

# Tech Stack
Programming Languages: Python 3.9, JavaScript

Markup Languages: HTML, CSS

Tools used: PowerBI

Frameworks: Bootstrap

Libraries used: NumPy, pandas, dataprep, matplotlib, scipy, seabron, TensorFlow, xgboost, sklearn, joblib, flask.

# Data Analysis:

Analysis was done using Power BI, answering 20 questions about the data
![analysis report ](https://user-images.githubusercontent.com/76780379/170844979-5b42173d-e2a4-40fd-859a-5c16e60694c2.jpg)
# Preprocessing:

1. Due to the presence of the date feature, the data was handled as a time series forecasting problem
2. Data was sorted (mergesort) according to month, day, flight departure hour, and flight departure minute
to prevent data leakage when splittling the data into the training and validation set.
3. Features extracted: weekday of flight, flight day, flight month, and distance between the source and destination cities.
4. Feature balance applied to airline as some categories had relatively low frequency
5. Outlier detection using the interquartile range on the label (price)
6. Feature engineering applied to the other features
7. Feature selection using the p value
8. Data transformation using the discrete cosine transform as this is a time series data (we suspected that the data may have been periodic)
![time series data](https://user-images.githubusercontent.com/76780379/170845001-c72271a3-f6b0-4886-bdf2-d2d2e7058622.jpg)
Multiple encoders were used and this resulted in 3 different dataset and training was done on each one of them separatly
# Modeling :

10 models were tried in Regression:
1. eXtreme Gradient Boosting Regressor
2. Poisson Regressor
3. Histogram Gradient Boosting Regressor
4. Linear Regression
5. Light Gradient Boosting Machine Regressor
6. Gradient Boosting Regressor
7. Extra Tree Regressor 
8. Bagging Regressor
9. Decision Tree Regressor
10. Random Forest 
11. A bagging ensemble learning model (simple averaging) made with: HistGradientBoostingRegressor,LGBMRegressor, ExtraTreesRegressor, BaggingRegressor, RandomForestRegressor 

The ensemble model and random forest got the 2 best r2 score in the regression testing set

Ensemble model r2 score: 0.982

Random Forest r2 score: 0.980

![random forest mse](https://user-images.githubusercontent.com/76780379/172643425-76dfa607-f2ab-40cb-9249-55b336ab592d.jpg)

9 models were tried in classification:
1. Ada Boost
2. Gradient Boosting Classifier
3. Bagging Classifier
4. Random Forest    
5. eXtreme Gradient Boosting Classifier
6. Decision Tree Classifier
7. Histogram Gradient Boosting Classifier     
8. Extra Tree Classifier 
9. Ensemble Stacking model that consists of RF, bagging classifier , extra tree classifier (the best performing models) 

# Deployment:
Deployment was done using HTML, CSS, Javascript, bootstrap for the interface and the backened was made by Flask.

The Website Link: https://airline-ticket-prediction-app.herokuapp.com/

![website](https://user-images.githubusercontent.com/73191469/172854369-b3791318-0408-4e82-a2a0-7dd7ee7197a2.png)
