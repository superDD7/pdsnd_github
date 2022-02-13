import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ("January", "February", 'March', 'April', 'May', 'June')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze within washington NY and Chicago
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    day = 1
    month = "January"

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New york, or Washington? ").lower()
    # loop for correct result
    while city != 'chicago' and city != 'new york' and city != 'washington':
        print("Invalid argument ! try again")
        city = input("Would you like to see data for chicago, new York, or washington? ").lower()

    #get user input for filter (day, month or both). with while loop
    filter = input("Would you like to filter the data by month, day, both ?").lower()
    while filter != 'day' and filter != 'month' and filter != 'both':
        print('Invalid argument ! try again')
        filter = input("Would you like to filter the data by month, day, both ?").lower()

    #get user filter by month
    if filter == "both" or filter == "month":
        while True:
            month = input("Which month ? January, February, March, April, May, June ? ")
            if month in month_list:
                break

    #get user filter by day
    if filter == "both" or filter == "day":
        while True:
            try:
                day = int(input("Which day? please type your response as an integer "))
                if day < 30:
                    break
            except ValueError:
                print("type an integer between 1 to 30")

    print('-'*40)
    return city, month, day, filter


def load_data(city, month, day, filter):
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day
    df['hour'] = df['Start Time'].dt.hour

    #select filter
    if filter == "both":
        # filter by day of week to create the new dataframe
        df = df[(df["month"] == month) & (df['day_of_week'] == day)]

    if filter == "month":
        # use the index of the months list to get the corresponding int
        df = df[df["month"] == month]

    if filter == "day":
        # use the index of the months list to get the corresponding int
        df = df[df["day_of_week"] == day]
        
    return df


def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common start hour
    popular_hour = df["hour"].value_counts().index.tolist()[0]
    
    # display the count of the most common hour
    count_hour = df["hour"].value_counts()[popular_hour]

    # print the result
    print("Most popular hour:{} \ncount:{} \nfilter by {}".format(popular_hour, count_hour, filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    best_start_station = df["Start Station"].value_counts().index.tolist()[0]

    # display most commonly used end station
    best_end_station = df["End Station"].value_counts().index.tolist()[0]

    # display most frequent combination of start station and end station trip
    best_combination_start = df[["Start Station", "End Station"]].value_counts().index.tolist()[0]

    print("The most commonly: \nstart station: {} \nend station: {}\n".format(best_start_station, best_end_station))
    print("The most frequent combination of station: {}".format(best_combination_start))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df["Trip Duration"].sum()

    # display mean travel time
    avg_duration = df["Trip Duration"].mean()

    # display result
    print("Total Duration:{} \nAvg Duration:{}".format(total_duration, avg_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df["User Type"].value_counts()

    if 'Gender' in df:
        # Only access Gender column in this case
        gender_counts = df["Gender"].value_counts()
        print("The count of user types: \n{},\n \ncounts of Gender: \n{} ".format(user_types, gender_counts))
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
   
    # Display earliest, most recent, and most common year of birth
    if 'Birth' in df:
        # Only access Birth column in this case
        earliest = df["Birth Year"].min()
        most_recent = df["Birth Year"].max()
        common_year = df["Birth Year"].value_counts().index.tolist()[0]
        print("\nYear of birth: \nearliest: {} \nmost recent: {} \nmost common: {}".format(earliest, most_recent, common_year))
    else:
        print('Birth stats cannot be calculated because Gender does not appear in the dataframe')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    x = 0
    y = 5
    while True:
        raw_answer = input("Do you want to see 5 lines of raw data ? yes or no  ").lower()
        if raw_answer == 'yes':
            print(df[x:y])
            x += 5
            y += 5
        else : 
            break
            
def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day, filter)

        time_stats(df, filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
