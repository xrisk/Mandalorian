import numpy as np
import os
import sys
import termios
import fcntl

from colorama import Fore


def initialize_term():
    fd = sys.stdout.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    # newattr[1] &= ~(termios.OPOST)
    newattr[6][termios.VTIME] = 0
    newattr[6][termios.VMIN] = 0
    termios.tcsetattr(fd, termios.TCSADRAIN, newattr)

    os.system("clear")
    os.system("tput civis")
    return oldterm


class Screen:
    def __init__(self, row, col):
        self.fd = sys.stdout.fileno()
        self.row = row
        self.col = col

    def initialize(self):
        self.old = initialize_term()

    def restore(self):
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, self.old)
        os.system("tput cvvis")

    def refresh(self):
        os.write(self.fd, b"\033[0;0H")
        # os.write(self.fd, b"\x1b[2J")

    def render(self, buf, l, r, banner):
        self.refresh()

        out = ""
        out = "\x1b[H"  # cursor on top lefth
        out += Fore.BLUE + banner + " | " + Fore.RESET
        out += "\r\n"
        for row in range(self.row):
            for col in range(l, r):
                if buf[row][col] == "":
                    out += " "
                else:
                    out += buf[row][col]
            out += "\r\n"
        # sys.stdout.buffer.write(out)
        print(out, flush=True)
