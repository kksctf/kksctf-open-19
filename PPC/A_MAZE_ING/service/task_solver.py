#!/usr/bin/env python3

from collections import namedtuple

import labyrinth
import astar
import socket
import time

Path = namedtuple('Path', ['start', 'end', 'path', 'rest_doors', 'rest_keys'])
Path.sort_by_pathlen_key = lambda p : len(p.path)

def solve_labyrinth(lab):
    if type(lab) != labyrinth.Labyrinth:
        raise TypeError("argument must have type {}, got {}".format(labyrinth.Labyrinth, type(lab)))

    #prepare path finder
    a = astar.Astar(lab) ; a.chars_unwalkable = '#' ; a.chars_walkable += '+'
    st = lab.player_coords
    end = lab.exit_coords

    #if no keys -- simply find shortest path
    if not lab.conf.keys():
        return lab.simple_solve(st, end)

    keys = lab.keys.copy() ; keys.insert(0, end)
    doors = lab.doors.copy()

    #find first reachable key
    paths = []
    for k in keys:
        s = a.find_path(st, k, doors)
        if s != None:
            paths.append(Path(st, k, s, doors.copy(), keys.copy()))
            paths[-1].rest_keys.remove(k)

    final_paths = []

    #check paths with each reachable keys and doors
    while sum([len(p.rest_keys) for p in paths]) > 0 :
        #check shortest paths first
        paths.sort(key=Path.sort_by_pathlen_key)
        old_path_count = len(paths)

        for p in paths:
            #if reached end cell
            if not end in p.rest_keys:
                final_paths.append(p)
                continue

            #else test each reachable door
            for d in p.rest_doors:
                cur_doors = p.rest_doors.copy() ; cur_doors.remove(d)
                #and try to get next key
                for k in p.rest_keys:
                    a = astar.Astar(lab) ; a.chars_unwalkable = '#' ; a.chars_walkable += '+'
                    s = a.find_path(p.end, k, cur_doors)
                    #if next key found -- add this path for further check
                    if s != None:
                        paths.append(Path(p.start, k, p.path+s, cur_doors.copy(), p.rest_keys.copy()))
                        paths[-1].rest_keys.remove(k)

        #remove all paths that was continued/ended at last iteration
        paths = paths[old_path_count:]

    #sort by solution length
    final_paths.sort(key=Path.sort_by_pathlen_key)
    #get shortest
    return final_paths[0].path


server_ip = 'gamma.kksctf.ru'
server_port = 31397
sock = socket.socket()
sock.connect( (server_ip, server_port) )


def parse_lab(data):
    l = labyrinth.Labyrinth()
    d = data.strip().split(b'\n')
    print(data.strip().decode())
    print(len(d))
    for i in range(len(d)):
        d[i] = d[i][::2].decode().replace(':','@').replace('<','!').replace('{','+').replace('O','k')
        print(len(d[i]))
        l.field = d
        l.conf = labyrinth.Config(2|4)

    l.doors = []
    l.keys = []
    for i in range(len(d)-1):
        for j in range(len(d[i])-1):
            if d[i][j] == '+':
                l.doors.append( (j,i) )
            if d[i][j] == 'k':
                l.keys.append( (j,i) )
            if d[i][j] == '!':
                l.exit_coords = (j,i)
    print(l.keys, l.doors)
    return solve_labyrinth(l)

while True:
    while True:
        data = b''
        while data.strip().split(b'\n')[-1] != b'#'*78:
            try:
                data += sock.recv(1100)
                print(len(data.strip()))
                if b'flag' in data:
                    print(data) ; exit(0)
                if data.strip().split(b'\n')[-1] != b'#'*78:
                    print(data.strip().split(b'\n')[-1])
                time.sleep(0.05)
            except OSError:
                break

        print(data.strip().decode())
        s = parse_lab(data)
        if type(s) == str: s = s.encode()
        sock.send(s+b'\n')
        time.sleep(0.05)

