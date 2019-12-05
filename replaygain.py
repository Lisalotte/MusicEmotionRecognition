#! /bin/env python

import ctypes
from ctypes import c_float, CDLL

replaygain = CDLL("libreplaygain.so")

# parse arguments
# gather files
# group into albums
# calculate gains
def analyze(sample_gen):
    """
    pass in a generator that produces audio samples
    returns the maximum sample
    """
    max_bucket = 1000
    max_sample = 0
    sample_bucket_left = []
    sample_bucket_right = []
    sample_count = 0
    for left, right in sample_gen:
        max_sample = max(max_sample, left, right)
        sample_bucket_left.append(left)
        sample_bucket_right.append(right)
        sample_count = sample_count + 1
        if sample_count == max_bucket:
            left = (c_float * max_bucket)(*sample_bucket_left)
            right = (c_float * max_bucket)(*sample_bucket_right)
            replaygain.gain_analyze_samples(left, right, max_bucket, 2)
            sample_bucket_left = []
            sample_bucket_right = []
            sample_count = 0

    if sample_count:
        left = (c_float * sample_count)(*sample_bucket_left)
        right = (c_float * sample_count)(*sample_bucket_right)
        replaygain.gain_analyze_samples(left, right, sample_count, 2)

    return max_sample

# apply tags

import random

replaygain.gain_init_analysis(44100)
ms = analyze(([random.random(), random.random()] for i in range(44100 * 60 * 3)))
print("Peak value %f" % (ms,))
print("Recommended gain: %f dB" % replaygain.gain_get_chapter())