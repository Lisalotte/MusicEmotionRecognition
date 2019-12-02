import sys

sys.path.append('./Music-Emotion-Recognition2/')

featEx = __import__('Feature-Extraction')

path = './rs/'

database = featEx.extract_feature(path)
