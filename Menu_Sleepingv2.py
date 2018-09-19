
import thinkdsp
import pyaudio
from Record_audio import *
import wave
import math
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
'''
Notes:

http://nbviewer.jupyter.org/github/AllenDowney/ThinkDSP/blob/master/code/scipy2015_demo.ipynb

'''
# ----- Music -------------------------------------------------------------------------------------------------------- #

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
            float(2/1)  ) # Octave

major_scale = (0, 2, 4, 5, 7, 9, 11, 12)
minor_scale = (0, 2, 3, 5, 7, 8, 10, 12)

# ----- Prompts ------------------------------------------------------------------------------------------------------ #

prompts = {
    # general
    'initialGreeting': "\nHello, welcome to The Voice feminization app\
                        \nReady to make some music?\n",

    'userInputPrompt': "Please enter your choice, or enter 'Q' to quit: ",

    # menu options -- tuples of phrases to be parsed and presented on new lines to the user
    'menu_start': ("Re-record (change base note)",
                   "Play Recording",
                   "Play Scale", # do I even need this?
                   "Run practice round", # play either "Hi!" at 'mi' or "Hello!" at 'so-la // or M3 up and
                   # practice exercise could be a 'repeat after me' thing where one note is played and user copies it
                   # chromatic? Scale?
                   "2-5-1",
                   "stats",
                   "about"), # "Hello" would be 'so-la'
    'menu_chosen': "\nMenu option %s chosen",
    'menu_new_frequency': ("Alright, what's the new frequency you want? Pick something between 220.0 and 1000.0: ",
                           "Setting new frequency..."),
    'menu_chords' : {major_scale: ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'],
                     minor_scale: ['i', 'ii°', 'III', 'iv', 'v(natural)', 'VI', 'VII']
                     },

    # quit
    'quit_validate': "\nAre you sure you want to quit? Enter Y to quit or any other key to stay: ",
    'quit_confirm': ("Have a lovely day. Remember to treat yourself nicely today.",
                     "See ya later alligator! Always remember that you matter.",
                     "In a while crocodile! You're awesome just the way you are!",
                     "Thanks for spending time with me",
                     "Okie dokes. Remember, you're worth it",
                     "Tataa baby, and Hakuna Matata!",
                     "Alright then. Take care of yourself now, you hear?",
                     "Bye bye. Be a good experience.",
                     "See ya. Don't forget to be strong in the real way!"),
    'quit_deny': "Glad to have you back!\n",

    # error
    'error_numOutOfRange': "\nThis option is not available.",
    'error_notChar': "\nThis is not a character.",
    'error_notNum': "\nThis is not a number.",
    'error_construction': "Sorry, this area is under construction.\n",
}

# -------------------------------------------------------------------------------------------------------------------- #

def __main__(tonic, scale, volume=0.5, fs=44100, duration=1.0):
    filePathName = 'audio-files/menu_sleeping_v2_demo.wav'
    begin(filePathName)
    # __analyze_spectrum()

'''
Runs at the start of the program to make the user record something to start.
Records a base, generates scale slightly above it, plays both back to user
'''
def begin(filePathName):
    # pre-start: reassurance
    reassurance = ( "this is where reassurance will go.",
                    "because you are loved, and things are hard.",
                    "I'm here for you.",
                    "\n",
                    "Please make sure you're somewhere quiet",
                    "Earphones with a microphone in it works the best!"
                    "\n")
    # for r in reassurance:
    #     print (r)
    #     sleep(1.0)

    # First, record the bottom

    print ("round 1")
    sample_width1, data1 = record()
    # data1 = pack('<' + ('h'*len(data)), *data)

    print ("ok, round 2")
    sample_width2, data2 = record()
    # data2 = pack('<' + ('h' * len(data)), *data)

    print ("ok num 3")
    sample_width3, data3 = record()
    # data3 = pack('<' + ('h' * len(data)), *data)

    print ("Done")
    samp_avg = ((sample_width1+sample_width2+sample_width3)/3)

    # i need to figure out how to match up the lengths of the array before I figure out what I'm doing here

    data_avg = [(d1 + d2 + d3)/3 for d1, d2, d3 in zip(data1, data2, data3)]

    # data_set = (data1, data2, data3)
    # data_length = max(data1.__len__(), data2.__len__(), data3.__len__())

    # data_avg = ((np.array(data1) + np.array(data2) + np.array(data3))/3)

    # pack it into audio file, then play it back
    data_avg = pack('<' + ('h' * len(data_avg)), *data_avg)

    wf = wave.open(filePathName, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(samp_avg)
    wf.setframerate(RATE)
    wf.writeframes(data_avg)
    wf.close()

    # Second, record the upper range


    # loop recording
    redo = 1
    while redo:
        #play back recording
        play_recording(filePathName)
        # choice to rerecord -- check for 'Y' or 'N'
        choice = input("Redo? Type in 'Y' for yes or 'N' for no: ")
        if not choice.isalpha():
            print("Yo I said a letter.\n")
        else:
            if not choice.upper() == 'Y' and not choice.upper() =='N':
                print ("This isn't the right letter.\n")
            elif choice.upper() == 'Y':
                record_tonic()
            # else: continue
            else:
                print("cool.\n")
                redo = 0

    return None

def record_tonic(filepath):
    print ("let's record a new sound\n")
    record_tonic_instructions = ("let's record a new sample")
    record_to_file(filepath)
    print ("great, done!\n")

'''
Plays back the recording.
Assumes the recording already exists.
taken from: https://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python
'''
def play_recording(filePathName):
    print ("here's how it sounds\n")
    sleep(2.0)

    # define stream chunk
    chunk = 1024

    # open a wav format music
    f = wave.open(filePathName, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

        # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()

def __analyze_spectrum(filePathName):
    f = thinkdsp.read_wave(filePathName)
    spectrum = f.make_spectrum()
    spectrum.plot()
    sp = spectrum.peaks()
    # print (sp[:5])
    # print (sp.__len__())
    __show_graph(sp)
    # I'm sure I can write this bit below more pythonically'
    # sum0, sum1 = 0, 0
    # for x in sp:
    #     sum0 += x[0]
    #     sum1 += x[1]
    # print ("cumulative sum: %i, %i" % (sum0, sum1))
    # print ("averages: %f, %f" % (sum0/sp.__len__(), sum1/sp.__len__()))

    print ("__analyze_spectrum complete")

def __show_graph(tuple):
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # This sets up a blank graph
    fig, ax = plt.subplot()
    ax.plot('Hz', 'Frequency', tuple)
    # ax.plot(, '-o', ms=20, lw=2, alpha=0.7, mfc='orange')
    ax.grid()

    # position bottom right
    # fig.text(0.95, 0.05, 'Property of MPL',
    #          fontsize=50, color='gray',
    #          ha='right', va='bottom', alpha=0.5)

    plt.show()

def play_scale():
    return None

def practice_round():
    return None

def two_five_one():
    return None

def current_stats():
    return None

__main__(440, 'major')

