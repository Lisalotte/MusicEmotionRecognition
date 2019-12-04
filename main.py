import sys
import Classification

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
sys.path.append('./Music-Emotion-Recognition2/')
featEx = __import__('Feature-Extraction')

path = './rs_test/'

database = featEx.extract_feature(path)
#Classification.classify()

# TODO
# Volume normalizeren
# Stress as omdraaien x
# Fixed bounds
