import numpy as np
import os
import sys
import termios
import fcntl


def initialize_term():
    fd = sys.stdout.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    newattr[1] &= ~(termios.OPOST)
    newattr[6][termios.VTIME] = 0
    newattr[6][termios.VMIN] = 0
    termios.tcsetattr(fd, termios.TCSADRAIN, newattr)

    os.system("clear")
    os.system("tput civis")
    return oldterm


class Screen:
    def __init__(self, row, col):
        self.fd = sys.stdout.fileno()
        self.buf = np.zeros(shape=(row, col), dtype=bytes)
        self.buf.fill(" ")
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

    def render(self, buf, l, r):
        # os.write(self.fd, b"\x1b[2J") # clear screen
        self.refresh()
        out = bytearray()
        out.extend(b"\x1b[H")  # cursor on top lef
        for row in range(self.row):
            for col in range(l, r):
                if buf[row][col] == b"":
                    out.extend(b" ")
                else:
                    out.extend(buf[row][col].encode("utf-8"))
            out.extend(b"\r\n")
        # sys.stdout.buffer.write(out)
        os.write(self.fd, out)
