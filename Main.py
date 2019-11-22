# Author: Sojung Choi
# Assignment: 8
import re
import logging
import itertools
import fnmatch
from datetime import datetime
import time
import os

# Declare logging variables
log_level = 5
log_name = 'TRACE'

# Declare variable to search for in file and/or user input
code = 'imperdiet'

# Declare helper variables to determine metrics
total_lines_in_file = 0


# Configure logger to console and LOG file for troubleshooting.
# Add custom level to logging module
logging.addLevelName(log_level, log_name)


def trace(self, msg, *args, **kwargs):
    if self.isEnabledFor(log_level):
        self._log(log_level, msg, args, **kwargs)


logging.Logger.trace = trace
logging.basicConfig(
    filename='consoleapp.log', filemode="w", level=log_level,
    format="%(asctime)s - %(name)s - %(threadName)s - %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)


# The main method for this program.
def main():

    logger.info('Log level: %s, %s', log_level, log_name)
    logger.info('Code word search: %s', code)
    logger.info('Log output file: consoleapp.log')
    logger.trace('main() call')
    time_start = int(round(time.time()*1000))
    logger.info('The program started @ %s', time_start)

    # Displays program introduction to the user in the console.
    intro()

    # Declare exit variable
    escape = 'y'

    # Begin program loop
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
                os.remove('writefile.txt')
                f = open('writefile.txt', 'w')
                # If the user chooses to start the program in "w" mode,
                # ask the user for a sentence and count how many times
                # the code word occurs based on the user's input.
                count_word_from_input(f)
        finally:
            logger.trace('In try-finally')
            escape = input('\nWould you like to keep going'
                           """ Enter 'y' to keep going, otherwise """
                           'press any key to exit: ')
            logger.debug('Escape input: %s', escape)
    logger.trace('main() exit')
    time_end = int(round(time.time()*1000))
    logger.info('Program ended @ %s', time_end)
    get_metrics()


# Displays an introduction to explain the program to the user.
def intro():
    logger.trace('intro() call')
    print("\nThis application accepts two input parameters:"
          "\nThe first is a read/write switch, "
          "and the second is a path to a your test text file.")
    logger.trace('intro() exit')


# Retrieves the user's input whether to start the program in "read" or "write" mode.
def get_switch():
    logger.trace('get_switch() call')
    user_switch = input("""\nPROMPT: Please select either read or write mode (r/w):""")
    switch = str.lower(user_switch)
    logger.debug('switch input: %s', switch)
    if switch != ('r' or 'w'):
        logger.error('Incorrect input entered for switch')
    return switch


# Counts the number of times the code word appears in the file
# located at the path provided by the user.
# Takes the switch selected (either "r" or "w") as a parameter
def count_word_in_file(switch):
    logger.trace('count_word_in_file() call')
    word_count = 0
    line_count = 0
    total_lines = 0
    try:
        path = get_path()
        file = open(path, switch)
        logger.trace('open file:' + file.name)
        time_start = int(round(time.time() * 1000))
        logger.info('Read file started @ %s', time_start)
        for idx, x in enumerate(file):
            time_start = int(round(time.time() * 1000))
            logger.info('Read file line started @ %s', time_start)
            logger.info('')
            total_lines += 1
            word_list = split_line(x)
            result = count_words_in_line(word_list)
            word_count += result[0]
            line_count += result[1]
            logger.debug('%s iteration, word_count=%s, line_count=%s', idx, word_count, line_count)
            time_end = int(round(time.time() * 1000))
            logger.info('Read file line ended @ %s', time_end)
        time_end = int(round(time.time() * 1000))
        logger.info('Read file ended @ %s', time_end)
        logger.debug('Return count result: %s, line count: %s, total lines: %s', word_count, line_count, total_lines)
        print('\nThe word "{}"'.format(code), 'appears',
              word_count, 'times in', line_count, 'line(s).')
        file.close()
        logger.info('File closed')
    except IOError as e:
        logger.critical('I/O error 9{0}: {1}'.format(e.errno, e.strerror))
    logger.trace('count_word_in_file() exit')


# Retrieves a string from the user to the file location to read from.
def get_path():
    logger.trace('get_path() call')
    # get user input
    user_input = str(input("""\nPROMPT: Please provide the path to the text file to read from: """))
    path = str.lower(user_input)
    logger.debug('path input: %s', path)
    if fnmatch.fnmatch(path, '*.txt'):
        logger.debug('Input in expected format')
    else:
        logger.error('Input not in expected format')
    logger.trace('get_path() exit')
    return path


# Counts of the number of times the code word appears based
# on the user's input
def count_word_from_input(f):
    logger.trace('count_word_from_input() call')
    word_count = 0
    line_count = 0
    total_lines = 0
    user_sentence = get_sentence()
    for i in itertools.count():
        if str.lower(user_sentence) == "q":
            break
        else:
            time_start = int(round(time.time() * 1000))
            logger.info('Write line started @ %s', time_start)
            f.write('\n' + user_sentence)
            time_end = int(round(time.time() * 1000))
            logger.info('Write line ended @ %s', time_end)
            total_lines += 1
            start = int(round(time.time() * 1000))
            logger.info('Find word from user start @ %s', start)
            word_list = split_line(user_sentence)
            result = count_words_in_line(word_list)
            word_count += result[0]
            line_count += result[1]
            logger.debug('%s iteration, word_count=%s, line_count=%s', i, word_count, line_count)
            user_sentence = get_sentence()
            end = int(round(time.time() * 1000))
            logger.info('Find word from user end @ %s', end)
    logger.debug('Return count result: %s, line count: %s', word_count, line_count)
    print('\nYou entered', total_lines, 'line(s). The word "{}"'.format(code), "appears",
          word_count, "time(s) in", line_count, "line(s).")


# Retrieves the user's input sentence
def get_sentence():
    logger.trace('get_sentence() call')
    user_sentence = str(input("""\nPROMPT:Please enter a sentence (enter "q" to exit):\n"""))
    sentence = str.lower(user_sentence)
    logger.debug('user entered sentence: %s', sentence)
    time_end = int(round(time.time() * 1000))
    logger.info('Write line ended @ %s', time_end)
    return sentence


# Reads the line and splits the string into a list based on white space
def split_line(x):
    logger.trace('split_line() call')
    word_list = re.findall(r'\w+', x)
    logger.debug('split line result: word_list length: %s', len(word_list))
    return word_list


# Counts the number of times the code word appears as well as the number of
# lines the word appears in
def count_words_in_line(word_list):
    logger.trace('count_words_in_line() call')
    count = 0
    lines = 0
    exists = 0
    for idx, y in enumerate(word_list):
        if str.lower(y) == code:
            count += 1
            exists = 1
            logger.debug('%s iteration, word_count=%s', idx, count)
    if exists == 1:
        lines += 1
    logger.debug('Return count words result: %s, line count: %s', count, lines)
    return [count, lines]


def get_metrics():
    metrics = str(input("""\nWould you like to see program metrics? Press any key to continue, or enter "q" to exit):\n"""))
    if metrics != 'q':
        get_total_execution_time()
        average_time_to_read_file_line()
        average_time_to_find_word_in_line()
        average_time_to_write_file_line()
        average_time_to_fine_word_in_user_line()


# Helper method to read log file into list
def get_log_list():
    logs = []
    for line in open('consoleapp.log', 'r'):
        logs.append(line.strip().split('>'))
    return logs


def get_line_from_log(idx):
    logs = get_log_list()
    return str(logs[idx])


def get_time_from_log_line(x):
    my_list = re.split('- |,', x)
    time_stamp = my_list[0]
    time_stamp = time_stamp.replace('[', '')
    time_stamp = time_stamp.replace("'", '')
    dt_obj = datetime.strptime(time_stamp,
                               '%Y-%m-%d %H:%M:%S')
    millisecond = dt_obj.timestamp()*1000
    return millisecond


def parse_log(string):
    log_file_path = r'consoleapp.log'
    with open(log_file_path, 'r') as file:
        for line in file:
            line_list = re.split(' - ', line)
            check_string = line_list[len(line_list)-1]
            split_check_string = re.split(':', check_string)
            x = split_check_string[1]
            if x.find(string) >= 0:
                x_split = re.split('@ ', x)
                milli = int(x_split[1])
                return milli


def get_total_execution_time():
    start = parse_log('The program started')
    end = parse_log('Program ended')
    print('The program  execution time: ', end - start)


def average_time_to_read_file_line():
    start = parse_log('Read file started')
    end = parse_log('Read file ended')
    print('The average time to read a line from the file: ', end - start)


def average_time_to_find_word_in_line():
    start = parse_log('Read file line started')
    end = parse_log('Read file line ended')
    print('The average time to find the word in a single line from the file: ', end - start)


def average_time_to_write_file_line():
    start = parse_log('Write line started')
    end = parse_log('Write line ended')
    print('The average time to read a line from the file: ', end - start)


def average_time_to_fine_word_in_user_line():
    start = parse_log('Find word from user start')
    end = parse_log('Find word from user end')
    print('The average time to find the word in a single line from user input: ', end - start)


main()

