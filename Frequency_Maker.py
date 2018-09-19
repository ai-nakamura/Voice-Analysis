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
major_intervals = (0, 2, 4, 5, 7, 9, 11, 12)
minor_intervals = (0, 2, 3, 5, 7, 8, 10, 12)

import Frequency_Player as fp

class Frequency_Maker():

    def __init__(self, tonic, scale, volume=0.5, fs=44100, duration=2.0):
        self.tonic = tonic
        self.scale = scale
        self.volume = volume
        self.fs = fs
        self.duration = duration
        self.chromatic = self.chromatic_scale()


    # --- setters ---------------------------------------------------------------- #
    def change_tonic(self, new_tonic):
        self.tonic = new_tonic
        # self.fp = Frequency_Player(new_tonic, self.scale)

    def change_scale(self, new_scale):
        self.scale = new_scale
        # self.fp = Frequency_Player(self.tonic, new_scale)

    # --- generate frequencies ---------------------------------------------------- #
    '''
    Generate the chromatic scale frequencies
    '''
    def chromatic_scale(self):
        chromatic_frequencies = []
        for r in ratios:
            chromatic_frequencies.append(self.tonic * r)
        return chromatic_frequencies

    '''
    determines the frequencies of the desired chord.
    Returns: list of frequencies -- root one octave below, triad calculated within range, and an octave above the last note of the triad
    '''
    def chord_stacker(self, chord_tonic):
        stack = []
        # octave below
        octave_below = self.chromatic[self.scale[chord_tonic]]/2.0
        stack.append(octave_below)

        # triad
        for x in range(3):
            # scale_index = picks up every other note from the chord_tonic
            # scale_index = chord_tonic + (0*2), chord_tonic + (1*2), chord_tonic(2*2)
            scale_index = chord_tonic + (x*2)
            # multiplier = 1
            # if the scale_index is out of range of self.scale, mod scale_index to within the range
            # then multiply given freq by 2 to send it up an octave
            if (scale_index) > (len(self.scale) - 1):
                scale_index %= (len(self.scale) - 1)
                # multiplier = 2
            # get proper index to pull out from chromatic scale
            chromatic_index = self.scale[scale_index]
            stack.append(self.chromatic[chromatic_index]) # * multiplier)

        # octave above
        octave_above = self.chromatic[self.scale[chord_tonic]]*2
        stack.append(octave_above)

        return stack


        # play the chord in unison
    def actual_chord(self, chord):
        chord_stack = self.chord_stacker(chord)
        unison = fp.sample_maker(chord_stack[0], self.volume, self.fs, self.duration)
        for x in chord_stack[1:]:
            unison += fp.sample_maker(x, self.volume, self.fs, self.duration)
        # self.__stream_player(unison)
        return unison


'''
e = Engine(440, major_intervals)
# e.chord_player(2)
# e.chord_player(5)
# e.chord_player(1)

e.stack_player(2)
e.stack_player(5)
e.stack_player(1)

e.change_tonic(440+20)
e.change_scale(minor_intervals)

e.stack_player(2)
e.stack_player(5)
e.stack_player(1)
'''

