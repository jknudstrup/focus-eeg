import os
import pandas as pd
import settings


def get_most_recent():
    """Returns string of filename of most recent brain wave recording."""
    wave_logs = os.listdir(settings.WAVE_PATH)
    most_recent = max(wave_logs)
    return most_recent


def get_last_brainwaves():
    """
    Retrieve most recent brain wave recording and return it as a dataframe.
    Assumes filenames are prepended
    with Unix timestamps.
    """
    most_recent = get_most_recent()
    wave_filename = settings.WAVE_PATH + most_recent
    waves_df = pd.read_csv(wave_filename)
    waves_df.columns = ["Timestamp", "Element", 'Left Ear', 'Left Forehead',
                        'Right Forehead', 'Right Ear']
    return waves_df


# Dropping from tail (to get even amounts of each element):
def trim_tail(df):
    """Return original dataframe, after dropping unwanted tail rows."""
    for ind, element in reversed(list(enumerate(df['Element']))):
        if element == settings.LAST_ELEMENT:
            break
        else:
            df.drop(ind, inplace=True)

    return df


# Trimming away initial entries
def trim_head(df):
    """
    Like trim_tail, but removes unwanted entries from the front of
    a dataframe.
    """
    for ind, element in enumerate(df['Element']):
        if element == settings.FIRST_ELEMENT:
            break
        else:
            df.drop(ind, inplace=True)

    return df


def trim_df(df):
    """Trims head and tail away from a df and returns a copy of the df."""
    trimmed_tail = trim_tail(df)
    trimmed = trim_head(trimmed_tail)

    return trimmed.copy()
