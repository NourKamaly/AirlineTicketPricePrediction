# AirlineTicketPricePrediction from End to End
# Analysis:

Analysis was done using Power BI, answering 20 questions about the data
![analysis report ](https://user-images.githubusercontent.com/76780379/170844979-5b42173d-e2a4-40fd-859a-5c16e60694c2.jpg)
# Preprocessing:

1. Due to the presence of the date feature, the data was handled as a time series problem
2. Data was sorted (mergesort) according to month, day, flight departure hour, and flight departure minute
to prevent data leakage when splittling the data into the training and validation set
3. Features extracted: weekday of flight, flight day, flight month, and distance between the two cities
4. Feature balance applied to airline
5. Outlier detection using the interquartile range
6. Feature selection using the p value
7. Feature engineering applied to the other features
8. Data transformation using the discrete cosine transform as this is a time series data (we suspected that the data may have been periodic)
![time series data](https://user-images.githubusercontent.com/76780379/170845001-c72271a3-f6b0-4886-bdf2-d2d2e7058622.jpg)
Multiple encoders were used and this resulted in 3 different dataset and training was done on each one of them separatly
# Modeling :

10 models were used in Regression
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

Random Forest got the best r2 score in the regression testing set so it was chosen as the final regression model
![random forest mse](https://user-images.githubusercontent.com/76780379/172643425-76dfa607-f2ab-40cb-9249-55b336ab592d.jpg)

9 models were used in classification
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
Deployment was done using HTML & CSS & bootstrap for the interface and the backened was made by Flask

![heroku interface](https://user-images.githubusercontent.com/76780379/172643666-dc5c3204-a044-4518-bc44-263e113841d0.jpg)


![deployment](https://user-images.githubusercontent.com/76780379/172643755-30eec144-13b4-4d40-a2b9-9d7dc951da93.jpg)
