import termios
import sys
import os
import numpy as np
from time import sleep

c = 0


class Screen:
    def __init__(self, row=25, col=80):
        self.fd = sys.stdout.fileno()
        self.buf = np.zeros(shape=(row, col), dtype=bytes)
        self.row = row
        self.col = col

    def refresh(self):
        os.write(self.fd, b"\x1b[2J")

    def hide_cursor(self):
        os.write(self.fd, b"\e[?25l")

    def update_buffer(self, src):
        np.copyto(self.buf, src)

    def render(self):
        # os.write(self.fd, b"\x1b[2J") # clear screen
        self.refresh()
        buf = bytearray()
        buf.extend(b"\x1b[H")  # cursor on top left
        for row in range(self.row):
            for col in range(self.col):
                buf.extend(self.buf[row][col])
            buf.extend(b"\r\n")
        os.write(self.fd, buf)


def initialize_term():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~(termios.ECHO | termios.ICANON)
    new[1] &= ~(termios.OPOST)
    termios.tcsetattr(fd, termios.TCSAFLUSH, new)
    return old


def read_byte():
    return os.read(sys.stdin.fileno(), 1)


def process_input():
    pass


class Game:
    def __init__(self, row=25, col=80):
        self.screen = Screen(row, col)
        self.row = row
        self.col = col
        self.buf = np.zeros(shape=(row, col), dtype=bytes)

        self.buf.fill(b"\\")
        self.c = 0

    def tick(self):
        # if self.buf[0][0] == "-":
        #     self.buf.fill(b"/")
        # else:
        #     self.buf.fill(b"-")
        self.c += 1
        if self.c % 2 == 0:
            self.buf.fill(b"/")
        else:
            self.buf.fill(b"\\")

    def draw(self):
        self.screen.update_buffer(self.buf)
        self.screen.render()

    def run(self):
        try:
            old = initialize_term()
            while True:
                # process_input()
                self.tick()
                self.draw()
                sleep(1)
        finally:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, old)


if __name__ == "__main__":
    g = Game()
    g.run()
