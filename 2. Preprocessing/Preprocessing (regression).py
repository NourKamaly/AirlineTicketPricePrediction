import numpy as np
import pandas as pd
from scipy import stats
import scipy 
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import ast
from scipy.interpolate import make_interp_spline
from sklearn import metrics
import seaborn as sns
from scipy.fft import fft,ifft
import warnings
warnings.filterwarnings("ignore")

dataset = pd.read_csv('Data/airline-price-prediction.csv')
print(dataset.head())

print(np.sum(dataset.duplicated()))

print(dataset.dtypes)

print(np.sum(dataset.isna()))

dataset['formatted_date'] = 0
dataset['source'] = 0
dataset['destination'] = 0
dataset['flight_day'] = 0
dataset['flight_month'] = 0
dataset['num_of_stops'] = 0
dataset['formatted_price'] =0
dataset['num_of_hours_taken'] =0
dataset['week_day_of_flight'] = 0
dataset['distance_bet_2_countries'] = 0
dataset['one_stop_in'] = 'Not Found'

def format_dates():
    observation = 0
    for date in dataset['date']:
        dataset['formatted_date'][observation] = date.replace('/','-')
        observation += 1

def extract_day_month():
    observation = 0
    for date in dataset['formatted_date']:
        format = date.split('-')
        dataset['flight_day'][observation] = int(format[0])
        dataset['flight_month'][observation] =int(format[1])
        if format[1]== '2' or format[1]== '02':
            dataset['formatted_date'][observation] = 'February ' + format[0] + ', '+ format[2]
        else :
            dataset['formatted_date'][observation] = 'March ' + format[0] + ', '+ format[2]
        observation+=1

def extract_weekday():
    observation =0
    dataset['formatted_date'] = pd.to_datetime(dataset['formatted_date'])
    for day in dataset['formatted_date']:
        dataset['week_day_of_flight'][observation]= day.day_name()
        observation +=1

format_dates()
extract_day_month()
extract_weekday()

print(dataset.head())

def split_route():
    observation = 0
    for route in dataset['route']:
        flight = ast.literal_eval(route)
        dataset['source'][observation] = flight['source']
        dataset['destination'][observation] = flight['destination']
        observation +=1

split_route()

def calculate_distance():
    distances = dict()
    distances['Mumbai','Kolkata'] = 2167
    distances['Mumbai','Hyderabad'] = 721
    distances['Mumbai','Chennai'] = 1344
    distances['Mumbai','Bangalore'] = 995
    distances['Mumbai','Delhi'] = 1439
    distances['Delhi','Bangalore'] = 2169
    distances['Delhi','Kolkata'] = 1554
    distances['Delhi','Hyderabad'] = 1579
    distances['Delhi','Chennai'] = 2202
    distances['Bangalore','Kolkata']= 1560
    distances['Bangalore','Hyderabad'] = 569
    distances['Bangalore','Chennai'] = 348
    distances['Kolkata','Hyderabad'] = 1489
    distances['Kolkata','Chennai'] = 1663
    distances['Hyderabad','Chennai'] = 628
    for observation in range(len(dataset['source'])):
        try :
            dist = distances[dataset['destination'][observation],dataset['source'][observation]]
        except :
            dist = distances[dataset['source'][observation],dataset['destination'][observation]]
        dataset['distance_bet_2_countries'][observation]= dist
    dataset['distance_bet_2_countries'] =  dataset['distance_bet_2_countries']/ dataset['distance_bet_2_countries'].max()

calculate_distance()

print(dataset.head())

print(dataset.stop.value_counts())

def split_num_of_stops():
    observation= 0
    for stop in dataset['stop']:
        if stop[:8] == 'non-stop':
            dataset['num_of_stops'][observation] = 0
        elif stop[:6] == '1-stop':
            dataset['num_of_stops'][observation] = 1
        else:
            dataset['num_of_stops'][observation] = 2
        observation+=1

split_num_of_stops()

def find_where_is_the_stop():
    observation = 0
    for stop in dataset['stop']:
        if stop[:6] == '1-stop':
            splitted = stop.split(' ')
            if len(splitted)>1:
                fine_splitting = splitted[1].split('\n')
                dataset['one_stop_in'][observation] = fine_splitting[0]
        observation+=1

find_where_is_the_stop()

print(dataset.one_stop_in.value_counts())

dataset['one_stop_in'] = [0 if stop == 'Not found' else 1 for stop in dataset ['one_stop_in']]

