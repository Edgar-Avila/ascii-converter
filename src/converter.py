import os
from threading import Thread
from time import sleep
import cv2 as cv
import numpy as np
from curses import wrapper
import curses

class AsciiConverter:
    def __init__(self, shades: str) -> None:
        self.map = [shades[int(np.interp(i, [0, 255], [0, len(shades)-1]))]
                    for i in range(256)]

    def convert_and_save(self, video: cv.VideoCapture, out_path):
        with open(out_path, 'w') as out_file:
            frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
            cols, rows = os.get_terminal_size()
            out_file.write(f'{rows}, {cols}, {frame_count}\n')
            for frame in range(frame_count):
                _, img = video.read()
                small = cv.resize(img, (cols-1, rows-1))
                gray = cv.cvtColor(small, cv.COLOR_BGR2GRAY)
                converted = [[self.map[val] for val in row] for row in gray]
                for row in converted:
                    out_file.write(''.join(row))
                    out_file.write('\n')
                if frame % 100 == 0:
                    print(f'{frame}/{frame_count}')

    def convert_and_play(self, video):
        def run(stdscr):
            frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
            rows, cols = stdscr.getmaxyx()
            for _ in range(frame_count):
                _, img = video.read()
                small = cv.resize(img, (cols-1, rows-1))
                gray = cv.cvtColor(small, cv.COLOR_BGR2GRAY)
                converted = [[self.map[val] for val in row] for row in gray]
                stdscr.clear()
                if cv.waitKey(20) == ord('q'):
                    break
                for row in converted:
                    stdscr.addstr(''.join(row))
                    stdscr.addstr('\n')
                stdscr.refresh()
                cv.imshow('Original', img)

        wrapper(run)

    def read_and_play(self, filename):
        def run(stdscr):
            pressed = ''
            def await_key_pressed():
                nonlocal pressed, stdscr
                key = -1
                while key != ord('q'):
                    key = stdscr.getch()
                    pressed = key
                
            t = Thread(target=await_key_pressed)
            t.start()
            with open(filename, 'r') as file:
                rows, cols, frame_count = file.readline().split(',')
                rows, cols, frame_count = int(rows), int(cols), int(frame_count)
                stdscr.clear()
                stdscr.refresh()
                for _ in range(frame_count):
                    if pressed == ord('q'):
                        break
                    stdscr.clear()
                    for _ in range(rows-1):
                        line = file.readline()
                        stdscr.addstr(line)
                    sleep(1/60)
                    stdscr.refresh()

        wrapper(run)