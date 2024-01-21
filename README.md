# Big-Mart-Store-Sales-Prediction

## 📜 Problem Statement

Nowadays, shopping mals and Big Marts keep track of individual item sales data in order to forecast future client demand and adjust inventory management. In a data warehouse, these data stores hold a significant amount of consumer information and particular item details. Build a solution that should able to predict the sales of the different stores of Big Mart according to the provided dataset.

## 👨‍🏫 Approach

The classical machine learning tasks like Data Exploration, Data Cleaning, Feature Engineering, Model Building and Model Testing. Try out different machine learning algorithms that’s best fit for the above case.

## 📃 Dataset

Link: https://www.kaggle.com/brijbhushannanda1979/bigmart-sales-data

## 📚 Data Description

Item_Identifier: Unique product ID

Item_Weight: Weight of product

Item_Fat_Content: Whether the product is low fat or not

Item_Visibility: The % of total display area of all products in a store allocated to the particular product

Item_Type: The category to which the product belongs

Item_MRP: Maximum Retail Price (list price) of the product

Outlet_Identifier: Unique store ID

Outlet_Establishment_Year: The year in which store was established

Outlet_Size: The size of the store in terms of ground area covered

Outlet_Location_Type: The type of city in which the store is located

Outlet_Type: Whether the outlet is just a grocery store or some sort of supermarket

Item_Outlet_Sales: Sales of the product in the particulat store. This is the outcome variable to be predicted.

## ⚒ Data Preprocessing

1. Exploratory Data Analysis
2. Categorial Features Analysis & Visualization
3. Numerical Features Analysis & Visualization
4. Outlier Removal
5. Missing Value Imputation
6. One-Hot Encoding
7. VIF
8. Feature Transformation

## ⚙ Model Fitting

1. Linear Regression
2. Lasso Regression
3. Ridge Regression
4. Decision Tree Regression
5. Random Forest Regressor
6. SVR
7. KNN Regression
8. Bagging
9. Gradient Boost Regressor
10. XGBRegressor
11. Cat Boost Regressor

## ⚖ Hyper-parameter Tuning

1. Grid Search CV
2. Randomized Search CV

## 📋 Result

| Model Name                  | Adjusted_R2_Train | Adjusted_R2_Test |
| --------------------------- | ----------------- | ---------------- |
| Linear Regression           | 0.684181          | 0.696789         |
| Lasso Regression            | 0.683903          | 0.696796         |
| Ridge Regression            | 0.684167          | 0.696734         |
| Decision Tree Regressor     | 0.725233          | 0.690461         |
| Random Forest Regressor     | 0.724835          | 0.691105         |
| KNN Regressor               | 0.737105          | 0.619672         |
| Bag Linear Regression       | 0.684170          | 0.696787         |
| Bag Decision Tree Regressor | 0.951230          | 0.665012         |
| Bag KNN Regressor           | 0.751586          | 0.635977         |
| Gradient Boosting           | 0.713710          | 0.710689         |
| XGBRegressor                | 0.716467          | 0.709214         |
| Cat Boost Regressor         | 0.712288          | 0.713226         |

## 🌟 Best Model

Cat Boost Regressor with highest R2 score: 71.32 %

## 👨‍💻 Render app Link

[big-mart-sales-forecast](https://big-mart-sales-forecast.onrender.com)

If you want to test the application, please download the .csv files in the [sample_datasets](sample_datasets) folder and use them.
