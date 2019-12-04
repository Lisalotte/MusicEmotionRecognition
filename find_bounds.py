import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

import sys
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

def bounds():
    rows = ['cent','rolloff','rms','zcr','beats','tempo', 'entropy', 'pitch']
    dataentries = ['cent_mean', 'rolloff_mean', 'rmse_mean', 'zcr_mean', 'average_beats', 'tempo', 'entropy', 'pitch']
    columns = ['min','max']
#    data = pd.read_csv('Music-Emotion-Recognition/Emotion_features.csv')
    data = pd.read_csv('Emotion_features_mod.csv')
    minmax = pd.DataFrame(index=rows, columns=columns)

    feature = data.ix[:, 'tempo':]
    features = feature.values

    for i in range(len(rows)):
        minmax['min'][rows[i]] = feature[dataentries[i]].min()
        minmax['max'][rows[i]] = feature[dataentries[i]].max()

    print(minmax)

'''
    rolloff_norm = (np.mean(rolloff))#-3000)/4000
    intensity_var.set_value(id, 0.8*np.mean(rmse) + (1-lowenergy)*0.2)
    timbre_var.set_value(id, 0.2*np.mean(zcr) + 0.4*np.mean(cent)+ 0.3*np.mean(rolloff) + 0.1*np.mean(entropy))
    rhythm_var.set_value(id, 0.4*np.average(beats) + 0.6*tempo)
    pitch_var.set_value(id, np.mean(pitch))

    for i in range(len(features['tempo'])):
'''

def main():
    bounds()
    
if __name__ == "__main__":
    main()