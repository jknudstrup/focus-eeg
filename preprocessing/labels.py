import os
import pandas as pd
import settings


def get_last_keypresses():
    """
    Returns a list of all keypress logs generated since the most recent
    training session.
    """
    wave_logs = os.listdir(settings.WAVE_PATH)
    most_recent = max(wave_logs)

    label_logs = os.listdir(settings.LABELS_PATH)
    recent_labels = [label for label in label_logs if label > most_recent]
    return recent_labels


def focus_label(timestamp, df):
    """Changes label to passed-in data frame"""
    focus_interval = [timestamp, timestamp + 3]
    times = df['Timestamp']
    label_interval = (times > focus_interval[0]) & (times < focus_interval[1])
    df.loc[label_interval, 'Label'] = 1


def distraction_label(timestamp, df):
    """Changes label to passed-in data frame"""
    dist_interval = [timestamp - 8, timestamp - 5]
    times = df['Timestamp']
    label_interval = (times > dist_interval[0]) & (times < dist_interval[1])
    df.loc[label_interval, 'Label'] = 2


def apply_labels_attn(recording_df, label_df):
    """Changes labels on brain wave recording,
    based on label dataframe for a single label file."""
    # Initialize Labels column

    label_times = label_df['Timestamp']  # Timestamps for keypresses

    first_time = label_times[0]  # First keypress will only indicate focus
    focus_label(first_time, recording_df)

    for time in label_times[1:]:
        focus_label(time, recording_df)
        distraction_label(time, recording_df)


def apply_labels_all(filtered_df, labels):
    """
    Label appropriate rows based on keypress timestamps,
    returning new dataframe.
    """
    labeled_df = filtered_df.copy()
    labeled_df['Label'] = 0

    for label_csv in labels:
        label_df = pd.read_csv(settings.LABELS_PATH + label_csv)
        if len(label_df) > 0:
            apply_labels_attn(labeled_df, label_df)

    return labeled_df
