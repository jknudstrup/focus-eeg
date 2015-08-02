import pandas as pd
from collections import defaultdict
import settings

def build_sigframes(ddict, df):
    """
    From the original dataframe, new signal sub-frames are created
    and stored in the provided defaultdict.
    """
    for ind, element in enumerate(settings.SIGNALS):
        key = settings.SIG_FRAMES[ind]
        val = df[df['Element'] == element].copy()
        if element != settings.FIRST_ELEMENT:  # Preserve timestamps
            val.drop(['Timestamp', 'Element'], axis=1, inplace=True)
        else:
            val.drop(['Element'], axis=1, inplace=True)
        val.index = range(val.shape[0])
        if key == 'good':
            val.columns = ['good0', 'good1', 'good2', 'good3']
        ddict[key] = val


def build_condframes(ddict, df):
    """
    From the original dataframe, new conditional sub-frames are created
    and stored in the provided defaultdict.
    """
    for ind, element in enumerate(settings.CONDITIONS):
        key = settings.CONDFRAMES[ind]
        val = df[df['Element'] == element].copy()
        val.drop(['Timestamp', 'Element', 'Left Forehead', 'Right Forehead',
                  'Right Ear'], axis=1, inplace=True)
        val.columns = [key]
        val.index = range(val.shape[0])
        ddict[key] = val


def combine_frames(ddict):
    """
    Takes in a defaultdict of sub-frames, combines them into one dataframe,
    and returns it.
    """
    combined_df = ddict['alpha']  # Initialize to make concat easier

    for sig in settings.SIG_FRAMES[1:]:
        d = ddict[sig]
        combined_df = pd.concat([combined_df, d], axis=1)

    for cond in settings.CONDFRAMES:
        d = ddict[cond]
        combined_df = pd.concat([combined_df, d], axis=1)

    return combined_df


def restructure_df(df):
    """
    Builds and returns a new dataframe with rows that are composites of the
    desired signals. The new row has the timestamp of the first element,
    regardless of the actual timestamps the following signals previously had.
    """
    sig_dict = defaultdict()

    # Build up signal dictionary
    build_sigframes(sig_dict, df)
    build_condframes(sig_dict, df)

    return combine_frames(sig_dict)


def filter_restructure(df):
    """
    Takes in data frame, drops rows if user was blinking, clenching jaw,
    or if there's a problem with electrode contact. Then drops the filter
    criterion rows and returns the new, filtered dataframe.
    """
    combined_df = df.copy()

    for noise in ['blink', 'jaw']:
        combined_df = combined_df[combined_df[noise] != 1]
    for fit in ['good0', 'good1', 'good2', 'good3']:
        combined_df = combined_df[combined_df[fit] == 1]

    filtered_df = combined_df.drop(['good1', 'good2', 'good3', 'good0', 'jaw',
                                    'blink'], axis=1)
    # Rebuild index
    filtered_df.index = range(filtered_df.shape[0])

    return filtered_df
