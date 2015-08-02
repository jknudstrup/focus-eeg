# File Paths
WAVE_PATH = "Recordings/Unlabeled/"
LABELS_PATH = "Recordings/Labels/"
CLEANED_PATH = 'Recordings/Cleaned/'

# Each row of the final frame will start with the first and end with the last:
FIRST_ELEMENT = ' /muse/elements/alpha_absolute'
LAST_ELEMENT = ' /muse/elements/jaw_clench'

# Build lists to check
SIGNALS = [" /muse/elements/alpha_absolute",
           " /muse/elements/beta_absolute",
           " /muse/elements/delta_absolute",
           " /muse/elements/theta_absolute",
           " /muse/elements/is_good"]
SIG_FRAMES = ['alpha', 'beta', 'delta', 'theta', 'good']

CONDITIONS = [" /muse/elements/jaw_clench", " /muse/elements/blink"]
CONDFRAMES = ['jaw', 'blink']