def fix_price_format(price):
    number = price.split(',')
    cost = number[0] + number[1]
    cost=int(cost)
    return cost

dataset['formatted_price'] = dataset.price.apply(lambda price:fix_price_format(price))

print(dataset.shape)

def get_outliers_boundaries():
    first_quartile = np.percentile(dataset['formatted_price'],25)
    third_quartile = np.percentile(dataset['formatted_price'],75)
    interquartile_range = third_quartile - first_quartile
    floor = first_quartile - 1.5 * interquartile_range
    cieling = third_quartile + 1.5 * interquartile_range
    #it doesnt make sense to have a negative price
    if floor < 0:
        floor = 0
    outliers = []
    for observation in range(len(dataset['formatted_price'])):
        if dataset['formatted_price'][observation] < floor or dataset['formatted_price'][observation] > cieling:
            outliers.append(dataset['formatted_price'][observation])
            dataset.drop(observation,axis=0,inplace=True)
    print("The outliers are '{values}'".format(values=outliers))

get_outliers_boundaries()

print(dataset.shape)

print(dataset.airline.value_counts())

print(dataset.ch_code.value_counts())

def calculate_time_taken():
    observation = 0
    for time_taken in dataset['time_taken']:
        time = time_taken.split(' ')
        float_hour = time[0].split('.')
        if(len(float_hour)>1):
            time[0] = float_hour[0] + 'h'
            time[1]= float_hour[1][:-1] + time[1]
        if time[1][:-1] != '' : 
            if int(time[1][:-1]) >= 40 :
                dataset['num_of_hours_taken'][observation] = int(time[0][:-1]) + 1
            else :
                dataset['num_of_hours_taken'][observation] = int(time[0][:-1]) 
        else :
            dataset['num_of_hours_taken'][observation] = int(time[0][:-1])
        observation+=1

calculate_time_taken()

dataset['type'] = [1 if kind_of_trip == 'business' else 0 for kind_of_trip in dataset['type']]

def get_feature_percentage():
    size = dataset.shape[0]
    ctr = 0
    for index in dataset.airline.value_counts().index:
        percentage = (int(dataset.airline.value_counts()[ctr])/size)*100
        print("Airline '{index}' represents '{percentage}' of the data".format(index = index,percentage =percentage))
        ctr += 1

get_feature_percentage()

def remove_low_frequency_airlines():
    high_frequency_airlines =['Vistara','Air India','Indigo']
    dataset ['airline'] = [airline if airline in high_frequency_airlines else 'Other_airline' for airline in dataset['airline']]

remove_low_frequency_airlines()

get_feature_percentage()

def categorize_time(time):
    hours = time.split(':')
    hours[0] = int(hours[0])
    if hours[0] <6:
        return 'Early morning'
    elif 6<= hours[0] < 12 :
        return 'Morning'
    elif 12<= hours[0] < 18:
        return 'Afternoon'
    else:
        return 'Evening'

dataset['dep_time'] = dataset.dep_time.apply(lambda time: categorize_time(time))

dataset['arr_time'] = dataset.arr_time.apply(lambda time: categorize_time(time))

dataset.drop(columns=['date','ch_code','time_taken','stop','route','price','formatted_date','num_code'],axis = 1,inplace=True)

print(dataset.head())

print(dataset.groupby('dep_time')[['formatted_price']].mean())

target_encoded_dataset = dataset.copy()

def arranging_dep_time_by_price(time):
    if time =='Early morning':
        return 1
    elif time == 'Afternoon':
        return 2
    elif time == 'Morning':
        return 3
    else :
        return 4

target_encoded_dataset['dep_time'] = target_encoded_dataset.dep_time.apply(lambda time: arranging_dep_time_by_price(time))

print(dataset.groupby('arr_time')[['formatted_price']].mean())

target_encoded_dataset['arr_time'] = target_encoded_dataset.arr_time.apply(lambda time: arranging_dep_time_by_price(time))

print(dataset.groupby('week_day_of_flight')[['formatted_price']].mean())

def arranging_day_by_price(day):
    if day =='Tuesday' :
        return 1
    elif day =='Thursday' :
        return 2
    elif day =='Wednesday' :
        return 3
    elif day =='Friday' :
        return 4
    elif day =='Monday' :
        return 5
    elif day =='Saturday' :
        return 6
    else :
        return 7

target_encoded_dataset['week_day_of_flight'] = target_encoded_dataset.week_day_of_flight.apply(lambda day: arranging_day_by_price(day))

