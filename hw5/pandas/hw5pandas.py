import pandas as pd


def load_divvy_data() -> pd.DataFrame:
    """
    Load Dataframe containing ride data from Divvy Bikes for 2023

    Returns:
        pd.DataFrame: Divvy data
    """
    return pd.read_csv("data/divvy_2023_sample_10k.csv")


def load_weather_data() -> pd.DataFrame:
    """
    Load Dataframe containing weather data for Chicago area for 2023

    Returns:
        pd.DataFrame: Weather data
    """
    return pd.read_csv("data/weather_chicago_2023.csv")


def summarize_ride_by_date(divvy_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize Divvy ride data by date. Aggregates ride count and average
    ride duration by date.
    Args:
        divvy_df (pd.DataFrame): Divvy ride data
    Returns:
        pd.DataFrame: Summary of ride data by date. Resulting dataframe
         contains the following index and columns:
            - ride_date: Date of the ride
            - ride_count: Number of rides on that date
    """
    raise NotImplementedError


def merge_rides_and_weather(
    divvy_summary: pd.DataFrame, weather_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge Divvy ride data with chicago weather data by date

    Args:
        divvy_summary (pd.DataFrame): Summary of ride data by date
        weather_data (pd.DataFrame): Weather data
    Returns:
        pd.DataFrame: Merged data
                Resulting dataframe is indexed by ride_date, and contains the
                following columns:
                - ride_count: Number of rides on that date
                - temp_max: Maximum temperature on that date
                - temp_min: Minimum temperature on that date
                - temp_avg: Average temperature on that date
                - temp_departure: Departure from normal temperature on that date

    """
    raise NotImplementedError


def compute_correlation(
    merged_data: pd.DataFrame, variable1: str, variable2: str
) -> float:
    """
    Compute the correlation between two variables in the dataframe

    Args:
        merged_data (pd.DataFrame): Merged data
        variable1 (str): Name of the first variable
        variable2 (str): Name of the second variable

    Returns:
        float: Correlation between the two variables
    """
    raise NotImplementedError


# Bonus Plotting
def plot_visual_correlation(
    merged_data: pd.DataFrame, variable1: str, variable2: str
) -> None:
    """
    Plot the correlation between two variables in the dataframe

    Args:
        merged_data (pd.DataFrame): Merged data
        variable1 (str): Name of the first variable
        variable2 (str): Name of the second variable
    """
    ax = merged_data.plot(y=variable1)
    merged_data.plot(y=variable2, secondary_y=True, ax=ax, rot=90)
