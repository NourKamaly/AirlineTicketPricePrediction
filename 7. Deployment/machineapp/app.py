from flask import Flask, render_template,request
import joblib
import pandas as pd
from datetime import datetime
import numpy as np
import pandas as pd
import warnings
import joblib
from datetime import datetime
warnings.filterwarnings("ignore")


app = Flask(__name__)

dataset=0

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

stringsource=''
stringdestination=''
@app.route('/predict',methods=['GET'])
def predict():
    date=request.args.get('date')
    Airline=request.args.get('Airline')
    departuretime=request.args.get('departuretime')
    takentime=request.args.get('takentime')
    stops=request.args.get('stops')
    arrivaltime=request.args.get('arrivaltime')
    type=request.args.get('type')
    source=request.args.get('source')
    destination=request.args.get('destination')
    stringsource=str(source)
    stringdestination=str(destination)
    if(stringsource=='Mumbai'):
        if(stringdestination=='Kolkata' or stringdestination=='Hyderabad'or stringdestination=='Chennai' or stringdestination=='Bangalore' or stringdestination=='Delhi'):
            validatSourceDestination=0
        else:
             validatSourceDestination=1
    
    if(stringsource=='Delhi'):
        if(stringdestination=='Bangalore' or stringdestination=='Kolkata'or stringdestination=='Hyderabad' or stringdestination=='Chennai'):
              validatSourceDestination=0
        else:
             validatSourceDestination=1
    
    
    if(stringsource=='Bangalore'):
        if(stringdestination=='Kolkata' or stringdestination=='Hyderabad'or stringdestination=='Chennai'):
             validatSourceDestination=0
        else:
             validatSourceDestination=1

    if(stringsource=='Kolkata'):
        if(stringdestination=='Hyderabad' or stringdestination=='Chennai'):
            validatSourceDestination=0
        else:
             validatSourceDestination=1
    
    if(stringsource=='Hyderabad'):
        if(stringdestination=='Chennai'):
           validatSourceDestination=0
        else:
            validatSourceDestination=1
    
    if(validatSourceDestination==1):
        return render_template('index.html',validatSourceDestination=validatSourceDestination)
    
    data={'date': date, 'airline':Airline,'dep_time':departuretime,'time_taken':takentime,'stop': stops ,'arr_time':arrivaltime,'type':type,
    'source': source, 'destination': destination}
    dataset = pd.DataFrame(data, index=[0])
    validatSourceDestination=-1
    print(str(departuretime))
    proccesseddate=preprossesing(dataset,stringsource,stringdestination)
    model=joblib.load('DecisionTreeT.h5')
    price=model.predict(proccesseddate)[0]
    return render_template('index.html',price=price)


