import pandas as pd
import pickle
import preprocessing as pr


def prepro_last():
    """Retrieves and preprocesses most recent recording."""
    print("Processing most recent recording...")
    recent_recording = pr.prepare.get_last_brainwaves()
    prep_df = pr.prepare.trim_df(recent_recording)
    rebuilt_df = pr.build_frame.restructure_df(prep_df)
    filtered_df = pr.build_frame.filter_restructure(rebuilt_df)

    return filtered_df


def train_build(df):
    """Makes a training set ready to be fitted."""
    print("Constructing training set...")
    recent_labels = pr.labels.get_last_keypresses()
    labeled_df = pr.labels.apply_labels_all(df, recent_labels)
    X, y = pr.build_model.make_training_set(labeled_df)

    return X, y


def fit_store(X, y):
    """Finds an optimal model, stores it in models folder."""
    print("Fitting model to training set...")
    model = pr.build_model.fit_model(X, y)
    pickle.dump(model, open("models/" + get_most_recent() + ".pkl", "wb"))


def main():
    """Cleans recent training data and fits a model to it."""
    df = prepro_last()
    X, y = train_build(df)
    fit_store(X, y)

if __name__ == "__main__":
    main()
