# Author: Sojung Choi
# Assignment: 8
import re
import logging

# Declare global variables
CODE = 'imperdiet'


# The main method for this program.
def main():
    # Configure logging to console and LOG file for troubleshooting.
    # Add custom level to logging module
    log_level = 9
    log_name = 'TRACE'
    logging.basicConfig(
        level=int(log_level),
        format="%(asctime)s:%(levelname)s:%(message)s",
        filename="consoleapp.log",
        filemode="w")

    def trace(msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(log_level):
            logging.log(log_level, msg, *args, **kwargs)

    logging.addLevelName(log_level, log_name)
    logging.trace = trace
    logging.Logger.log_lower = trace

    # Displays program introduction to the user in the console.
    intro()
    # Declare exit variable
    escape = 'y'
    while escape == 'y':
        try:
            # Prompt the user whether the program should proceed with either
            # read or write mode and store the input.
            switch = get_switch()
            if switch == 'r':
                # If the user chooses to start the program in "r" mode,
                # ask for the path to the text file that the program should read,
                # then read the file line by line and count how many times the code
                # word occurs in how many lines.
                count_word_in_file(switch)
            elif switch == "w":
                # If the user chooses to start the program in "w" mode,
                # ask the user for a sentence and count how many times
                # the code word occurs based on the user's input.
                count_word_from_input()
        finally:
            escape = input('\nWould you like to keep going'
                           """ Enter 'y' to keep going, otherwise """
                           'press any key to exit: ')


# Displays an introduction to explain the program to the user.
def intro():
    logging.trace('Intro started', exc_info=True)
    print("\nThis application accepts two input parameters:"
          "\nThe first is a read/write switch, "
          "and the second is a path to a your test text file.")
    logging.trace('Intro printed')


# Retrieves the user's input whether to start the program in "read" or "write" mode.
def get_switch():
    switch = str(input("""\nPROMPT: Please select either read or write mode (r/w):"""))
    return str.lower(switch)


# Counts the number of times the code word appears in the file
# located at the path provided by the user.
# Takes the switch selected (either "r" or "w") as a parameter
def count_word_in_file(switch):
    word_count = 0
    line_count = 0
    try:
        path = get_path()
        file = open(path, switch)
        for x in file:
            word_list = split_line(x)
            result = count_words_in_line(word_list)
            word_count += result[0]
            line_count += result[1]
        print('\nThe word "{}"'.format(CODE), 'appears',
              word_count, 'times in', line_count, 'line(s).')
        file.close()
    except IOError as e:
        print("I/O error 9{0}: {1}".format(e.errno, e.strerror))


# Retrieves a string from the user to the file location to read from.
def get_path():
    # get user input
    user_input = str(input("""\nPROMPT: Please provide the path to the text file to read from: """))
    path = str.lower(user_input)
    return path


# Counts of the number of times the code word appears based
# on the user's input
def count_word_from_input():
    word_count = 0
    line_count = 0
    total_lines = 0
    user_sentence = get_sentence()
    while str.lower(user_sentence) != "q":
        total_lines += 1
        word_list = split_line(user_sentence)
        result = count_words_in_line(word_list)
        word_count += result[0]
        line_count += result[1]
        user_sentence = get_sentence()
    print('\nYou entered', total_lines, 'line(s). The word "{}"'.format(CODE), "appears",
          word_count, "time(s) in", line_count, "line(s).")


# Retrieves the user's input sentence
def get_sentence():
    user_sentence = str(input("""\nPROMPT:Please enter a sentence (enter "q" to exit):\n"""))
    sentence = str.lower(user_sentence)
    return sentence


# Reads the line and splits the string into a list based on white space
def split_line(x):
    word_list = re.findall(r'\w+', x)
    return word_list


# Counts the number of times the code word appears as well as the number of
# lines the word appears in
def count_words_in_line(word_list):
    count = 0
    lines = 0
    exists = 0
    for y in word_list:
        if str.lower(y) == CODE:
            count += 1
            exists = 1
    if exists == 1:
        lines += 1
    return [count, lines]


main()

