import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime


class Rossman(object):
    
    def __init__(self):
        
        self.home_path = '/home/pedro/Documentos/repositories/1-Rossman-Sales-Prediction'
        self.competition_distance_scaler = pickle.load(open(self.home_path + 'parameters/competition_distance_scaler.pkl','rb'))
        self.time_month_scaler           = pickle.load(open(self.home_path + 'parameters/time_month_scaler.pkl','rb'))
        self.year_scaler                 = pickle.load(open(self.home_path + 'parameters/year_scaler.pkl','rb'))
        self.promo_time_week_scaler      = pickle.load(open(self.home_path + 'parameters/promo_time_week_scaler.pkl','rb'))
        self_encoding_store_type         = pickle.load(open(self.home_path + 'parameters/enconding_store_type.pkl','rb'))        

            
    def data_cleaning(self,df1):

        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo',
                   'StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment',
                   'CompetitionDistance', 'CompetitionOpenSinceMonth',
                   'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek',
                   'Promo2SinceYear', 'PromoInterval']

        # Changing write pattern to snakecase

        snakecase = lambda x: inflection.underscore( x )

        cols_new = list( map( snakecase, cols_old ) )

        # Renaming
        df1.columns = cols_new

        ## 1.3. Data Types

        df1['date'] = pd.to_datetime(df1['date'])

        ## 1.5. Fillout NA

        # First, we must analyze what every variable and data with NA values

        # competition_distance
        ## Assumption: if it is NA, maybe it is because the store doesnt have an near competitor
        ## What has been done: CONSIDER AN EXTREME DISTANT RANGE FROM NEAR COMPETITOR

        df1['competition_distance'] = df1['competition_distance'].apply( lambda x: 100000 if math.isnan(x) else x )

        # competition_open_since_month
        ## Assumption: there are two main reasons that this data is NA: (i) the store doesnt have a near competitor or
        ## (ii) the store has an near competitor, but it the opening data is unknown, either it is older than the store or data is unavailable
        ## What has been done: CONSIDER THE SAME MONTH THAT THE STORE HAS BEEN OPEN (because it maybe older than the store)

        # Error: EDIT Solved
        df1['competition_open_since_month'] = df1.apply( lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1)
        #Alternative: 
        #df1.competition_open_since_month.fillna(df1.date.dt.month, inplace=True)

        # competition_open_since_year
        ## Same ideia from variable above

        #Error: EDIT: Solved
        df1['competition_open_since_year'] = df1.apply( lambda x: x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis=1)
        #Alternative: 
        #df1.competition_open_since_year.fillna(df1.date.dt.month, inplace=True)



        # promo2
        ## Doesnt have any NA

        # promo2_since_week
        ## Assumption: it is possible that the NA values are due to lack of participation/extension of any promotions.
        ## What I think should have been done: ALL NA VALUES ARE CONSIDERED "0", AS THE STORE IS NOT EXTENDING PROMOTIONS
        ## What has actually been done: CONSIDER THE SAME VALUE AS THE DATE
        df1['promo2_since_week'] = df1.apply( lambda x: x['date'].month if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)


        # promo2_since_year
        ## Same logic as above
        df1['promo2_since_year'] = df1.apply( lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)


        # promo_interval
        ## The problem here is that, it is hard to understand the way it has been inserted.
        ## What has been done: (i) Analyze the interval of the promo; (ii) Check if sale month is in promo_interval
        ## if it is, (iii) apply value 1 to new column is_promo, else 0.
        ## This way, it will be easy to check if sale is inside a promotion interval.

        month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec', }

        df1['promo_interval'].fillna(0, inplace=True)
        df1['month_map'] = df1['date'].dt.month.map(month_map)

        df1['is_promo'] = df1[['promo_interval', 'month_map']].apply( lambda x: 0 if x['promo_interval'] == 0 else 1 if x['month_map'] in x['promo_interval'].split(',') else 0, axis=1 )

        df1.isna().sum()


        df1.sample(5).T

        ## 1.6. Change Types

        # Competion and promos since are portrayed as float types, while it should be int type.

        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(int)
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype(int)
        df1['promo2_since_week'] = df1['promo2_since_week'].astype(int)
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(int)
    
        return df1
    
    
    def feature_engineering(self, df2):

        #year
        df2['year'] = df2['date'].dt.year

        #month
        df2['month'] = df2['date'].dt.month

        #day
        df2['day'] = df2['date'].dt.day

        #weekofyear
        df2['week_of_year'] = df2['date'].dt.weekofyear

        #year week
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')

        #competitionsince
        df2['competition_since'] = df2.apply( lambda x: datetime.datetime(year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1), axis=1 )
        df2['competition_time_month'] = ((df2['date'] - df2['competition_since']) / 30).apply(lambda x: x.days).astype(int)

        #promo since
        df2['promo_since'] = df2['promo2_since_year'].astype(str) + '-' + df2['promo2_since_week'].astype(str)
        df2['promo_since'] = df2['promo_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days=7) )
        df2['promo_time_week'] = ((df2['date'] - df2['promo_since']) / 7).apply(lambda x: x.days ).astype(int)

        #assortment
        df2['assortment'] = df2['assortment'].apply( lambda x: 'basic' if x=='a' else 'extra' if x=='b' else 'extended')

        #state holiday
        df2['state_holiday'] = df2['state_holiday'].apply( lambda x: 'public_holiday' if x=='a' else 'easter_holiday' if x=='b' else 'christmas' if x=='c' else 'regular_day')

        # 3.0. VARIABLE FILTERING

        ## 3.1. Line Filtering

        df2 = df2[(df2['open'] != 0)]

        ## 3.2. Column FIltering

        cols_drop = ['open', 'promo_interval', 'month_map']

        df2 = df2.drop(cols_drop, axis = 1)
        
        return df2
    
    def data_preparation(self, df5):

        ## 5.1. Data normalization

        ## 5.2. Data rescaling

        # Before choosing which rescale method will be used, we must know which variables have outliers.
        #sns.boxplot(df5['competition_distance'])

        # competition distance
        df5['competition_distance'] = self.competition_distance_scaler.fit_transform( df5[['competition_distance']].values )

        # competition time month
        df5['competition_time_month'] = self.time_month_scaler.fit_transform( df5[['competition_time_month']].values )

        # year
        df5['year'] = self.year_scaler.fit_transform( df5[['year']].values )

        # promo time week
        df5['promo_time_week'] = self.promo_time_week_scaler.fit_transform( df5[['promo_time_week']].values )

        #sns.distplot(df5['competition_distance'])

        ## 5.3. Data transformation

        ### 5.3.1. Encoding

        #df5.select_dtypes('object')

        # state holiday - One hot encoding
        df5 = pd.get_dummies( df5, prefix=['state_holiday'], columns=['state_holiday'])


        # store type - Label Encoder
        le = LabelEncoder()
        df5['store_type'] = self_encoding_store_type.fit_transform(df5['store_type'])


        # assortment - Ordinal Encoder
        assortment_dict = {'basic':1, 'extra':2, 'extended':3}
        df5['assortment'] = df5['assortment'].map(assortment_dict)


        ### 5.3.1. Nature Transformation

        # day of week
        df5['day_of_week_sin'] = df5['day_of_week'].apply(lambda x: np.sin( x * (2 * np.pi/7)))
        df5['day_of_week_cos'] = df5['day_of_week'].apply(lambda x: np.cos( x * (2 * np.pi/7)))

        # day
        df5['day_sin'] = df5['day'].apply(lambda x: np.sin( x * (2 * np.pi/30)))
        df5['day_cos'] = df5['day'].apply(lambda x: np.cos( x * (2 * np.pi/30)))

        # month
        df5['month_sin'] = df5['month'].apply(lambda x: np.sin( x * (2 * np.pi/12)))
        df5['month_cos'] = df5['month'].apply(lambda x: np.cos( x * (2 * np.pi/12)))

        # week of year
        df5['week_of_year_sin'] = df5['week_of_year'].apply(lambda x: np.sin( x * (2 * np.pi/52)))
        df5['week_of_year_cos'] = df5['week_of_year'].apply(lambda x: np.cos( x * (2 * np.pi/52)))
        
        cols_selected = ['store',
                        'promo',
                        'store_type',
                        'assortment',
                        'competition_distance',
                        'competition_open_since_month',
                        'competition_open_since_year',
                        'promo2',
                        'promo2_since_week',
                        'promo2_since_year',
                        'competition_time_month',
                        'promo_time_week',
                        'day_of_week_sin',
                        'day_of_week_cos',
                        'day_sin',
                        'day_cos',
                        'month_cos',
                        'month_sin',
                        'week_of_year_cos',
                        'week_of_year_sin']
        
        return df5[cols_selected]
    
    
    def get_prediction(self, model, original_data, test_data):
        
        # Prediction
        
        pred = model.predict(test_data)
        
        # Join pred into the original data
        original_data['prediction'] = np.expm1(pred)
        
        return original_data.to_json(orient='records', date_format='iso')
        
