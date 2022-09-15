import os
import cv2 as cv
import numpy as np
from curses import wrapper


class AsciiConverter:
    def __init__(self, video: cv.VideoCapture, shades: str) -> None:
        self.video: cv.VideoCapture = video
        self.height: int = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.width: int = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        self.frame_count: int = int(video.get(cv.CAP_PROP_FRAME_COUNT))

        self.map = [shades[int(np.interp(i, [0, 255], [0, len(shades)-1]))]
                    for i in range(256)]

    def convert_and_save(self, out_path):
        cols, rows = os.get_terminal_size()
        with open(out_path, 'w') as out_file:
            out_file.write(f'{rows}, {cols}, {self.frame_count}\n')
            for frame in range(self.frame_count):
                _, img = self.video.read()
                small = cv.resize(img, (cols-1, rows-1))
                gray = cv.cvtColor(small, cv.COLOR_BGR2GRAY)
                converted = [[self.map[val] for val in row] for row in gray]
                for row in converted:
                    out_file.write(''.join(row))
                    out_file.write('\n')
                if frame % 100 == 0:
                    print(f'{frame}/{self.frame_count}')

    def convert_and_play(self):
        def run(stdscr):
            rows, cols = stdscr.getmaxyx()
            for _ in range(self.frame_count):
                _, img = self.video.read()
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
