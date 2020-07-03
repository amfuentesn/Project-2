import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chile': 'chile.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chile, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = input("Choice one of three cities: chile, new york city or washington ")
    city = city.lower()
    while city != 'chile' and city != 'new york city' and city != 'washington':
        city = input("Choice a correct city: chile, new york city or washington ")
        city = city.lower()

    # get user input for month (all, january, february, ... , june)
    
    month = input("Choice a month name (all, january, february, ... , june): ")
    month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("Choice a day of week (all, monday, ... , sunday): ")
    day = day.lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    popular_month = df['month'].mode()[0]
    print('The Most Common month:',  popular_month)

    # display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('The Most Common day:',  popular_day)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]    
    print('The most commonly used start station: ' + popular_start_station )

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: ' + popular_end_station)
    
    # display most frequent combination of start station and end station trip

    popular_startend_station = (df['Start Station']+df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station trip: ' + popular_startend_station )
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    df['dif time']= (df['End Time']-df['Start Time'])
    df['dif time sec']=df['dif time'].dt.seconds
    total_travel_time= np.sum(df['dif time sec'])
    print('The total travel time: ' , total_travel_time)

    # display mean travel time

    mean_travel_time= np.mean(df['dif time sec'])
    print('The mean travel time' , mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    count_user_type=df['User Type'].value_counts()
    print ('The counts of user type: ',count_user_type)

    # Display counts of gender

    if 'Gender' in df.columns:
        counts_gender= df['Gender'].value_counts()
        print ('The Counts of gender: ',counts_gender)
    else:
        print ("The city doesn't have this information")

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        earliest_year_of_birth = np.min(df['Birth Year'])
        print ('Earliest year of birth: ' , earliest_year_of_birth)
        most_recent_year_of_birth= df['Birth Year'].values[0]
        print ('Most recent year of birth: ' , most_recent_year_of_birth)
        most_common_year_of_birth = df['Birth Year'].mode()[0]  
        print ('Most common year of birth: ' , most_common_year_of_birth)
    else:
        print ("The city doesn't have year of birth")
        
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()