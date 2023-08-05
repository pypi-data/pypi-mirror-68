import numpy as np

__all__ = ['freqs_to_normalized_radians',
           'normalized_radians_to_freqs']

def freqs_to_normalized_radians(freqs, fs):

    return freqs / fs * 2 * np.pi

def normalized_radians_to_freqs(w, fs):

    return w / np.pi * fs / 2