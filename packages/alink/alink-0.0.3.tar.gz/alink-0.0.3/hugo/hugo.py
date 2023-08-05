import sys
import os


def main(args):
    if len(args) == 0:
        return
    url = args[0]
    output = os.popen('adb -d shell am start %s -a android.intent.action.VIEW' % url).readlines()[0]
    echo(output)


def echo(value):
    print('\033[32m %s \033[0m' % value)


if __name__ == '__main__':
    main(sys.argv[1:])
