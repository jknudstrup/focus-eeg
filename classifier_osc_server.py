# import os
# import sys
# #reload(sys)  
# import imp
# imp.reload(sys)
# sys.setdefaultencoding('Cp1252')

from liblo import *
import sys
import time
import pickle
clf = pickle.load( open("model.pkl", "rb" ) ) #choose appro
import numpy as np
import pandas as pd


class MuseServer(ServerThread):
    #listen for messages on port 5001
    def __init__(self):
        self.current_row = False
        ServerThread.__init__(self, 5001)


    @make_method('/muse/elements/alpha_absolute', 'ffff')
    def alpha_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        self.current_row = [l_ear, l_forehead, r_forehead, r_ear]
        pass


    @make_method('/muse/elements/beta_absolute', 'ffff')
    def beta_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        x = [l_ear, l_forehead, r_forehead, r_ear]
        if len(self.current_row) == 4:
            self.current_row += x
        pass


    @make_method('/muse/elements/delta_absolute', 'ffff')
    def delta_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        x = [l_ear, l_forehead, r_forehead, r_ear]
        if len(self.current_row) == 8:
            self.current_row += x
        pass


    @make_method('/muse/elements/theta_absolute', 'ffff')
    def theta_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        x = [l_ear, l_forehead, r_forehead, r_ear]
        if len(self.current_row) == 12:
            self.current_row += x
        assert len(self.current_row) == 16

        #For some godawful reason the following must now be done:
        #self.current_row = np.array(self.current_row).reshape(1, -1)
        #print row #Delete me

        #print self.current_row
        #break #Really delete me

        self.current_row = pd.Series(self.current_row).reshape(1, -1) #Gotta do this now apparently
        #print self.current_row
        #print clf.predict(self.current_row)
        print clf.decision_function(self.current_row)
        condition_names = {1 : "Focused.", 2 : "Zoning Out!", 3 : "Wavering..."}
        # prediction = clf.predict(self.current_row)[0]
        # score = clf.decision_function(self.current_row)[0][0]
        # if (score > -3) and (score < 0): 
        #     prediction = 3
        # name = condition_names[prediction], str(score)

        # if name[0] != "Focused.":
        #     print(name)
        # else:
        #     print(" ")
        #     print(" ")
        self.current_row = False
        pass

    #Handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        pass

try:
    server = MuseServer()
except (ServerError, err):
    print(str(err))
    sys.exit()

server.start()

if __name__ == "__main__":
    #clf = pickle.load( open("model.pkl", "rb" ) ) #choose appropriate filename
    while 1:
        time.sleep(1)
