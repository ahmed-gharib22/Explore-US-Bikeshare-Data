import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Here is the user input for the city (chicago, new york city, washington)
    while True:
      citices = ['chicago', 'new york', 'washington']
      city =input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
      if city.strip() in citices:    
         break
      else:
        print("Please enter one of the cities listed!")

    # Here is the user input for the month (all, january, february, ... , june)     
    while True:
        months = ['all',  'january', 'february', 'march', 'april', 'may', 'june'] 
        month = input("Which month? All,  January, February, March, April, May, or June?\n").lower()
        if month.strip() in months:  
         break
        else:
          print("Please enter one of the months listed!") 
        
    # Here is the user input for the day of the week (all, monday, tuesday, ... sunday)       
    while True:
        days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = input("Which day? All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday?\n").lower()
        if day.strip() in days:   
           break
        else:
           print("Please enter one of the days listed!")
       
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day_of_Week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
    # filter by month to create the new dataframe
     df = df[df['Month'] == month.title()]
    
    # filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
      df = df[df['Day_of_Week'] == day.title()]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # Here is the most common month
    most_common_month = df['Month'].mode()[0]
    print('most common month:', most_common_month)
    
    # Here is the most common day of week
    most_common_day = df['Day_of_Week'].mode()[0]
    print('most common day of week:', most_common_day)
    
    # Here is the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Hour'].mode()[0]
    print('most common hour of day:', most_common_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    start_time = time.time()

    # Here is the most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print('most common start station:', most_commonly_used_start_station)
    
    # Here is the most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    print('most common end station:', most_commonly_used_end_station)
    
    # Here is the most frequent combination of start station and end station trip
    df['Trip'] = ' From ' + df['Start Station'] + ' To ' + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print('most common trip from start to end:', most_common_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    
    start_time = time.time()

    # Here is the total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("total trip duration is: ", total_travel_time)
    
    # Here is the average travel time
    average_travel_time = df['Trip Duration'].mean()
    print("average trip duration is: ", average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    
    start_time = time.time()

    # Here are counts of user types
    user_types = df['User Type'].value_counts()
    print('counts of user types is:\n', user_types)
    
    # Here are counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('counts of gender is:\n', gender)
    except KeyError:
     print('Gender Data is not Available for Washington')
    
    # Here is the earliest, most recent, and most common year of birth
    try:
        oldest_year = df['Birth Year'].min()
        latest_year = df['Birth Year'].max()
        most_common_year_birth = df['Birth Year'].mode()[0]
        print("earliest year of birth is: {}\nmost recent year of birth is: {}\nmost common year of birth is: {}".format(oldest_year, latest_year, most_common_year_birth))
    except KeyError:
     print('Year of Birth Data is not Available for Washington')     
  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    print('\nRaw data is available to check... \n')
    
    # Here is a view of the available raw data in chunks of 5 rows type
    display_raw = input('To view the available raw data in chunks of 5 rows type: Yes or No.\n').lower()
    while display_raw not in ('yes', 'no'):
        print('That is invalid input, please enter your selection again')
        display_raw = input('To view the available raw data in chunks of 5 rows type: Yes or No.\n').lower()
   
    while display_raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], index_col = 0 ,chunksize=5):
                print(chunk)
                display_raw = input('To view the available raw data in chunks of 5 rows type: Yes.\n').lower()
                if display_raw != 'yes':
                    print('Thank You')
                    break
            break

        except KeyboardInterrupt:
            print('Thank you.')

def main():
    while True:
        city, month, day = get_filters()
        print("City: {}, Month: {}, Day: {}\n".format(city, month, day))
        df = load_data(city, month, day)
        print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()