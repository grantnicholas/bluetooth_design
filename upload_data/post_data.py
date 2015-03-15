import os
import sys


def post_data(filename):
    curl = 'cat {0} | curl -H "Content-Type: text/plain" -X POST --data-binary @- http://104.236.62.9:3000/upload'.format(
        filename)
    # print curl
    os.system(curl)


def main():
    filename = sys.argv[1]
    post_data(filename)

if __name__ == '__main__':
    main()
