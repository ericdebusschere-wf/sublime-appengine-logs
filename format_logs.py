import sys
import re
import datetime
import optparse

from collections import namedtuple

LOG_FORMAT_REGEX = '^\t([0-9]):([0-9\.]*)[\s]{1}(.*)$'
SPACING = '\t'

LogLevel = namedtuple('LogLevel', 'level color label label_spaces')

class color:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

class log_levels:
    REQUEST = LogLevel(None, color.ENDC, 'REQUEST', 3)
    DEBUG = LogLevel(0, color.BLUE, 'DEBUG', 4)
    INFO = LogLevel(1, color.GREEN, 'INFO', 5)
    WARNING = LogLevel(2, color.YELLOW, 'WARNING', 2)
    ERROR = LogLevel(3, color.RED, 'ERROR', 4)
    CRITICAL = LogLevel(4, color.PINK, 'CRITICAL', 1)

def get_log_level_values(log_level):
    if log_level is log_levels.DEBUG.level:
        return log_levels.DEBUG
    elif log_level is log_levels.INFO.level:
        return log_levels.INFO
    elif log_level is log_levels.WARNING.level:
        return log_levels.WARNING
    elif log_level is log_levels.ERROR.level:
        return log_levels.ERROR
    elif log_level is log_levels.CRITICAL.level:
        return log_levels.CRITICAL

def rewrite_line(line, color_line=False):
    splits = re.match(LOG_FORMAT_REGEX, line).groups()
    log_level = int(splits[0])
    time_stamp = str(datetime.datetime.fromtimestamp(float(splits[1])))

    ret_msg = splits[2]

    log_level = get_log_level_values(log_level)

    ret_line = log_level.label + (' ' * log_level.label_spaces) + time_stamp + (' ' * 3) + ret_msg

    if color_line:
        return colorize_line(ret_line, log_level)
    return ret_line

def colorize_line(line, log_level):
    return log_level.color + line

def print_logs_to_terminal(input_file):
    for line in input_file:
        line = line.strip('\n')
        if line[0] != '\t':  # log message
            print '\n' + log_levels.REQUEST.color + log_levels.REQUEST.label + SPACING + line
        elif not re.match(LOG_FORMAT_REGEX, line):
            print color.ENDC + line[2:]
        else:
            print rewrite_line(line, color_line=True)

def write_logs_to_file(input_file, output_file):
    output_lines = []
    for line in input_file:
        line = line.strip('\n')
        if line[0] != '\t':  # log message
            output_lines.append('\n' + log_levels.REQUEST.label + SPACING + line + '\n')
        elif not re.match(LOG_FORMAT_REGEX, line):
            output_lines.append(line[2:] + '\n')
        else:
            output_lines.append(rewrite_line(line) + '\n')
    output_file.writelines(output_lines)

def main():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--print", dest="print_to_terminal")
    parser.add_option("-o", "--output", dest="output_file")
    (options, args) = parser.parse_args()

    args = sys.argv[1:]

    if len(args) == 0:
        print 'You must supply an input log file to read'
        sys.exit(1)

    input_file = open(args[0], 'r')

    if not options.output_file and not options.print_to_terminal:
        options.print_to_terminal = True

    if options.print_to_terminal:
        print_logs_to_terminal(input_file)

    if options.output_file:
        output_file = open(options.output_file, 'w')
        write_logs_to_file(input_file, output_file)

if __name__ == '__main__':
    main()
