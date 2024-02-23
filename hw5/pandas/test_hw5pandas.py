import pytest
import pandas as pd
import os

from hw5pandas import (
    load_divvy_data,
    load_weather_data,
    summarize_ride_by_date,
    merge_rides_and_weather,
    compute_correlation
)

def test_task3_load_divvy_data() -> None:
    assert os.path.exists('data/divvy_2023_sample_10k.csv')
    trips = load_divvy_data()
    assert trips.shape == (10000, 13)
    assert trips.columns.tolist() == ['ride_id', 'rideable_type', 'started_at', 'ended_at', 'start_station_name', 'start_station_id', 'end_station_name', 'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng', 'member_casual']

def test_task3_load_weather_data() -> None:
    assert os.path.exists('data/weather_chicago_2023.csv')
    weather = load_weather_data()
    assert weather.shape == (365, 10)
    assert weather.columns.tolist() == ["calendar_date","temp_max","temp_min",
                                        "temp_avg","temp_departure","hdd","cdd",
                                        "percpitation","new_snow","snow_depth"]
    
def test_task3_summarize_ride_by_date_stub() -> None:
    # Create a sample DataFrame for testing
    divvy_df = pd.DataFrame({
        'started_at': ['2022-01-01 10:00:00', '2022-01-01 11:00:00', '2022-01-02 09:00:00'],
        'ended_at': ['2022-01-01 10:30:00', '2022-01-01 11:30:00', '2022-01-02 09:30:00'],
        'ride_id': [1, 2, 3]
    })

    # Call the function to get the summarized ride data
    ride_dates = summarize_ride_by_date(divvy_df)

    # Assert the expected output
    expected_output = pd.DataFrame({
        'ride_date': ['2022-01-01', '2022-01-02'],
        'ride_count': [2, 1],
    })
    pd.testing.assert_frame_equal(ride_dates, expected_output)

def test_task3_summarize_ride_by_date() -> None:
    divvy_df = pd.read_csv('data/divvy_2023_sample_10k.csv')

    ride_dates = summarize_ride_by_date(divvy_df)

    assert ride_dates.shape == (365, 2)
    assert ride_dates.columns.tolist() == ['ride_date', 'ride_count']
    assert ride_dates['ride_date'].nunique() == 365
    assert ride_dates['ride_count'].sum() == 10000

    # Check the first and last dates

    assert ride_dates['ride_date'].iloc[0] == '2023-01-01'
    assert ride_dates['ride_date'].iloc[1] == '2023-01-02'
    assert ride_dates['ride_date'].iloc[-1] == '2023-12-31'
    assert ride_dates['ride_date'].iloc[-2] == '2023-12-30'
    assert ride_dates['ride_count'].iloc[0] == 6
    assert ride_dates['ride_count'].iloc[1] == 12
    assert ride_dates['ride_count'].iloc[-1] == 5
    assert ride_dates['ride_count'].iloc[-2] == 7

    # Check average ride count
    assert ride_dates['ride_count'].mean() == pytest.approx(27.397260)

def test_task4_merge_rides_and_weather_stub() -> None:
    # Create a sample divvy_summary DataFrame
    divvy_summary = pd.DataFrame({
        'ride_date': ['2022-01-01', '2022-01-02'],
        'ride_count': [2, 1],
    })

    # Create a sample weather_data DataFrame
    weather_data = pd.DataFrame({
        'calendar_date': ['2022-01-01', '2022-01-02'],
        'temp_max': [32, 28],
        'temp_min': [20, 18],
        'temp_avg': [26, 23],
        'temp_departure': [2, -5]
    })

    # Call the function to merge the data
    merged_data = merge_rides_and_weather(divvy_summary, weather_data)

    # Assert the expected output
    expected_output = pd.DataFrame({
        'ride_count': [2, 1],
        'temp_max': [32, 28],
        'temp_min': [20, 18],
        'temp_avg': [26, 23],
        'temp_departure': [2, -5]
    }, index=pd.Index(['2022-01-01', '2022-01-02'], name='ride_date'))
    pd.testing.assert_frame_equal(merged_data, expected_output)


