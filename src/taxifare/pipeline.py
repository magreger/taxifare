import numpy as np
import pandas as pd
import math

def scale_distance(dist):

    """
    Scale the Manhattan distance to a range between 0 and 1.

    The expected distance range is 0 to 100 km.

    Parameters
    ----------
    dist : float or pandas.Series
        Manhattan distance in kilometers.

    Returns
    -------
    float or pandas.Series
        Scaled distance between 0 and 1.

    """

    dist_min = 0
    dist_max = 100
    scaled = (dist - dist_min) / (dist_max - dist_min)
    return scaled

def manhattan_distance_vectorized(df: pd.DataFrame, start_lat: str, start_lon: str, end_lat: str, end_lon: str) -> dict:
    """
    Calculate the Manhattan distance in km between two points on the earth (specified in decimal degrees).
    Vectorized version for pandas df
    """
    earth_radius = 6371

    lat_1_rad, lon_1_rad = np.radians(df[start_lat]), np.radians(df[start_lon])
    lat_2_rad, lon_2_rad = np.radians(df[end_lat]), np.radians(df[end_lon])

    dlon_rad = lon_2_rad - lon_1_rad
    dlat_rad = lat_2_rad - lat_1_rad

    manhattan_rad = np.abs(dlon_rad) + np.abs(dlat_rad)
    manhattan_km = manhattan_rad * earth_radius

    return manhattan_km

def manhattan_distance_for_pipe(df):

    """
    Calculate the Manhattan distance for use in an sklearn pipeline.

    The function uses the pickup and dropoff latitude and longitude
    columns and returns the resulting distance as a DataFrame.
    """

    lonlat_features = ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]
    distance = manhattan_distance_vectorized(df, *lonlat_features)
    return pd.DataFrame({'distance': distance})

def scale_passenger(p):

    """
    Scale the number of passengers to a range between 0 and 1.

    The expected passenger range is 0 to 8.

    Parameters
    ----------
    p : int, float or pandas.Series
        Number of passengers.

    Returns
    -------
    float or pandas.Series
        Scaled passenger count between 0 and 1.
    """

    p_min = 0.
    p_max = 8.
    p_scaled = (p - p_min) / (p_max - p_min)
    return p_scaled

def scale_timedelta(timedelta):

    """
    Scale the time difference to a range between 0 and 1.

    The expected range is 0 to 2190 days, corresponding approximately
    to six years.

    Parameters
    ----------
    timedelta : float or pandas.Series
        Number of days since the reference date.

    Returns
    -------
    float or pandas.Series
        Scaled time difference between 0 and 1.
    """

    timedelta_min = 0
    timedelta_max = 2190
    scaled = (timedelta - timedelta_min) / (timedelta_max - timedelta_min)
    return scaled



def transform_time_features(X: pd.DataFrame) -> pd.DataFrame:

    """
    Extract and transform time-related features from pickup_datetime.

    The pickup timestamp is converted to New York local time. The function
    extracts the day of the week, hour, and month. Hour and month are encoded
    using sine and cosine transformations to represent their cyclical nature.

    In addition, the number of days since January 1, 2009 is calculated.

    Parameters
    ----------
    X : pandas.DataFrame or pandas.Series
        Input data containing a ``pickup_datetime`` column.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the transformed time features:
        ``hour_sin``, ``hour_cos``, ``day_of_week``, ``month_sin``,
        ``month_cos`` and ``timedelta``.
    """

    if isinstance(X, pd.Series):
        X = X.to_frame()

    pickup_dt = pd.to_datetime(X["pickup_datetime"], utc=True)
    timedelta = (pickup_dt - pd.Timestamp('2009-01-01T00:00:00', tz='UTC')) / pd.Timedelta(1, 'D')

    pickup_dt_ny = pickup_dt.dt.tz_convert("America/New_York").dt

    dow = pickup_dt_ny.weekday
    hour = pickup_dt_ny.hour
    month = pickup_dt_ny.month

    hour_sin = np.sin(2 * math.pi / 24 * hour)
    hour_cos = np.cos(2 * math.pi / 24 * hour)

    month_sin = np.sin(2 * math.pi / 12 * month)
    month_cos = np.cos(2 * math.pi / 12 * month)

    return pd.DataFrame({
        'hour_sin': hour_sin,
        'hour_cos': hour_cos,
        'day_of_week': dow,
        'month_sin': month_sin,
        'month_cos': month_cos,
        'timedelta': timedelta
    }, index=X.index)
