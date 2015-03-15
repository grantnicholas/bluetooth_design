import re
import sys

rx = re.compile('value:(.+)')


def decode_line(aline):
    match_data = re.findall(rx, line)
    if match_data != []:
        match_data = match_data[0]
        no_whitespace = match_data.replace(' ', '')
        decoded = no_whitespace.decode('hex')
        return decoded


for line in sys.stdin:
    var = decode_line(line)
    if var is not None:
        print var
