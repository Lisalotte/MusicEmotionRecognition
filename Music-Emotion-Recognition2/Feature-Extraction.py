import warnings
import numpy as np
from os import listdir
from os.path import isfile, join

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import librosa
    import pandas as pd


'''
    function: extract_features
    input: path to mp3 files
    output: csv file containing features extracted
    
    This function reads the content in a directory and for each mp3 file detected
    reads the file and extracts relevant features using librosa library for audio
    signal processing

'''

def norm(var, varmin, varmax):
    return (var-varmin)/(varmax-varmin)

def extract_feature(path):
    id = 1  # Song ID
    feature_set = pd.DataFrame()  # Feature Matrix
    
    # Individual Feature Vectors
    songname_vector = pd.Series()
    tempo_vector = pd.Series()
    total_beats = pd.Series()
    average_beats = pd.Series()
    rmse_mean = pd.Series()
    rmse_std = pd.Series()
    rmse_var = pd.Series()
    cent_mean = pd.Series()
    cent_std = pd.Series()
    cent_var = pd.Series()
    rolloff_mean = pd.Series()
    rolloff_std = pd.Series()
    rolloff_var = pd.Series()
    zcr_mean = pd.Series()
    zcr_std = pd.Series()
    zcr_var = pd.Series()

    tempo_norm = pd.Series()    
    timbre_var = pd.Series()    
    rhythm_var = pd.Series()    
    pitch_var = pd.Series()
    intensity_var = pd.Series()
    entropy_var = pd.Series()
    
    # Traversing over each file in path
    file_data = [f for f in listdir(path) if isfile (join(path, f))]
    for line in file_data:
        if ( line[-1:] == '\n' ):
            line = line[:-1]

        # Reading Song
        songname = path + line
        y, sr = librosa.load(songname, duration=60)
        S = np.abs(librosa.stft(y))
        
        # Extracting Features
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        #rmse = librosa.util.normalize(rmse,axis=1)
        
        mean = np.mean(rmse[0])
        count = 0
        for rms in rmse[0]:
            if (rms < mean):
                count += 1
        lowenergy = count/len(rmse[0])

        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        entropy = librosa.feature.spectral_flatness(y=y)
        zcr = librosa.feature.zero_crossing_rate(y)  
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        frames_to_time = librosa.frames_to_time(onset_frames[:20], sr=sr)

        pitch = librosa.core.piptrack(y=y, sr=sr)
      
        # Transforming Features
        songname_vector.set_value(id, line)  # song name
        tempo_vector.set_value(id, tempo)  # tempo (beats per minute), middle = 120 bpm
        #tempo_norm.set_value(id, tempo/120.0) 
        total_beats.set_value(id, sum(beats))  # beats
        average_beats.set_value(id, np.average(beats))
        rmse_mean.set_value(id, np.mean(rmse))  # rmse
        rmse_std.set_value(id, np.std(rmse))
        rmse_var.set_value(id, np.var(rmse))
        cent_mean.set_value(id, np.mean(cent))  # cent
        cent_std.set_value(id, np.std(cent))
        cent_var.set_value(id, np.var(cent))
        rolloff_mean.set_value(id, np.mean(rolloff))  # rolloff
        rolloff_std.set_value(id, np.std(rolloff))
        rolloff_var.set_value(id, np.var(rolloff))
        zcr_mean.set_value(id, np.mean(zcr))  # zero crossing rate
        zcr_std.set_value(id, np.std(zcr))
        zcr_var.set_value(id, np.var(zcr))
        entropy_var.set_value(id, np.mean(entropy)) # entropy
        '''
        cent_min = 600
        cent_max = 4000
        cent_norm = norm(np.mean(cent_mean),cent_min,cent_max)
        print(cent_norm)

        rolloff_min = 1000
        rolloff_max = 7100
        rolloff_norm = norm(np.mean(rolloff_mean),rolloff_min,rolloff_max)
        print(rolloff_norm)

        rmse_min = 0.0
        rmse_max = 0.2
        rmse_norm = norm(np.mean(rmse),rmse_min,rmse_max)
        print(rmse_norm)

        zcr_min = 0.0
        zcr_max = 0.3
        zcr_norm = norm(np.mean(zcr_mean),zcr_min,zcr_max)
        print(zcr_norm)

        beats_min = 900
        beats_max = 1700
        beats_norm = norm(np.mean(average_beats),beats_min,beats_max)
        print(beats_norm)

        tempo_min = 40
        tempo_max = 200
        tempo_norm = norm(np.mean(tempo_vector),tempo_min,tempo_max)

        entropy_min = 0.0
        entropy_max = 0.5
        entropy_norm = norm(np.mean(entropy),entropy_min,entropy_max)
        print(entropy_norm)

        pitch_min = 0.0
        pitch_max = 50.0
        pitch_norm = norm(np.mean(pitch),pitch_min,pitch_max)
        '''
        
        intensity_var.set_value(id, 0.8*np.mean(rmse) + (1-lowenergy)*0.2)
        timbre_var.set_value(id, 0.2*np.mean(zcr) + 0.4*np.mean(cent)+ 0.3*np.mean(rolloff) + 0.1*np.mean(entropy))
        rhythm_var.set_value(id, 0.4*np.average(beats) + 0.6*tempo)
        pitch_var.set_value(id, np.mean(pitch))
        '''
        intensity_var.set_value(id, 0.8*rmse_norm + (1-lowenergy)*0.2)
        timbre_var.set_value(id, 0.2*zcr_norm + 0.4*cent_norm+ 0.3*rolloff_norm+ 0.1*entropy_norm)
        rhythm_var.set_value(id, 0.4*beats_norm + 0.6*tempo_norm)
        pitch_var.set_value(id, pitch_norm)
        '''
        print(line)
        id = id+1
    
    intensity_norm = (intensity_var-intensity_var.min())/(intensity_var.max()-intensity_var.min())
    timbre_norm = (timbre_var-timbre_var.min())/(timbre_var.max()-timbre_var.min())
    rhythm_norm = (rhythm_var-rhythm_var.min())/(rhythm_var.max()-rhythm_var.min())
    pitch_norm = (pitch_var-pitch_var.min())/(pitch_var.max()-pitch_var.min())
    entropy_norm = (entropy_var-entropy_var.min())/(entropy_var.max()-entropy_var.min())

    # Concatenating Features into one csv and json format
    feature_set['song_name'] = songname_vector  # song name
    feature_set['class'] = 0

    # Intensity
    feature_set['tempo'] = tempo_vector  # tempo 
    feature_set['total_beats'] = total_beats  # beats
    feature_set['average_beats'] = average_beats

    feature_set['intensity'] = intensity_norm  # root mean squared energy
    feature_set['timbre'] = timbre_norm  # root mean squared energy
    feature_set['rhythm'] = rhythm_norm  # root mean squared energy
    feature_set['entropy'] = entropy_norm
    feature_set['pitch'] = pitch_norm

    feature_set['cent_mean'] = cent_mean
    feature_set['rolloff_mean'] = rolloff_mean
    feature_set['rmse_mean'] = rmse_mean
    feature_set['zcr_mean'] = zcr_mean
    feature_set['average_beats'] = average_beats
    feature_set['tempo'] = tempo_vector

    # Converting Dataframe into CSV Excel and JSON file
    feature_set.to_csv('Emotion_features_mod.csv')
    feature_set.to_json('Emotion_features_mod.json')
