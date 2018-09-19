'''

Generates the whole stack of chords to go with the fundamental frequency using the Chromatic scale.

'''

import pyaudio
import numpy as np
'''
# Chromatic ratios taken from: http://fundamentals-of-piano-practice.readthedocs.io/en/latest/chapter2/CH2.2.html
ratios = (  float(1/1),     # Unison
            float(16/15),   # minor second
            float(9/8),     # Major second
            float(6/5),     # minor third
            float(5/4),     # Major third
            float(4/3),     # Perfect fourth
            float(25/18),   # Tritone
            float(3/2),     # Perfect fifth
            float(8/5),     # minor sixth
            float(5/3),     # Major sixth
            float(9/5),     # minor seventh
            float(15/8),    # Major seventh
            float(2/1)      # Octave
         )
major_scale = (0, 2, 4, 5, 7, 9, 11, 12)
minor_scale = (0, 2, 3, 5, 7, 8, 10, 12)

class Frequency_Player:
    def __init__(self, tonic, scale, volume=0.5, fs=44100, duration=5.0):
        self.tonic = tonic
        self.scale = scale
        # self.chromatic_frequency = self.chromatic_scale()
        self.volume = volume
        self.fs = fs
        self.duration = duration




    # determines the frequencies of the desired chord.
    # Returns: list of frequencies -- root one octave below, triad calculated within range, and an octave above the last note of the triad

    # def chord_stacker(self, chord_tonic):
    #     stack = []
    #     # octave below
    #     octave_below = self.chromatic_frequency[self.scale[chord_tonic-1]]/2.0
    #     stack.append(octave_below)
    #
    #     # triad
    #     for x in range(3):
    #         # scale_index = picks up every other note from the chord_tonic
    #         # scale_index = chord_tonic + (0*2), chord_tonic + (1*2), chord_tonic(2*2)
    #         scale_index = chord_tonic-1 + (x*2)
    #         # multiplier = 1
    #         # if the scale_index is out of range of self.scale, mod scale_index to within the range, then multiply given freq by 2 to send it up an octave
    #         if (scale_index) > (len(self.scale) - 1):
    #             scale_index %= (len(self.scale) - 1)
    #             # multiplier = 2
    #         # get proper index to pull out from chromatic scale
    #         chromatic_index = self.scale[scale_index]
    #         stack.append(self.chromatic_frequency[chromatic_index] * multiplier)
    #
    #     # octave above
    #     octave_above = self.chromatic_frequency[self.scale[chord_tonic-1]]*2
    #     stack.append(octave_above)
    #
    #     return stack
    '''
'''
Makes a numpy.ndarray for a sine wave of the given frequency 
'''
def sample_maker(frequency, volume, fs=44100, duration=5.0):
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)
    return samples * volume

def stream_player(samples,volume, fs=44100, duration=5.0):
    p = pyaudio.PyAudio()
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively)
    stream.write(volume * samples)

    stream.stop_stream()
    stream.close()

    p.terminate()


# if __name__ == '__main__':
#     # TODO: do the thing; engine!
#     cg = Chord_Generator(440, major_scale)
#     print (cg.chord_stacker(6))