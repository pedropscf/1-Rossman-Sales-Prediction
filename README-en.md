
### :pushpin: [__Ler em português__](https://github.com/pedropscf/1-Rossman-Sales-Prediction/blob/5ed9248695e7da027ef9554eea48d1c1cfdf71cb/README.md)

# Rossman store sales prediction over the next 6 weeks

Rossman is a pharmaceutic company with over than 3000 stores spread across 7 different countries in Europe. The company created a challenge at the Kaggle platform related to its business challenges to make sales predictions. The main problem is related to the differences created by having thousand of managers at the company, where they use different methodologies to create the sales prediction. Also, there are features that may not be using in those predictions, such as sazonality, store type, assortment or holidays.

The company needs a solution that is able to predict sales for each store across the next 6 weeks, thus, the main question is:

- **How much sales the store X is going to make over the next 6 weeks?**

## Features

To answer the challenge, the company  made available a data set with daily sales of different stores, along with information about the store, such its type, assortment. All features available at the data set are:

| Feature  | Description |
| ------------- | ------------- |
| store  | Store number |
| day_of_week  | Day of week  |
| date  | Data das vendas  |
| sales | Total sales realized on that day |
| customers | Number of customers at the store at that day |
| open | Whether the store is open |
| promo | Whether the store has a promotion |
| state_holiday | Wheter is a national holiday |
| school_holiday | Whether is a school holiday |
| store_type | Store type |
| assortment | Variety of products available |

In addition to the previous features, there are also features related to the presence of competitors its distance and extended promotions

## Solution

The problem was classified as a tradicional regression problem that could be solved with machine learning and time series. A solution was realized in development cycles from end to end and is described briefly (full solution along with the code can be seen [here.](https://github.com/pedropscf/1-Rossman-Sales-Prediction/blob/7e3111cdad78d7373659ab99296c9290d8afb02d/m05_vid01_store_sales_prediction_PTBR.ipynb) ) in:

### Data cleaning and manipulation

The data set contains over than 1 million rows and 18 features and the initial job had a focus to suit the data types properly at the dataframe, followed by the job of filling null values to features related to competitors and extended promotions.

### Feature Engineering

At this point, the main features created were related to time and derived from the timestamp, such as number of week, month and month/year. Due to the high number of null values to features related to the extended promotions, features about promotion and extended promotions were joined together, in order to create a single feature that informs whether the story has a promotion.

### Exploratory Data Analysis

At the EDA, univariate data analysis, bivariate data analysis and correlation matrix among numerical data and caategorical data were realized in other to understand the relation between them. Also, a analysis related to the behavior of the target variable (sales) and different categorical data (such as store type and assortment) has been made.

Finally, different hypothesis about sales have been made and tested, helping by bringing insights to the problem.

### Feature selection and transformation

Initially, all features were transformed in some way:

- Log: target feature was transformed by applying the logarithm to its values;

- Rescaling: other features were transformed with the RobustScaler and MinMaxScaler methods, such as year or distance to competitor;

- Nature: cyclical features, such as the ones related to time (month, number of week, day of week) were transformed by trigonometric decomposition (sine and cosine  contributions).

With all features properly transformed and rescaled, a Random Forest regressor, along with the Boruta algorithm were used in other to extract which features or combinations are more relevant to the regression problem. With the result, it is possible to determine which features go for the training stage.

### Model creation and cross validation

From the selectec features, different machine learning regression models were trained, such as linear regression, regularized linear regression, random forest regression and XGBoost. Initially, the training was done on the training data, followed by the model evaluation on the test data.  Then, a training on the models were made by dividing the training data in 5 periods of time (5 folds cross validation) and all error metrics were saved.

Thereby, it was observed that linear models presented a high error metric in comparison to the ensemble models, this was expected due to the non linear behavior of sales across time. Random forest and XGBoost present a very low error metric, with XGBoost regressor model being the chosen one.

### Model performance analysis

Finally, after the model has been trained and tuned, the company's question can be answered

- **How much sales the store X is going to make over the next 6 weeks?** The model was deployed to production enviroment trough the Heroku Cloud and a Telegram bot was created to provide the prediction of the sales across the next 6 weeks of each store. The bot can be acessed trough [this Telegram channel](https://t.me/pedropscf_RossmanBot). This way, it is possible to consult the sales prediction of different stores with a unified methodology.

- Other points were observed, considering the mean absolut percentage error, it is possible to obtain a range of stimated sales values for the next period. With this, the **total sales for all stores over the next period is $279 million**, where the worst scenario is $240 million and the best scenario of $317 million.

<p align="center">
  <img src="https://github.com/pedropscf/1-Rossman-Sales-Prediction/blob/7e3111cdad78d7373659ab99296c9290d8afb02d/img/model_results.png" />
</p>

- By analyzing the model and its errors, it is possible to see that the model has a slight trend to predict sales values that are smaller than the real values. Thus, bringing a margin of safety of the predicted values.

## Technologies used

**Data manipulation and cleaning:** pandas, numpy

**Data visualization:** matplotlib, seaborn

**Machine learning:** Regression models (scikit-learn e xgboost), feature selection (Boruta)

**Cloud environment:** Flask, requests, desenho de API e Heroku


## About me
I am data science enthusiast, learning new applications of Machine Learning, AI and Data Science in general to solve a diverse range of business problems.

## Authors

- Pedro Fernandes [@pedropscf](https://www.github.com/pedropscf)
