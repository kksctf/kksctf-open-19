#!/usr/bin/env python3


import barcode
import midi
import re
import os


def create_barcode(text: str, out_name: str):
    code128 = barcode.get_barcode_class("code128")
    bar = code128(text)
    fullname = bar.save(out_name)
    return fullname


regex_string = r'<rect x=".*" y=".*" width="(\d*).(\d*)mm".*style="fill:([a-z]*);"\/>'
regex_compiled = re.compile(regex_string)
def barcode_to_bin(barcode_path: str):
    barcode_svg = open(barcode_path, "r").read()
    parsed = regex_compiled.findall(barcode_svg)
    out = []
    for i in parsed:
        length = (int(i[0]) * 1000 + int(i[1])) // 200
        out.extend(([0] if i[2] == 'white' else [1]) * length)
    return out


def create_midi(text: str, sample_path: str, out_path: str):
    midifile = midi.read_midifile(sample_path)

    track = midifile[0][:]

    target = barcode_to_bin(create_barcode(text, "tmp"))
    target = [0]*10 + target
    pos = 0
    for v in target:
        for i in range(80, 100):
            on = midi.NoteOnEvent(tick=0, velocity=1, pitch=i if v else 0)
            track.insert(pos, on)
            pos += 1
        track.insert(pos, midi.NoteOnEvent(tick=40, velocity=1, pitch=0))
        pos += 1
        for i in range(80, 100):
            off = midi.NoteOffEvent(tick=0, pitch=i if v else 0)
            track.insert(pos, off)
            pos += 1

    for i in range(pos, len(track)-1):
        track.pop(pos)

    midifile.append(track)

    midi.write_midifile(out_path, midifile)


WORDS_LEN = 10
def main():
    conversation = open("./conversation.txt").readlines()
    for i, message in enumerate(conversation):
        cur_dir = "side" + message[0]
        cur_subdir = "pack{}".format(i)
        rel_path = os.path.join(".", "wwwdata", cur_dir, cur_subdir)
        if not os.path.exists(rel_path):
            os.mkdir(rel_path)
        words = []
        message = message.strip().split(": ")[1]
        while message:
            where_to_cut = WORDS_LEN if len(message) > WORDS_LEN else len(message)
            cut, message = message[:where_to_cut], message[where_to_cut:]
            words.append(cut)

        for i, word in enumerate(words):
            target_path = os.path.join(rel_path, "word{}".format(i))
            print("encoding {} into {}".format(word, target_path))
            create_midi(word, "input.mid", target_path)



if __name__ == "__main__":
    main()
