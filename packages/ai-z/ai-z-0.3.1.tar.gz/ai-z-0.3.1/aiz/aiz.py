#!/usr/bin/env python3

import argparse
import sys
from aiz.hwinfo import DetectHardware, PrintHardwareInfo, gpuDevices, DisplayStats
from time import sleep
import curses

__version__ = '0.3.1'


def ParseCmdLine(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', default=False, action='store_true')
    parser.add_argument('--showhwinfo', default=False, action='store_true')

    #print(argv)
    args = parser.parse_args(argv)

    return args


def InitDisplay():
    return curses.initscr()

def DisplayMenu(win):
    win.addch('\n')
    win.addch('\n')
    win.addstr("q:Quit")

def Shutdown(win):
    curses.endwin()
    sys.exit(0)

def MainLoop(win):
    if not curses.has_colors():
        print('Error: Terminal does not support color')
        Shutdown(win)

    curses.start_color()
    #COLOR_CYAN
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.noecho()
    win.nodelay(True)

    while(True):
        sleep(0.01)
        win.clear()
     
        DisplayStats(win, curses)

        DisplayMenu(win)

        curses.cbreak()
        key = win.getch()
        curses.nocbreak()
        if key == 113:
            Shutdown(win)

        win.refresh()


def main(argv):
    args = ParseCmdLine(argv[1:])


    if args.version is True:
        print("AI-Z version %s" % __version__)
        return


    DetectHardware()
    
    if args.showhwinfo is True:
        PrintHardwareInfo()
        return

    win = None

    try:
        win = InitDisplay()
        MainLoop(win)
    except Exception as e:
        print(e)
        Shutdown(win)

def run_main():
    main(sys.argv[1:])

if __name__ == '__main__':
    main(sys.argv)