def preprossesing(dataset,stringsource,stringdestination):
    dataset['full_information_timestamp'] = 0
    dataset['flight_day'] = 0
    dataset['flight_month'] = 0
    dataset['week_day_of_flight'] = 0
    dataset['departure_time_of_the_day']=0
    dataset['arrival_time_of_the_day']=0
    dataset['num_of_hours_taken'] =0
    dataset['num_of_stops'] = 0
    dataset['source'] = 0
    dataset['destination'] = 0
    dataset['distance_between_2_cities'] = 0

    def format_date(date):
        dashed_date = date.replace('/','-')
        return dashed_date

    dataset['full_information_timestamp'] = dataset.date.apply(lambda date:format_date(date))

    def extract_day_month(date):
        splitted_date = date.split('-')
        day = int(splitted_date[0])
        month =int(splitted_date[1])
        if splitted_date[1]== '2' or splitted_date[1]== '02':
            new_date_format = 'February ' + splitted_date[0] + ', '+ splitted_date[2]
        else :
            new_date_format = 'March ' + splitted_date[0] + ', '+ splitted_date[2]
        return day,month,new_date_format

    dataset[['flight_day', 'flight_month','full_information_timestamp']] = pd.DataFrame(dataset.full_information_timestamp.apply(lambda date: extract_day_month(date)).tolist(), index=dataset.index)

    dataset['full_information_timestamp'] = pd.to_datetime(dataset['full_information_timestamp'])

    def extract_weekday(day):
        return day.day_name()

    dataset['week_day_of_flight'] = dataset.full_information_timestamp.apply(lambda date:extract_weekday(date))

    def remove_low_frequency_airlines():
        high_frequency_airlines =['Vistara','Air India','Indigo']
        dataset ['airline'] = [airline if airline in high_frequency_airlines else 'Other_airline' for airline in dataset['airline']]

    remove_low_frequency_airlines()

    def calculate_time_taken(time_taken):
        time = time_taken.split(' ')
        float_hour = time[0].split('.')
        hours = 0
        if(len(float_hour)>1):
            time[0] = float_hour[0] + 'h'
            time[1]= float_hour[1][:-1] + time[1]
        if time[1][:-1] != '' : 
            if int(time[1][:-1]) >= 40 :
                hours = int(time[0][:-1]) + 1
            else :
                hours = int(time[0][:-1]) 
        else :
            hours = int(time[0][:-1])
        return hours

    dataset['num_of_hours_taken'] = dataset.time_taken.apply(lambda time_taken: calculate_time_taken(time_taken))

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

    def split_num_of_stops(stop):
        if stop[:8] == 'non-stop':
            stop_count = 0
        elif stop[:6] == '1-stop':
            stop_count = 1
        else:
            stop_count = 2
        return stop_count

    dataset['num_of_stops']= dataset.stop.apply(lambda stop:split_num_of_stops(stop))

    dataset['type'] = [1 if kind_of_trip == 'business' else 0 for kind_of_trip in dataset['type']]

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

    def calculate_distance(source,destination):
        try :
            dist = distances[source,destination]
        except :
            dist = distances[destination,source]
        return dist
    
    print(stringsource)
    print(stringdestination)
    dataset['distance_between_2_cities'] = distances[stringsource,stringdestination]
    dataset['distance_between_2_cities'] = dataset['distance_between_2_cities']/2202


    def one_hot_encode_time(time):
        morning =0
        afternoon =0
        evening = 0
        early_morning = 0
        if time =='Early morning':
            early_morning = 1
        elif time == 'Afternoon':
            afternoon =1
        elif time == 'Morning':
            morning = 1
        elif time == 'Evening' :
            evening = 1
        return early_morning,morning,afternoon,evening

    dataset[['dep_time_Early morning', 'dep_time_Morning','dep_time_Afternoon','dep_time_Evening']] = pd.DataFrame(dataset.dep_time.apply(lambda time: one_hot_encode_time(time)).tolist(), index=dataset.index)

    dataset[['arr_time_Early morning', 'arr_time_Morning','arr_time_Afternoon','arr_time_Evening']] = pd.DataFrame(dataset.arr_time.apply(lambda time: one_hot_encode_time(time)).tolist(), index=dataset.index)

    def one_hot_encode_week_day(day):
        sunday = 0
        saturday = 0
        thursday = 0
        tuesday = 0
        if day =='Tuesday' :
            tuesday = 1
        elif day =='Thursday' :
            thursday = 1
        elif day =='Saturday' :
            saturday = 1
        elif day == 'Sunday' :
            sunday = 1
        return saturday,sunday,tuesday,thursday

    dataset[['week_day_of_flight_Saturday', 'week_day_of_flight_Sunday','week_day_of_flight_Tuesday','week_day_of_flight_Thursday']] = pd.DataFrame(dataset.week_day_of_flight.apply(lambda day: one_hot_encode_week_day(day)).tolist(), index=dataset.index)

    def one_hot_encode_airline(airline):
        vistara = 0
        indigo = 0
        air_india = 0
        other = 0
        if airline == 'Vistara' :
            vistara = 1
        elif airline == 'Indigo' :
            indigo = 1
        elif airline == 'Air India' :
            air_india = 1
        elif airline =='Other_airline' :
            other = 1
        return vistara,air_india,indigo,other

    dataset[['airline_Vistara', 'airline_Air India','airline_Indigo','airline_Other_airline']] = pd.DataFrame(dataset.airline.apply(lambda airline: one_hot_encode_airline(airline)).tolist(), index=dataset.index)

    def one_hot_encode_city(city):
        delhi = 0
        hyderabad = 0
        mumbai = 0
        bangalore = 0
        kolkata = 0
        chennai =0
        if city == 'Delhi' :
            delhi = 1
        elif city == 'Hyderabad' :
            hyderabad =1
        elif city == 'Mumbai' :
            mumbai = 1
        elif city == 'Bangalore' :
            bangalore = 1
        elif city == 'Kolkata' :
            kolkata = 1
        elif city == 'Chennai' :
            chennai = 1
        return delhi,hyderabad,mumbai,bangalore,kolkata,chennai

    dataset[['source_Delhi','source_Hyderabad', 'source_Mumbai','source_Bangalore','source_Kolkata','source_Chennai']] = pd.DataFrame(dataset.source.apply(lambda city: one_hot_encode_city(city)).tolist(), index=dataset.index)

    dataset[['destination_Delhi','destination_Hyderabad', 'destination_Mumbai','destination_Bangalore','destination_Kolkata','destination_Chennai']] = pd.DataFrame(dataset.destination.apply(lambda city: one_hot_encode_city(city)).tolist(), index=dataset.index)

    features = ['type', 'flight_month', 'num_of_stops',
        'distance_between_2_cities', 'airline_Air India',
        'airline_Indigo', 'airline_Other_airline', 'airline_Vistara',
        'source_Bangalore', 'source_Chennai', 'source_Delhi',
        'source_Hyderabad', 'source_Kolkata', 'source_Mumbai',
        'destination_Bangalore', 'destination_Chennai', 'destination_Delhi',
        'destination_Hyderabad', 'destination_Kolkata', 'destination_Mumbai',
        'week_day_of_flight_Saturday', 'week_day_of_flight_Sunday',
        'week_day_of_flight_Thursday', 'week_day_of_flight_Tuesday',
        'dep_time_Afternoon', 'dep_time_Early morning', 'dep_time_Evening',
        'dep_time_Morning', 'arr_time_Afternoon', 'arr_time_Early morning',
        'arr_time_Evening', 'arr_time_Morning']

    for column in dataset.columns:
        if column not in features:
            dataset.drop(columns=column,axis=1,inplace=True)

    dataset = dataset[['type', 'flight_month', 'num_of_stops',
       'distance_between_2_cities', 'airline_Air India',
       'airline_Indigo', 'airline_Other_airline', 'airline_Vistara',
       'source_Bangalore', 'source_Chennai', 'source_Delhi',
       'source_Hyderabad', 'source_Kolkata', 'source_Mumbai',
       'destination_Bangalore', 'destination_Chennai', 'destination_Delhi',
       'destination_Hyderabad', 'destination_Kolkata', 'destination_Mumbai',
       'week_day_of_flight_Saturday', 'week_day_of_flight_Sunday',
       'week_day_of_flight_Thursday', 'week_day_of_flight_Tuesday',
       'dep_time_Afternoon', 'dep_time_Early morning', 'dep_time_Evening',
       'dep_time_Morning', 'arr_time_Afternoon', 'arr_time_Early morning',
       'arr_time_Evening', 'arr_time_Morning']]
            
    return dataset
    
if __name__=='__main__':
    app.run(debug=True)