def test_task4_merge_rides_and_weather() -> None:
    divvy_df = pd.read_csv('data/divvy_2023_sample_10k.csv')
    weather_df = pd.read_csv('data/weather_chicago_2023.csv')
    
    ride_dates = summarize_ride_by_date(divvy_df)
    merged_data = merge_rides_and_weather(ride_dates, weather_df)

    assert merged_data.shape == (365, 5)
    assert merged_data.columns.tolist() == ['ride_count', 'temp_max', 'temp_min', 'temp_avg', 'temp_departure']
    assert merged_data.index.nunique() == 365
    
    #Spot check the index
    assert merged_data.index.name == 'ride_date'
    assert merged_data.index[0] == '2023-01-01'
    assert merged_data.index[1] == '2023-01-02'
    assert merged_data.index[-1] == '2023-12-31'
    assert merged_data.index[-2] == '2023-12-30'

    # Check the ride counts and temperature values
    assert merged_data['ride_count'].iloc[0] == 6
    assert merged_data['temp_max'].iloc[0] == 45
    assert merged_data['temp_min'].iloc[0] == 37
    assert merged_data['temp_avg'].iloc[0] == pytest.approx(41.0)
    assert merged_data['temp_departure'].iloc[0] == pytest.approx(14.2)

    assert merged_data['ride_count'].iloc[1] == 12
    assert merged_data['temp_max'].iloc[1] == 43
    assert merged_data['temp_min'].iloc[1] == 32
    assert merged_data['temp_avg'].iloc[1] == pytest.approx(37.5)
    assert merged_data['temp_departure'].iloc[1] == pytest.approx(10.8)


    assert merged_data['ride_count'].iloc[-2] == 7
    assert merged_data['temp_max'].iloc[-2] == 37
    assert merged_data['temp_min'].iloc[-2] == 27
    assert merged_data['temp_avg'].iloc[-2] == pytest.approx(32.0)
    assert merged_data['temp_departure'].iloc[-2] == pytest.approx(4.8)

    assert merged_data['ride_count'].iloc[-1] == 5
    assert merged_data['temp_max'].iloc[-1] == 36
    assert merged_data['temp_min'].iloc[-1] == 31
    assert merged_data['temp_avg'].iloc[-1] == pytest.approx(33.5)
    assert merged_data['temp_departure'].iloc[-1] == pytest.approx(6.5)    


    assert merged_data['ride_count'].sum() == 10000
    assert merged_data['temp_avg'].mean() == pytest.approx(54.138356)
    assert merged_data['temp_max'].mean() == pytest.approx(62.482192)
    assert merged_data['temp_min'].mean() == pytest.approx(45.794521)
    assert merged_data['temp_departure'].mean() == pytest.approx(2.758904)




def test_task5_compute_correlation_stub() -> None:
    # Create a sample merged_data DataFrame
    merged_data = pd.DataFrame({
        'ride_count': [2, 1, 3, 4],
        'temp_max': [32, 28, 30, 35],
        'temp_min': [20, 18, 22, 25],
        'temp_avg': [26, 23, 25, 30],
        'temp_departure': [2, -5, 0, 3]
    })

    # Call the function to compute the correlation
    correlation = compute_correlation(merged_data, 'ride_count', 'temp_max')

    # Assert the expected output
    expected_output = 0.8214416322175221
    assert correlation == pytest.approx(expected_output)


def test_task5_compute_correlation() -> None:
    divvy_df = pd.read_csv('data/divvy_2023_sample_10k.csv')
    weather_df = pd.read_csv('data/weather_chicago_2023.csv')
    
    ride_dates = summarize_ride_by_date(divvy_df)
    merged_data = merge_rides_and_weather(ride_dates, weather_df)

    correlation = compute_correlation(merged_data, 'ride_count', 'temp_avg')
    assert correlation == pytest.approx(0.8199028410413619)

