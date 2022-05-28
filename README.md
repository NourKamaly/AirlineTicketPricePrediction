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
The preprocessing phase resulted in 3 different dataset and training was done on each one of them separatly
# Modeling :

10 models were used 
1. eXtreme Gradient Boosting Regressor
2. Poissom Regressor
3. Histogram Gradient Boosting Regressor
4. Linear Regressiom
5. Light Gradient Boosting Machine Regressor
6. Gradient Boosting Regressor
7. Extra Tree Regressor 
8. Bagging Regressor
9. Decision Tree Regressor
10. Random Forest 

Random Forest got the best r2 score in the regression testing set (0.9555) so it was chosen as the final regression model
![Random Forest](https://user-images.githubusercontent.com/76780379/170845111-a8631ed3-92ed-4378-932c-eccfd3714c87.jpg)

# Deployment:
Deployment was done using CSS & bootstrap for the interface and the backened was made by Flask
