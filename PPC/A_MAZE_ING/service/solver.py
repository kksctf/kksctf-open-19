#!/usr/bin/env python3

from collections import namedtuple

import labyrinth
import astar

Path = namedtuple('Path', ['start', 'end', 'path', 'rest_doors', 'rest_keys'])
Path.sort_by_pathlen_key = lambda p : len(p.path)

def solve_labyrinth(lab):
    #lab = labyrinth.Labyrinth() #TODO: TEMP!!!
    if type(lab) != labyrinth.Labyrinth:
        raise TypeError("argument must have type {}, got {}".format(labyrinth.Labyrinth, type(lab)))

    a = astar.Astar(lab) ; a.chars_unwalkable = '#' ; a.chars_walkable += '+'
    st = lab.player_coords
    end = lab.exit_coords

    if not lab.conf.keys():
        return lab.simple_solve(st, end)

    keys = lab.keys.copy() ; keys.insert(0, end)
    doors = lab.doors.copy()

    paths = []
    for k in keys:
        s = a.find_path(st, k, doors)
        if s != None:
            paths.append(Path(st, k, s, doors.copy(), keys.copy()))
            paths[-1].rest_keys.remove(k)
            #print(paths[-1])
            #lab.draw_solution(paths[-1].path)
            #print('\n\n')

    #print(len(paths), paths[0].path, paths[0].rest_keys, paths[0].rest_doors)
    final_paths = []

    while sum([len(p.rest_keys) for p in paths]) > 0 :
        paths.sort(key=Path.sort_by_pathlen_key)
        old_path_count = len(paths)

        for p in paths:
            if not end in p.rest_keys:
                final_paths.append(p)
                continue

            for d in p.rest_doors:
                cur_doors = p.rest_doors.copy() ; cur_doors.remove(d)
                for k in p.rest_keys:
                    #print('key:',k, 'door:',d, p.rest_keys, cur_doors)
                    a = astar.Astar(lab) ; a.chars_unwalkable = '#' ; a.chars_walkable += '+'
                    s = a.find_path(p.end, k, cur_doors)
                    if s != None:
                        paths.append(Path(p.start, k, p.path+s, cur_doors.copy(), p.rest_keys.copy()))
                        paths[-1].rest_keys.remove(k)
                        #print(paths[-1])
                        #lab.draw_solution(paths[-1].path)
                        #lab.draw_solution(p.path)
                        #print('\n\n')

        paths = paths[old_path_count:]

    final_paths.sort(key=Path.sort_by_pathlen_key)
    return final_paths[0].path

