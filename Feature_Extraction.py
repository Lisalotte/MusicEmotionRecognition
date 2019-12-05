import numpy as np
import librosa

class Features:
    tempo = 0 #tempo
    beats = 0 #average beats per frame
    rms = 0 #rms
    cent = 0 #centroid
    rolloff = 0 #rolloff
    zcr = 0 #zcr
    low = 0 #lowenergy
    entropy = 0 #entropy

    def normalize(self, min, max):
        self.tempo = (self.tempo-minmax.tempo_min)/(minmax.tempo_max-minmax.tempo_min)
        self.beats = (self.beats-minmax.beats_min)/(minmax.beats_max-minmax.beats_min)
        self.rms = (self.rms-minmax.rms_min)/(minmax.rms_max-minmax.rms_min)
        self.cent = (self.cent-minmax.cent_min)/(minmax.cent_max-minmax.cent_min)
        self.rolloff = (self.rolloff-minmax.rolloff_min)/(minmax.rolloff_max-minmax.rolloff_min)
        self.zcr = (self.zcr-minmax.zcr_min)/(minmax.zcr_max-minmax.zcr_min)
        self.low = (self.low-minmax.low_min)/(minmax.low_max-minmax.low_min)
        self.entropy = (self.entropy-minmax.entropy_min)/(minmax.entropy_max-minmax.entropy_min)

    def classify(self):        
        energy = 0.8*self.rmse + (1-self.low)*0.2
        timbre = 0.2*self.zcr + 0.4*self.cent+ 0.3*self.rolloff + 0.1*self.entropy
        rhythm = 0.4*self.beats + 0.6*self.tempo

        if energy < 0.5: #low energy
            if (0.7*timbre + 0.3*rhythm < 0.5): 
                emotionClass = 'contentment' #2 (+/-)
            else:
                emotionClass = 'depression' #3  (-/-)
            stress = 0.7*timbre + 0.3*rhythm
        else:
            if (0.3*timbre + 0.7*rhythm < 0.5): 
                emotionClass = 'exuberance' #1 (+/+)
            else:
                emotionClass = 'frantic' #4 (-/+)
            stress = 0.3*timbre + 0.7*rhythm
        
        return (energy, stress)

class MinMax:
    tempo_min = 0
    tempo_max = 0
    beats_min = 0
    beats_max = 0
    rms_min = 0
    rms_max = 0
    cent_min = 0
    cent_max = 0
    rolloff_min = 0
    rolloff_max = 0
    zcr_min = 0
    zcr_max = 0
    low_min = 0
    low_max = 0
    entropy_min = 0
    entropy_max = 0

def norm(var, varmin, varmax):
    return (var-varmin)/(varmax-varmin)

def extract_features(songname):
    features = Features()
   
    y, sr = librosa.load(songname, duration=60)
    #TODO check if song already in database

    # Extracting Features
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    
    mean = np.mean(rmse[0])
    count = 0
    for rms in rmse[0]:
        if (rms < mean):
            count += 1
    lowenergy = float(count)/float(len(rmse[0]))

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    entropy = librosa.feature.spectral_flatness(y=y)
    zcr = librosa.feature.zero_crossing_rate(y)  
    pitch = librosa.core.piptrack(y=y, sr=sr)
    
    # Add Features to class
    features.tempo = tempo  # tempo (beats per minute), middle = 120 bpm
    features.beats = np.average(beats)
    features.rms = np.mean(rmse)
    features.cent = np.mean(cent)
    features.rolloff = np.mean(rolloff)
    features.zcr = np.var(rolloff)
    features.low = lowenergy
    features.entropy = np.mean(entropy)

    return features


def main():
    features = extract_features('/home/lisa/Documents/MMS/rs_test/Arrival.mp3')
    print(features.__dict__)
    
if __name__ == "__main__":
    main()
    