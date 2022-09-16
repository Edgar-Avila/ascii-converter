import cv2 as cv
from converter import AsciiConverter
import argparse
from os.path import splitext

def main():
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='Name of the video that you want to pass to ascii')
    parser.add_argument('-s', '--shade', help='Level of shading: "binary", "normal", "extended"')
    parser.add_argument('-o', '--out', help='Saves to file instead of showing ascii')
    args = parser.parse_args()

    # Check args
    if args.filename is None:
        raise RuntimeError('You need to specify a filename')
    if args.shade is not None:
        if args.shade not in ('binary', 'normal', 'extended'):
            raise RuntimeError('The argument shade should be "binary", "normal" or "extended"')

    # Define variables
    filename = args.filename
    out_path = args.out or ''
    selected_shade_level = args.shade or 'normal'
    shade_levels = {
        'binary': '.@',
        'normal': ' .:-=+*#%@',
        'extended': ' .`^",:;Il!i><~+_-?][1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    }
    shades = shade_levels[selected_shade_level]

    # Get video
    _, file_extension = splitext(filename)
    print(file_extension)
    converter = AsciiConverter(shades)
    if file_extension in ('.mp4', '.mov', '.avi'):
        video = cv.VideoCapture(filename)
        if not video.isOpened():
            raise RuntimeError('Filename was incorrect or not a video')

        # Convert
        if out_path:
            converter.convert_and_save(video, out_path)
        else:
            converter.convert_and_play(video)

        # Exit video
        video.release()
    elif file_extension in ('.txt'):
        converter.read_and_play(filename)

    
    # Exit all
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()