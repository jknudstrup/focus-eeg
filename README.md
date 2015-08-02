# Focus EEG Classifier

This is a classifier for attentive states that uses the Muse portable EEG headset. Given an experimental recording of brain wave data, it will attempt to classify attentive and non-attentive states, and will print live predictions to a terminal.

If you follow the instructions outlined in this document, you can train your own classifier, potentially with far greater accuracy than off-the-shelf algorithms. Some of this process will seem a bit more... involved than I'd like it to be. Interaxon is (purportedly) working on a port for LibMuse to desktop OS', so hopefully I'll be able to correct that soon.

##Dependencies

* *Muse Headset:* This headset is required to interact with the Focus EEG Classifier. In principle, any kind of EEG would work with my methods, but you'd need to coerce the recordings into the right format.

* *Muse SDK:* This will have all the lovely stuff you'll want to run the Muse on OSX. Speaking of which:

* *OSX:* If you fix the paths and get all the dependencies right, you might be able to get this going on Windows or Linux, I just wouldn't know how.

* *pyliblo:* This is needed for the OSC server. Generally, you're going to want to follow the procedures and install the dependencies for everything [here](https://sites.google.com/a/interaxon.ca/muse-developer-site/developer-getting-started-guide).