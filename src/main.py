import cv2 as cv
from converter import AsciiConverter
import argparse

def main():
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='Name of the video that you want to pass to ascii')
    args = parser.parse_args()

    # Check args
    if args.filename is None:
        raise RuntimeError('You need to specify a filename')

    # Define variables
    filename = args.filename
    shades = ' .:-=+*#%@'

    # Get video
    video = cv.VideoCapture(filename)
    if not video.isOpened():
        raise RuntimeError('Filename was incorrect or not a video')

    # Convert
    converter = AsciiConverter(video, shades)
    converter.convert_and_play()

    # Exit
    video.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()