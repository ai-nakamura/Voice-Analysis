import User_Interface
import Frequency_Maker
import Frequency_Player as fp
from time import sleep

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
            float(2/1)    ) # Octave

major_scale = (0, 2, 4, 5, 7, 9, 11, 12)
minor_scale = (0, 2, 3, 5, 7, 8, 10, 12)

prompts = {
    # general
    'initialGreeting': "\nHello, welcome to The Auto Chord Generator app\
                     \nReady to make some music?\n",
    # 'start': "\nPlease choose from the following options:",
    'userInputPrompt': "Please enter your choice, or enter 'Q' to quit: ",

    # menu options -- tuples of phrases to be parsed and presented on new lines to the user
    'menu_chosen': "\nMenu option %s chosen",
    # this is the only part that can't be dynamic
    'menu_start': ("Insert new frequency", "Switch scales", "Change duration", "Play the chords", "2-5-1"),
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


def __main__(tonic, scale, volume=0.5, fs=44100, duration=1.0):
    ui = User_Interface.UI_Interface(prompts)
    fm = Frequency_Maker.Frequency_Maker(tonic, scale, volume, fs, duration)
    # fp = Frequency_Player.Frequency_Player(tonic, scale, volume, fs, duration)

    print(prompts['initialGreeting'])

    # you still work, great
    # for note in fm.chromatic:
    #     sample = fp.sample_maker(note, volume, fs, duration)
    #     fp.stream_player(sample, volume, fs, duration)

    # lamba == like a tiny function, not even important/big enough for a 'def'
    scale_name = lambda: 'minor' if scale == minor_scale else 'major'

    while True:
        # main menu
        print("Current tonic:", tonic)
        print("Current scale: %s\n"% scale_name())
        userChoice_mainMenu = ui.get_user_input(prompts['menu_start'])
        print(prompts['menu_chosen'] % str(userChoice_mainMenu))

        # option 1. New data
        if userChoice_mainMenu == 1:
            tonic = ui.get_user_new_frequency()
            print("New frequency chosen: %s\nSetting new frequency...\n" % tonic)
            fm = Frequency_Maker.Frequency_Maker(tonic, scale, volume, fs, duration)
            # fp = Frequency_Player.Frequency_Player(tonic, scale, volume, fs, duration)

        elif userChoice_mainMenu == 2:
            scale = minor_scale if scale == major_scale else major_scale
            print('Switching scale to %s \n'% scale_name())
            fm.change_scale(scale)

        elif userChoice_mainMenu == 3:
            try:
                new_duration = float(input("How long do you want it? Please don't say something terrible like 10.0 seconds. "))
                if (new_duration < 0):
                    print("Well you're being a negative nancy aren't you.\n")
                    continue
                duration = float(new_duration)
            except:
                print("N")
                sleep(1.0)
                print("o")
                sleep(1.0)
                print("You know what that spells?")
                sleep(1.0)
                print("That's right.")
                sleep(1.0)
                print("No.")
                sleep(1.0)
                print("And now you get to sit there")
                sleep(1.0)
                print("Cuz I TOLD YOU to not do that.")
                sleep(2.0)
                print("hmph\n")

        # option 4: View chords
        elif userChoice_mainMenu == 4:
            print("okie dokes, chordy chord chord")
            user_chord_choice = ui.get_user_input(prompts['menu_chords'][scale])
            print("\nChord chosen:", prompts['menu_chords'][scale][user_chord_choice-1])
            chord_samples = fm.chord_stacker(user_chord_choice-1)
            chord_unison = fm.actual_chord(user_chord_choice-1)
            for note in chord_samples:
                to_play = fp.sample_maker(note, volume, fs, duration)
                fp.stream_player(to_play, volume, fs, duration)
            sleep(duration/2)
            fp.stream_player(chord_unison, volume, fs, duration)

        # option 5: 2-5-1
        elif userChoice_mainMenu == 5:
            # print("2-5-1, got it")
            print(scale)
            two = fm.actual_chord(scale[1])
            five = fm.actual_chord(scale[4])
            one = fm.actual_chord(scale[0])
            fp.stream_player(two, volume, fs, duration)
            fp.stream_player(five, volume, fs, duration)
            fp.stream_player(one, volume, fs, duration)



m = __main__(440, major_scale)

