# Focus EEG Classifier

This is a classifier for attentive states that uses the Muse portable EEG headset. Given an experimental recording of brain wave data, it will attempt to classify attentive and non-attentive states, and will print live predictions to a terminal.

If you follow the instructions outlined in this document, you can train your own classifier, potentially with far greater accuracy than off-the-shelf algorithms. Some of this process will seem a bit more... involved than I'd like it to be. Interaxon is (purportedly) working on a port for LibMuse to desktop OS', so hopefully I'll be able to correct that soon.

## Dependencies

* *Muse Headset:* This headset is required to interact with the Focus EEG Classifier. In principle, any kind of EEG would work with my methods, but you'd need to coerce the recordings into the right format.

* *Muse SDK:* This will have all the lovely stuff you'll want to run the Muse on OSX. Speaking of which:

* *OSX:* If you fix the paths and get all the dependencies right, you might be able to get this going on Windows or Linux, I just wouldn't know how.

* *pyliblo:* This is needed for the OSC server. Generally, you're going to want to follow the procedures and install the dependencies for everything [here](https://sites.google.com/a/interaxon.ca/muse-developer-site/developer-getting-started-guide).

## General Procedure

From a high level perspective, there are three phases: gathering training data, training and deploying a model, and finally running online predictions. More concretely, you'll be doing the following:

1. Connect Muse and start recording
2. Start labeler script and run experiment
3. Stop Muse and label recordings
4. Run training script to build predictive model
5. Run OSC server to generate predictions on incoming Muse stream

## Instructions

Clone this repo and navigate to its folder in Terminal, then do the following:

1. Connect the Muse and begin recording:
    * Entering <muse-io --device Muse --osc osc.udp://localhost:5001,osc.udp://localhost:5002> into the terminal (minus angle brackets) should work. Make sure ports 5001 and 5002 are available.
    * Ensure proper muse fit and connection strength.
    * This is a long one: paste <muse-player -i /muse/elements/delta_absolute /muse/elements/theta_absolute /muse/elements/alpha_absolute /muse/elements/beta_absolute /muse/elements/is_good /muse/elements/blink /muse/elements/jaw_clench -l udp:5002 -C Recordings/Unlabeled/$(date +%s).csv> and run it. Your streaming EEG data will start recording on a .csv file.
2. Start labeler script and run experiment:
    * Start labeler.py
    * Begin some attention-taxing activity (listen to educational podcasts, Coursera lectures, etc.)
    * Hit a key whenever you notice yourself losing focus.

3. When you're satisfied with your training session, or get too tired to continue, hit ctrl-c to kill the Muse player and Esc to close labeler.py.

4. Run train.py to train a model (this can take a few minutes, depending on the length of your training session).

5. Run OSC server and get predictions:
    * Run classifier_osc_server.py
    * Keep terminal window open
    * Observe focus scores. If you're drifting too much, take a break!

