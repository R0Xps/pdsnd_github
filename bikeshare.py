import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, or washington).
    while True:
        city = input('Which city would you like to see data for? Chicago, New York City, or Washington? Please type the city name as shown here.\n').strip().lower()
        if city in CITY_DATA:
            break
        print('Sorry I couldn\'t find that city in the list, please try again.')

    print(f'Looks like you want to know about {city.title()}! If that\'s not the case, please exit or restart the program now.\n')

    # get user input for which filters to use (month, day, both, or none).
    while True:
        filters = input('Would you like to filter the data by month, day, both, or nothing at all? Type \'none\' for no time filters.\n').strip().lower()
        if filters in ('month', 'day', 'both', 'none'):
            break
        print('Sorry I couldn\'t understand that, please try again.')

    filter_by_month = filters in ('month', 'both')
    filter_by_day = filters in ('day', 'both')

    # get user input for month (january, february, ... , june)
    month = 'all'
    while filter_by_month:
        month = input('Which month? January, February, March, April, May, or June? Please type out the full name of the month.\n').strip().lower()
        if month in MONTHS:
            break
        print('Sorry, that month either doesn\'t exist, or we have no data available for it.')

    # get user input for day of week (sunday, monday, ..., saturday)
    day = 'all'
    while filter_by_day:
        day = input('Which day of the week? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? Please type out the full name of the day.\n')
        if day in DAYS:
            break
        print('Sorry I couldn\'t understand that, please try again.')

    print('-' * 40)
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

    # add column with both starting and ending stations
    df['start_end_stations'] = 'Starting station: ' + df['Start Station'] + ', Ending station: ' + df['End Station']

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # check whether to filter by month or not
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # check whether to filter by day of the week or not
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = df['month'].mode()[0]
    print(f'Most common month: {month_mode}')
    
    # display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print(f'Most common day of the week: {day_mode}')
    
    # display the most common start hour
    hour_mode = df['hour'].mode()[0]
    print(f'Most common start hour: {hour_mode}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_st_mode = df['Start Station'].mode()[0]
    print(f'Most popular starting station: {start_st_mode}')
    
    # display most commonly used end station
    end_st_mode = df['End Station'].mode()[0]
    print(f'Most popular ending station: {end_st_mode}')
    
    # display most frequent combination of start station and end station trip
    trip_mode = df['start_end_stations'].mode()[0]
    print(f'Most popular trip (starting and ending stations):\n{trip_mode}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate and display total travel time
    total_travel_seconds = df['Trip Duration'].sum()
    total_travel_timedelta = pd.Timedelta(f'{total_travel_seconds} seconds')
    print(f'Total travel time: {total_travel_timedelta}')

    # calculate and display mean travel time
    mean_travel_seconds = df['Trip Duration'].mean()
    mean_travel_timedelta = pd.Timedelta(f'{mean_travel_seconds} seconds')
    print(f'Mean travel time for a trip: {mean_travel_timedelta}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('User type breakdown:\n', user_type_counts)
    print()

    # Display counts of gender
    try:
        user_gender_counts = df['Gender'].value_counts()
        print('User gender breakdown:\n', user_gender_counts)
    except KeyError:
        print('No gender data to share.')
    print()

    # Display earliest, most recent, and most common year of birth
    try:
        oldest_birth_year = int(df['Birth Year'].min())
        youngest_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f'Oldest birth year: {oldest_birth_year}')
        print(f'Youngest birth year: {youngest_birth_year}')
        print(f'Most common birth year: {most_common_birth_year}')
    except KeyError:
        print('No birth year data to share.')
    print()
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def get_yes_no_choice(message):
    while True:
        choice = input(message).strip().lower()
        if choice in ('yes', 'no'):
            return choice
        print(f'Invalid choice ({choice}). Please try again')


def raw_data(df):
    """Displays the raw data of the file 5 rows at a time"""
    
    choice = get_yes_no_choice('Would you like to see the raw data? yes/no\n')
    rows = df.shape[0]
    curr_row = 0
    
    while choice == 'yes' and curr_row < rows:
        print(df[curr_row : curr_row + 5])
        curr_row += 5
        choice = get_yes_no_choice('Would you like to see 5 more rows of the raw data? yes/no\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = get_yes_no_choice('\nWould you like to restart? Enter yes or no.\n')
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()