print(dataset.groupby('airline')[['formatted_price']].mean())

def arranging_airline_by_price(airline):
    if airline == 'Other_airline' :
        return 1
    elif airline == 'Indigo' :
        return 2
    elif airline == 'Air India' :
        return 3
    else :
        return 4

target_encoded_dataset['airline'] = target_encoded_dataset.airline.apply(lambda airline: arranging_airline_by_price(airline))

print(dataset.groupby('source')[['formatted_price']].mean())

def arranging_source_by_price(source):
    if source == 'Delhi' :
        return 1
    elif source == 'Hyderabad' :
        return 2
    elif source == 'Mumbai' :
        return 3
    elif source == 'Bangalore' :
        return 4
    elif source == 'Kolkata' :
        return 5
    else :
        return 6

target_encoded_dataset['source'] = target_encoded_dataset.source.apply(lambda source: arranging_source_by_price(source))

print(dataset.groupby('destination')[['formatted_price']].mean())

def arranging_destination_by_price(source):
    if source == 'Delhi' :
        return 1
    elif source == 'Hyderabad' :
        return 2
    elif source == 'Mumbai' :
        return 3
    elif source == 'Bangalore' :
        return 4
    elif source == 'Chennai' :
        return 5
    else :
        return 6

target_encoded_dataset['destination'] = target_encoded_dataset.destination.apply(lambda destination: arranging_destination_by_price(destination))

print(target_encoded_dataset.head())

target_encoded_dataset.drop(columns=['one_stop_in'],axis=1,inplace=True)

dataset = pd.get_dummies(dataset,columns=['airline','source','destination','week_day_of_flight','dep_time','arr_time'])

dataset.sort_values(by = ['flight_month','flight_day',],inplace =True,kind = 'quicksort',ascending = True)

target_encoded_dataset.sort_values(by = ['flight_month','flight_day',],inplace =True,kind = 'quicksort',ascending = True)

def draw_periodic_signal(dataFrame,condition,grouping_column,condition_column,label):
    df = dataFrame[dataFrame[condition_column]==condition]
    df = df.groupby(grouping_column)[[label]].mean()
    x_values = np.array(df.index)
    y_values = np.array(df[label])
    X_Y_Spline = make_interp_spline(np.array(x_values), y_values)
    X_ = np.linspace(x_values.min(), x_values.max(), 400)
    Y_ = X_Y_Spline(X_)
    plt.plot(X_,Y_)
    plt.show()

draw_periodic_signal(dataset,2,'flight_day','flight_month','formatted_price')

draw_periodic_signal(dataset,3,'flight_day','flight_month','formatted_price')

dataset['formatted_price'][:500].plot(figsize=(24,5))
plt.show()

for column in dataset.columns:
    if column != 'formatted_price':
        corr,pval = stats.pearsonr(dataset[column],dataset['formatted_price'])
        print("'{column}' has correlation of '{corr}' and pvalue of '{pval}'".format(column=column,corr=corr,pval=pval))

for column in dataset.columns:
    if column != 'formatted_price':
        corr,pval = stats.pearsonr(dataset[column],dataset['formatted_price'])
        if pval > 0.05:
            dataset.drop(columns=column,axis=1,inplace=True)

dataset.drop(columns=['one_stop_in'],axis=1,inplace=True)

for column in target_encoded_dataset.columns:
    if column != 'formatted_price':
        corr,pval = stats.pearsonr(target_encoded_dataset[column],target_encoded_dataset['formatted_price'])
        print("'{column}' has correlation of '{corr}' and pvalue of '{pval}'".format(column=column,corr=corr,pval=pval))

for column in target_encoded_dataset.columns:
    if column != 'formatted_price':
        corr,pval = stats.pearsonr(target_encoded_dataset[column],target_encoded_dataset['formatted_price'])
        if pval > 0.05:
            target_encoded_dataset.drop(columns=column,axis=1,inplace=True)

print(dataset.head())

#dataset.to_csv("one_hot_encoded_dataset.csv",index=False)

print(target_encoded_dataset.head())

#target_encoded_dataset.to_csv("target_encoded_dataset.csv",index=False)

frequency = dataset.copy()
frequency.drop(columns=['formatted_price'],axis=1,inplace=True)
freq_domain = scipy.fft.dct(frequency)

freq_domain = pd.DataFrame(data=freq_domain,columns= frequency.columns)

print(freq_domain.head())

#freq_domain.to_csv("frequency_domain_dataset.csv",index=False)



