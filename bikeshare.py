import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    city = input('which city would you like to see data chicago,washington or new_york_city?').lower()
    while city not in (CITY_DATA .keys()):
        print('which city would you like to see data chicago,washington or new_york_city?')
        city= input('Enter city name?').lower()

    filter= input('Would you like to filter data by month,day,or all?').lower()
    while filter not in (['month','day','all']):
        print('incorrect filter')
        filter= input('Would you like to filter data by month,day,or all?').lower()

    months =['january','february','march','april','may','june']
    if filter == 'month' or filter == 'all' :
        month = input('which month: January,February,March,April,May,June?').lower()
        while month not in months :
            print('incorrect month')
            month = input('which month: January,February,March,April,May,June?').lower()
    else:
        month = 'all'

    days =['monday','tuesday','wednsday','thursday','friday','saturday','sunday']
    if filter == 'day' or filter == 'all' :
       day = input('which day:Monday,Tuesday,Wednsday,Thursday,Friday,Sunday ?').lower()
       while day not in days :
            print('incorrect day')
            day = input('which day:Monday,Tuesday,Wednsday,Thursday,Friday,Sunday ?').lower()
    else:
         day  = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    print('\nCalculatin The Most Frequent Times of Travel ...\n')
    start_time = time.time()
    print(df.month.mode()[0])
    print(df.day_of_week.mode()[0])
    df['hour']= df['Start Time'].dt.hour
    print(df['hour'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(df):
    print('\nCalculating The Most Popular Station and Trip...\n')
    start_time = time.time()
    common_start = df['Start Station'].mode()[0]
    print(common_start)
    common_end = df['End Station'].mode()[0]
    print(common_end)
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print( common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel = df['Trip Duration'].sum()
    print(total_travel)
    mean_travel = df['Trip Duration'].mean()
    print(mean_travel)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    print(user_types)
    print(df.columns)
    if 'Gender'in df.columns.values.tolist():
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print("NOT APPLICABLE ON THIS CITY.")

    if 'Birth Year'in df.columns.values.tolist():
        earliest = df['Birth Year'].min()
        print(earliest)
        recent = df['Birth Year'].max()
        print(recent)
        common_birth = df['Birth Year'].mode()[0]
        print(common_birth)
    else:
        print("NOT APPLICABLE ON THIS CITY.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
   while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        n = 0
        while True :
            entry= input("Do you want to print raw data?").lower()
            if entry  == "yes" :
                print (df.iloc[n:n+5])
                n += 5
            elif entry == "no":
                break

        print(df.head())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	    main()
