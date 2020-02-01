#!/usr/bin/env python3


import midi
import sys
import os
from PIL import Image, ImageOps
from pyzbar import pyzbar


def solve_one(path: str) -> str:
    midifile = midi.read_midifile(path)             # Load and parse midifile

    target_track = midifile[1]                      # Get track with encoded barcode
    
    barcode_as_bin = []

    line = False
    space = False

    for v in target_track:
        if v.data == [99, 1]:                       # Notes from 80 to 99, we choose one
            line = True
            continue
        elif v.data == [0, 1] and not line:
            space = True
            continue
                                                    # We'll add 255 and 0, and invert them later
        if line and v.data == [99, 0]:
            line = False
            barcode_as_bin.append(255)              # If note 99 ended, add 255 (White) to sequence
        elif space and v.data == [0, 0]:
            space = False                           # If note 0 ended, then it was spacing between black lines of barcode
            barcode_as_bin.append(0)

    [barcode_as_bin.append(0) for _ in range(10)]   # Add 10 whitelines to end
    
    im = Image.new("L", (850, 100))
    pix = im.load()
    for pos, val in enumerate(barcode_as_bin):      # Draw white lines on black background
        for i in range(50):                         # Height = 50
            for j in range(5):                      # Width = 5
                pix[5*pos + j, 25+i] = val
    im = ImageOps.invert(im)                        # Invert white to black
    
    #im.show()                                      # If you want to see decoded barcode, you can uncomment this

    text = pyzbar.decode(im)[0].data.decode()       # Decode text from barcode
    print(text, end="", flush=True)
    return text


def main():
    if len(sys.argv) < 2:
        exit(1)
    
    path_to_solve = os.path.join(os.getcwd(), sys.argv[1])
    solve_one(path_to_solve)


if __name__ == "__main__":
    main()

