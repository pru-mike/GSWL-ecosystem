#!/usr/bin/python
"""
Usage:
    reports.py (<file>)

"""

import sys
import os
import tty
import termios
import subprocess

REPORT_FILE = 'reports.txt'
TEMP_SCRIPT_FILE = '/tmp/.ledgerscript.sh'


def getchar():
    """
    Get a single character from stdin.
    """
    # from http://code.activestate.com/recipes/134892/
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def makescript(cmd):
    """
    Make a helper script which eases usage of the ecosystem.
    """
    out = ""
    out += '#!/bin/bash\n'
    out += 'shopt -s expand_aliases\n'
    out += '. alias\n'
    out += '{}\n'.format(cmd)
    with open(TEMP_SCRIPT_FILE, 'w') as fh:
        fh.write(out)
    os.chmod(TEMP_SCRIPT_FILE, 0777)


def show((expl, cmd)):
    """
    Show one report from the report file.
    """
    makescript(cmd)
    os.system('clear')
    print(expl)
    print(cmd)
    subprocess.call(TEMP_SCRIPT_FILE, shell=True)


def main(argv=None):
    if (argv is not None and len(argv) > 1):
        filename = argv[1]
    else:
        filename = REPORT_FILE

    reports = []
    with open(filename, 'r') as fh:
        expl = ''
        cmd = ''
        for line in fh.readlines()[2:]:  # skip header lines
            if (line.startswith('#')):
                expl += line
            elif (not line.startswith('\n')):
                # consider everything else as the cmd
                cmd = line.strip()

            if (cmd):
                reports.append((expl.strip(), cmd))
                cmd = ''
                expl = ''

    i = 0
    while True:
        show(reports[i])
        print('h = previous report, l = next report, q = quit [h/l/q] ?')
        action = getchar()
        if (action == 'h'):
            i = i - 1 if i > 0 else len(reports) - 1
        elif (action == 'l'):
            i = i + 1 if i < len(reports) - 1 else 0
        elif (action == 'q'):
            break

if __name__ == '__main__':
    main(sys.argv)
