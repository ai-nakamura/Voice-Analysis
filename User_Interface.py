
from random import randint

class UI_Interface:

    def __init__(self, prompts):
        self.prompts = prompts
        print("UI_Interface")



    # def UI_engine(self):
        # print(self.prompts['initialGreeting'])
        #
        # while True:
        #     # main menu
        #     userChoice_mainMenu = self.get_user_input(self.prompts['menu_start'])
        #     print(self.prompts['menu_chosen'] % str(userChoice_mainMenu))
        #
        #     # option 1. Insert/Update new data
        #     if userChoice_mainMenu == 1:
        #         print("alright, new frequency time")
        #
        #     # option 2: View data
        #     elif userChoice_mainMenu == 2:
        #         print("okie dokes, chordy chord chord")


    # TODO: split off 'except' area into a different method so I don't have to raise stupid errors
    def get_user_input(self, menu_prompt):
        queryChoice = -1
        # run indefinitely until a proper choice is made
        while queryChoice < 0:
            try:
                # print(self.prompts['start'])
                for index in range(0, len(menu_prompt)):
                    print("%s. " % (index + 1) + menu_prompt[index])
                choice = (input(self.prompts['userInputPrompt']))

                # Check if user wants to end program
                if choice.upper() == 'Q':
                    raise IOError

                # Determine if the user given choice if within the range of menu_prompt given.
                else:
                    queryChoice = int(choice)
                    if type(menu_prompt) == int:
                        max_range = menu_prompt
                    else:
                        max_range = len(menu_prompt)
                    if queryChoice > max_range or queryChoice <= 0:
                        raise TypeError

            except(IOError):
                # Runs when the user wants to quit. Prompts the user to confirm to quit
                q = str(input(self.prompts['quit_validate']))
                if q.upper() == 'Y':
                    quit_num = randint(0, len(self.prompts['quit_confirm']) - 1)
                    print(self.prompts['quit_confirm'][quit_num])
                    raise SystemExit
                else:
                    print(self.prompts['quit_deny'])
            except(TypeError):
                queryChoice = -1
                print(self.prompts['error_numOutOfRange'])
            except:
                print(self.prompts['error_notNum'])

            else:
                if queryChoice > 0: break

        # returns the user's choice as the number from the menu (will be index + 1)
        return (queryChoice)



    def get_user_new_frequency(self, ):
        user_new_frequency = 0.0
        print(self.prompts['menu_new_frequency'][0])
        while True:
            # print(self.prompts['menu_new_frequency'][0])
            user_new_frequency = input()
            try:

                # user wants to quit
                if user_new_frequency.upper() == 'Q':
                    raise IOError

                elif (float(user_new_frequency) < 220.0) or (float(user_new_frequency) > 1000.0):
                    print("I SAID pick something between 100.0 and 15000.0")
                    continue

            except(ValueError):
                print("Excuse me, I need a number, punk ")
                continue

            # user wants to quit
            except(IOError):
                # Runs when the user wants to quit. Prompts the user to confirm to quit
                q = str(input(self.prompts['quit_validate']))
                if q.upper() == 'Y':
                    quit_num = randint(0, len(self.prompts['quit_confirm']) - 1)
                    print(self.prompts['quit_confirm'][quit_num])
                    raise SystemExit
                else:
                    print(self.prompts['quit_deny'])

            else:
                return float(user_new_frequency)

    def check_result(self, result):
        return None

# ui = UI_Interface()