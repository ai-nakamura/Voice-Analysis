import thinkdsp
import pyaudio
import Record_audio as rec
import wave
import matplotlib.pyplot as plt
import numpy as np
import thinkplot

def voice_analysis_test(filepath):
    f = thinkdsp.read_wave(filepath)
    # spectrum = f.make_spectrum()
    # spectrum.plot() # the squiggly blue line
    # sp = spectrum.peaks()
    fig,ax = plt.subplots()

    # ok, i am currently not recording x=frequency, y=occurrences like ithought i was
    f.make_spectrum().plot(high=2000)
    thinkplot.config(title='Spectrum', xlabel='frequency (Hz)', ylabel='number occurrences')
    thinkplot.show()

    f_spectrogram = f.make_spectrogram(seg_length=1024)
    f_spectrogram.plot(high=2000)
    thinkplot.config(title='Spectrogram', xlabel='frequency (Hz)', ylabel='number occurrences')
    thinkplot.show()

    # start = 3.0
    # duration = 0.4
    # segment = f.segment(start, duration)
    # segment_spectrum = segment.make_spectrum()
    # segment_spectrum.plot()
    # thinkplot.config(title='working title', xlabel='frequency (Hz)', ylabel='number occurrences')
    # thinkplot.show()

voice_analysis_test('audio-files/menu_sleeping_demo.wav')
