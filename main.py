import sys

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
sys.path.append('./Music-Emotion-Recognition/')

featEx = __import__('Feature-Extraction')

path = './rs/'

database = featEx.extract_feature(path)
