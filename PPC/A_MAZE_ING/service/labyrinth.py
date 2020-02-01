#!/usr/bin/env python3

import sys
import time
import random
from collections import namedtuple
import field
from field import GameError
import astar
import algorithms
from itertools import chain #to flattern list


class Config:
    optionset = [0,1,2,4,8,16]
    opt_none = optionset[0]
    opt_loops = optionset[1]
    opt_rooms = optionset[2]
    opt_keys = optionset[3]
    opt_fog_linear = optionset[4]
    opt_fog_radial = optionset[5]

    def __init__(self, options = 0, **kwargs):
        '''allows to pass options as bits or explicitly. kwargs overrides options
        kwargs:
            rooms = False        #whether generate rooms or not
            keys = False         #place doors and keys
            fog = False          #draw fog (both linear and radial)
            linear_fog = False   #draw linear fog
            radial_fog = False   #draw radial fog
            room_count = random.randrange(2,8)
            keys_count = random.randrange(2,4)
            fog_radius = 5'''

        self.options = options
        if 'rooms' in kwargs.keys():
            if kwargs['rooms']: self.options |= self.opt_rooms
            else: self.options &= ~self.opt_rooms

        if 'room_count' in kwargs.keys():
            self.__room_count = kwargs['room_count']
        else:
            self.__room_count = random.randrange(3,8)

        if 'keys' in kwargs.keys():
            if kwargs['keys']: self.options |= self.opt_keys
            else: self.options &= ~self.opt_keys

        if 'keys_count' in kwargs.keys():
            self._keys_count = kwargs['keys_count']
        else:
            self._keys_count = random.randrange(2,4)

        if 'fog' in kwargs.keys():
            if kwargs['fog']: self.options |= self.opt_fog_linear | self.opt_fog_radial
            else: self.options &= ~self.opt_fog_linear

        if 'linear_fog' in kwargs.keys():
            if kwargs['linear_fog']: self.options |= self.opt_fog_linear
            else: self.options &= ~self.opt_fog_linear

        if 'radial_fog' in kwargs.keys():
            if kwargs['radial_fog']: self.options |= self.opt_fog_radial
            else: self.options &= ~self.opt_fog_radial

        if 'fog_radius' in kwargs.keys():
            self.__fog_radius = kwargs['fog_radius']
        else:
            self.__fog_radius = 5

    def rooms(self): return bool(self.options & self.opt_rooms)
    def keys(self): return bool(self.options & self.opt_keys)
    def fog(self): return self.linear_fog() and self.radial_fog
    def linear_fog(self): bool(self.options & self.opt_fog_linear)
    def radial_fog(self): return bool(self.options & self.opt_fog_radial)
    def room_count(self): return self.__room_count
    def keys_count(self): return self._keys_count
    def fog_radius(self): return self.__fog_radius



Room = namedtuple('Room', ['pos', 'size'])

class Labyrinth(field.Field):
    __charset = '# @!_k+~-' #wall empty player target visited key door fog path
    __char_wall = __charset[0]
    __char_empty = __charset[1]
    __char_player = __charset[2]
    __char_exit = __charset[3]
    __char_visited = __charset[4] #for generation
    __char_key = __charset[5]
    __char_door = __charset[6]
    __char_fog = __charset[7]
    __char_path = __charset[8]

    #__optionset = [0,1,2,4,8,16]
    #opt_none = __optionset[0]
    #opt_loops = __optionset[1]
    #opt_rooms = __optionset[2]
    #opt_keys = __optionset[3]
    #opt_fog_linear = __optionset[4]
    #opt_fog_radial = __optionset[5]

    ########
    ##init##
    def __init__(self, config = Config(), size = (79//2, 25)):
        walkable = self.__char_empty + self.__char_exit + self.__char_visited + self.__char_key
        unwalkable = self.__char_wall + self.__char_door
        super().__init__(size, self.__char_empty, self.__char_wall, walkable = walkable, unwalkable = unwalkable)

        self.conf = config
        self.collected_keys = []

        self.rooms = []
        self.doors = []
        self.keys = []

        self.player_coords = [1,1]
        #self.exit_coords = (self.size[0]-2, self.size[1]-2)

        #keys may fail, take more than one attempt to generate
        generated = False
        if  self.conf.keys():
            for kc in range(self.conf.keys_count(), -1, -1):
                self.conf._keys_count = kc
                for i in range(3): #10 attempts to generate w/o errors
                    try:
                        self.generate(False)
                        generated = True
                        break
                    except Exception as e:
                        ex = e
                        print('Failed to generate:', e, file=sys.stderr)
                if generated: break
        else:
            try:
                self.generate(False)
                generated = True
            except Exception as e:
                ex = e
                print('Failed to generate:', e, file=sys.stderr)
        if not generated:
            raise ex

    def __get_unvisited_neighbours(self, coords, distance=2):
        res = []
        for c in [(coords[0] + k[0]*distance, coords[1] + k[1]*distance) for k in zip([-1,1,0,0], [0,0,-1,1])]: #check neighbours
            try:
                if self.get_cell(c) == self.__char_empty:
                    res.append(c)
            except GameError as e:
                pass
                #print(e, c)
        return res

    def __place_room(self, pos, size):
        self.rooms.append( Room(pos, size) )
        for i in range(pos[0], pos[0]+size[0]):
            for j in range(pos[1], pos[1]+size[1]):
                self.set_cell(self.__char_visited, (i,j))
                #self.set_cell(self.__char_empty, (i,j))

    #TODO: check len of path from each room (and maybe between rooms?)
    #so choose a room for a key

    def __is_path_exists(self, solution): #start, end):
        return (solution != None) and (len(solution) > 0)

    def __reachable_rooms(self, start, banned_list = None):
        if banned_list == None: banned_list = self.doors
        if not self.conf.rooms:
            return None
        res = []
        for i in self.rooms:
            s = self.simple_solve(start, i.pos, banned_list = banned_list)
            if self.__is_path_exists(s):
                res.append(i)
        return res

    def __closest_point_index(self, target, points_list, banned_list = None):
        'returns index of point closest to target point'
        if banned_list == None: banned_list = self.doors
        res = []
        #no path can be longer than max_len so max_len means no path exists
        max_len = self.size[0]*self.size[1]*2
        for i in points_list:
            s = self.simple_solve(i, target, banned_list = banned_list)
            res.append(len(s) if self.__is_path_exists(s) else max_len)
        if len(res) == 0: return None
        m = min(res)
        return None if m == max_len else res.index(m)

    #if coridor (according to generator)
    def __is_coridor(self, point):
        'if cell has 2 of 4 nearest cells as walls'
        walls_count = 0
        for i in zip([0,0,-1,1], [-1,1,0,0]):
            if self.get_cell(point[0]+i[0], point[1]+i[1]) == self.__char_wall:
                walls_count += 1
        return walls_count == 2

    def __generate_doors_step(self, doors, only_key = False):
        '''doors are not empty; self.keys are not empty'''
        __flattern_doors = lambda: list(chain(*doors))
        __flattern = lambda x: list(chain(*x))
        target_point = self.exit_coords if len(self.keys) == 0 else self.keys[-1]

        #step 2,4,...: place key
        if self.conf.rooms:
            rooms_available = self.__reachable_rooms(self.player_coords, banned_list = __flattern_doors())
            ri = self.__closest_point_index(
                    target_point,
                    [r.pos for r in rooms_available],
                    banned_list = __flattern(doors[:-1]))
            if ri == None: raise ValueError('cannot place key') #TODO: GenerationError

            r = rooms_available[ri]
            c = (r.pos[0] + (r.size[0] // 2), r.pos[1] + (r.size[1] // 2))
            self.keys.append(c)
            self.set_cell(self.__char_key, self.keys[-1])
        #TODO: else random point
        #print('key placed:', self.keys[-1])
        if only_key: return

        #step 3,5,...: surround key with doors
        target_point = self.exit_coords if len(self.keys) < 2 else self.keys[-2]
        doors.append([])
        #print(__flattern_doors())
        while True: #check bypass
            s = self.simple_solve(
                    self.player_coords,
                    target_point,
                    banned_list = __flattern(doors[:-2]+doors[-1:]))#doors[-1])
            if s == None: break

            #solution from key to start
            s_k_s = self.__solution_to_coords(
                self.simple_solve(
                    self.keys[-1],
                    self.player_coords,
                    banned_list = __flattern(doors[:-2]+doors[-1:])),#doors[-1]),
                self.keys[-1])
            #solution from key to end
            s_k_e = self.__solution_to_coords(
                self.simple_solve(
                    self.keys[-1],
                    target_point,
                    banned_list = __flattern(doors[:-2]+doors[-1:])),#doors[-1]),
                self.keys[-1])

            if s_k_s == None or s_k_e == None:
                break

            #find last common cell
            com_i = None
            for i in range(min(len(s_k_s), len(s_k_e))):
                #print(s_k_s[i], '==' if s_k_s[i] == s_k_e[i] else '!=', s_k_e[i])
                if s_k_s[i] == s_k_e[i]: #they MUST have save len
                    com_i = i

            #find first different cell
            dif_i = None
            for i in range(com_i, min(len(s_k_s), len(s_k_e))):
                if s_k_s[i] != s_k_e[i]:
                    dif_i = i
                    break

            #place door
            for i in range(dif_i, len(s_k_s)):
                #print(i, s_k_s[i])
                if self.__is_coridor(s_k_s[i]):
                    doors[-1].append(s_k_s[i])
                    break

    def __generate_doors(self):
        'doors generation'
        #print('doors generation')
        self.doors = [] #writing here flattern list of lists 'doors' at end
        self.keys = []

        doors = [] #list of lists of doors. To divide in logical blocks (for each step)

        #step 1: place last door(s)
        doors.append([])
        __flattern_doors = lambda: list(chain(*doors)) #TODO: maybe to globals?
        s = self.__solution_to_coords(self.simple_solve(banned_list = __flattern_doors()))
        while s != None:
            #go by path from end
            for i in s[::-1][3:]:
                if self.__is_coridor(i):
                    doors[-1].append(i) ; break
            #doors[-1].append(s[-4]) #ok for room 3*3
            s = self.__solution_to_coords(self.simple_solve(banned_list = __flattern_doors()))
        #print('last doors placed')

        #steps 2..(n-1)
        for i in range(self.conf.keys_count()):
            self.__generate_doors_step(doors, i == self.conf.keys_count()-1)

        #step n: place doors on field
        self.doors = __flattern_doors()
        for i in self.doors:
            self.set_cell(self.__char_door, i)

    def __rooms_overlap(self, r1, r2):
        return (((r1.pos[0] <= r2.pos[0] and r2.pos[0] <= r1.pos[0]+r1.size[0]-1) or
                (r2.pos[0] <= r1.pos[0] and r1.pos[0] <= r2.pos[0]+r2.size[0]-1)) and
                ((r1.pos[1] <= r2.pos[1] and r2.pos[1] <= r1.pos[1]+r1.size[1]-1) or
                (r2.pos[1] <= r1.pos[1] and r1.pos[1] <= r2.pos[1]+r2.size[1]-1)))

    def generate(self, debug = False):
        ##prepare field
        #fill all field with walls
        self.field = [self.__char_wall * self.size[0]] * self.size[1]

        #make empty holes in each 2nd coord from (1,1): (3,1), (1,3), (3,3) and etc.
        for i in range(1, self.size[0]-1, 2):
            for j in range(1, self.size[1]-1, 2):
                self.set_cell(self.__char_empty, (i,j))

        #generate maze (maybe recursion?.. no)
        current = (random.randrange(3, self.size[0]-4) | 1, random.randrange(3, self.size[1]-4) | 1) #self.player_coords
        stack = [current]
        while True:
            #current cell is visited, check nearest
            if debug:
                self.draw()
                time.sleep(0.015)
            self.set_cell(self.__char_visited, current)
            unvis = self.__get_unvisited_neighbours(current)

            #if no unvisited -- remove from stack, go back
            if len(unvis) == 0:
                stack = stack[:-1]
                if len(stack) == 0:
                    break
                current = stack[-1]
            #else choose new way randomly
            else:
                r = random.randrange(len(unvis))
                stack.append(unvis[r])
                next_c = stack[-1]
                #draw way #TODO: more beautiful
                if current[0] == next_c[0]:
                    for i in range(min(current[1], next_c[1]), max(current[1], next_c[1])+1):
                        self.set_cell(self.__char_visited, (current[0], i))
                else:
                    for i in range(min(current[0], next_c[0]), max(current[0], next_c[0])+1):
                        self.set_cell(self.__char_visited, (i, current[1]))
                current = next_c

        #generate rooms
        if self.conf.rooms():
            self.rooms = []
            for _ in range(random.randrange(2,8)):
                for __ in range(5): #try to place a room 5 times
                    room_size = [(3,5), (5,3)][random.randrange(2)]
                    room_pos = (random.randrange(3, self.size[0]-3-room_size[0]) | 1, random.randrange(3, self.size[1]-3-room_size[1]) | 1)
                    ok = True
                    for r in self.rooms: #check collision
                        if self.__rooms_overlap(r, Room(room_pos, room_size)):
                            ok = False ; break
                    if ok:
                        self.__place_room(room_pos, room_size)
                        break

        ##TODO: generate loops
        #if self.conf.loops():
        #    pass

        #place exit
        self.exit_coords = ( (self.size[0] & (~1))-1, (self.size[1] & (~1))-1)
        self.set_cell(self.__char_visited, self.exit_coords[0]-1, self.exit_coords[1])
        self.set_cell(self.__char_visited, self.exit_coords[0], self.exit_coords[1]-1)
        if self.conf.rooms():
            #self.__place_room( ((self.size[0]-1-3) | 1, (self.size[1]-1-3) | 1), (3,3) )
            self.__place_room( (self.exit_coords[0]-2, self.exit_coords[1]-2), (3,3) )
            self.exit_coords = (self.exit_coords[0]-1, self.exit_coords[1]-1)
        #if self.size[0] & 1 == 1: #TODO: wut?? if field has right side 1 cell wider
        #    self.exit_coords = (self.size[0]-3, self.size[1]-3)
        #else:
        #    self.exit_coords = (self.size[0]-4, self.size[1]-3)
        self.set_cell(self.__char_exit, self.exit_coords)

        #TODO: generate keys
        if self.conf.keys():
            self.__generate_doors()

        #replace all visited cells with empty
        for i in range(len(self.field)):
            self.field[i] = self.field[i].replace(self.__char_visited, self.__char_empty)
        g = algorithms.generate_graph(self, self.player_coords, self.exit_coords) #TODO: temp!
        #print(g.verts)
        e = g.edges.items()
        #for i in sorted(e, key = lambda x: x[1].v1 * len(g.verts) + x[1].v2):
            #print(i)


    ########
    ##util##

    ##########
    ##checks##
    def is_exit(self, *args):
        '''is_wall(self, coords_tuple)\nis_wall(self, x, y)'''
        return self.get_cell(*args) == self.__charset[3]

    def reached_exit(self):
        return self.is_exit(self.player_coords)

    ########
    ##game##
    def turn(self, direction):
        try:
            d = {'u': (0,-1), 'd': (0,1), 'l': (-1,0), 'r': (1,0)}[direction]
        except KeyError as e:
            raise ValueError(''.format(e))
        new_c = (self.player_coords[0] + d[0], self.player_coords[1] + d[1])

        #if door -- try to open
        if self.get_cell(new_c) == self.__char_door:
            if len(self.collected_keys) > 0:
                self.collected_keys.pop()
                self.set_cell(self.__char_empty, new_c)
            else:
                raise GameError('No key to open that door!')

        #if wall
        if self.is_wall(new_c):
            raise GameError('Wall hit')

        #update player coord
        self.player_coords[0] += d[0]
        self.player_coords[1] += d[1]

        #print(self.keys, self.player_coords)
        #if key -- collect
        if self.get_cell(self.player_coords) == self.__char_key: #TODO: or check by coords?
            self.collected_keys.append(tuple(self.player_coords))
            self.keys.remove(tuple(self.player_coords))
            self.set_cell(self.__char_empty, self.player_coords)

    def __fog_count_pos(self, center_coord, radius):
        fog_len_left = max(center_coord - radius//2, 0)
        fog_pos_right = min(center_coord + radius//2 + 1, self.size[0])
        return fog_len_left, fog_pos_right

    def __fog_line(self, cur_line, visible_l, visible_r):
        return self.set_str_in_line(self.__char_fog * self.size[0], visible_l, cur_line[visible_l:visible_r])

    def drawing_line_extra(self, cur_line, i, **kwargs):
        #draw solution if exist
        if 'solution_cells' in kwargs.keys() and kwargs['solution_cells'] != None:
            for j in kwargs['solution_cells']:
                if j[1] == i:
                    cur_line = self.set_char_in_line(cur_line, j[0], self.__char_path)

        #draw linear fog #TODO: rooms are badly fogged
        if self.conf.linear_fog():
            if i in range(self.player_coords[1]-1, self.player_coords[1]+2):
                cur_line = self.__fog_line(cur_line, kwargs['fog_hor_left'], kwargs['fog_hor_right']+1)

            if i in range(kwargs['fog_ver_top'], self.player_coords[1]-1):
                cur_line = self.__fog_line(cur_line, self.player_coords[0]-1, self.player_coords[0]+2)
            elif i in range(self.player_coords[1]-1, self.player_coords[1]+2):
                pass
            elif i in range(self.player_coords[1]+2, kwargs['fog_ver_bottom']+1): #fog_ver_bottom+1):
                cur_line = self.__fog_line(cur_line, self.player_coords[0]-1, self.player_coords[0]+2)
            else:
                cur_line = self.__char_fog * len(cur_line)
            pass

        #draw radial fog
        if self.conf.radial_fog():
            radius = self.conf.fog_radius() #TODO: TEMP
            vert_distance_from_player = abs(self.player_coords[1] - i)
            if vert_distance_from_player > radius:
                cur_line = self.__char_fog * len(cur_line)
            else:
                l = (radius - vert_distance_from_player) * 2 + 1
                fog_len_left, fog_pos_right = self.__fog_count_pos(self.player_coords[0], l)
                cur_line = self.__fog_line(cur_line, fog_len_left, fog_pos_right)

        if self.player_coords[1] == i:
            cur_line = self.set_char_in_line(cur_line, self.player_coords[0], self.__char_player)
        #if self.exit_coords[1] == i:
        #    cur_line = cur_line[:self.exit_coords[0]-self.size[0]] + self.__charset[3] + cur_line[self.exit_coords[0]+1:]
        return cur_line

    def draw_to_str(self, solution_cells = None):
        #count borders of linear fog
        kwargs = {'solution_cells': solution_cells}
        if self.conf.linear_fog():
            for i in range(self.player_coords[0],-2,-1):
                if self.is_wall(i, self.player_coords[1]):
                    fog_hor_left = i
                    break
            for i in range(self.player_coords[0],self.size[0]+1):
                if self.is_wall(i, self.player_coords[1]):
                    fog_hor_right = i
                    break
            for i in range(self.player_coords[1],-2,-1):
                if self.is_wall(self.player_coords[0], i):
                    fog_ver_top = i
                    break
            for i in range(self.player_coords[1],self.size[1]+1):
                if self.is_wall(self.player_coords[0], i):
                    fog_ver_bottom = i
                    break

            #print('hor: {}, ver: {}'.format((fog_hor_left, fog_hor_right), (fog_ver_top, fog_ver_bottom)))
            kwargs = {'solution_cells': solution_cells,
                    'fog_hor_left': fog_hor_left,
                    'fog_hor_right': fog_hor_right,
                    'fog_ver_top': fog_ver_top,
                    'fog_ver_bottom': fog_ver_bottom
                    }

        res = super().draw_to_str(**kwargs)
        beautify = lambda l : l.replace('++','{}').replace('!!','<>').replace('kk','Om').replace('@@',':(')
        return beautify(res)

    #solver
    def simple_solve(self, start = None, end = None, banned_list = []):
        start = self.player_coords if start == None else start
        end = self.exit_coords if end == None else end
        a = astar.Astar(self)
        return a.find_path(start, end, banned_list)

    def solve_keys(self, start = None, end = None): #, banned_list = []):
        Path = namedtuple('Path', ['dirs', 'cur_pos', 'rest_doors', 'rest_keys'])
        paths = []
        ##step 0: test path to exit
        #s = self.simple_solve(start, end, banned_list)
        #if s != None: return s



    def __solution_to_coords(self, solution, start = None):
        if solution == None: return None
        cells = [self.player_coords if start == None else start]
        for i in solution:
            c = cells[-1]
            d = {'u': (0,-1), 'd': (0,1), 'l': (-1,0), 'r': (1,0)}[i]
            cells.append( (c[0]+d[0], c[1]+d[1]) )
        return cells

    def draw_solution(self, solution = None, start_coord = None):
        s = self.simple_solve() if solution == None else solution
        cells = self.__solution_to_coords(s, start_coord)
        print(self.draw_to_str(cells))


def play_local(**kwargs):
    #l = Labyrinth(Config(rooms = True, radial_fog = True))
    l = Labyrinth(Config(**kwargs)) #, linear_fog = True))
    print(l.draw_to_str())
    while not l.reached_exit():
        inp = [i.strip() for i in input().strip().split()]
        for i in inp:
            for j in i:
                l.turn(j)
            print(l.draw_to_str())
            if l.reached_exit(): break
    print('WIN')

def play_ai(**kwargs):
    l = Labyrinth(Config(**kwargs)) #, linear_fog = True))
    #l = Labyrinth(Config(**kwargs), ((int(79*2.5)//2 | 1),int(25*2.5)|1)) #, linear_fog = True))
    print(l.draw_to_str())
    solution = l.simple_solve()
    l.draw_solution() #TODO: pass solution to draw_solution
    time.sleep(1) #input()
    while not l.reached_exit():
        if solution != None:
            for i in solution:
                l.turn(i)
                l.draw_solution()
                #print(l.draw_to_str())
                if l.reached_exit(): break
                time.sleep(0.15)
        else: break
    print('WIN' if l.reached_exit() else 'NO WAY')
    #test bypass
    for i in range(len(l.doors)):
        l.set_cell(' ', l.doors[i])
        solution = l.simple_solve()
        if solution != None and len(solution) != 0:
            print('BYPASS!')
            l.draw_solution() #TODO: pass solution to draw_solution
        l.set_cell('+', l.doors[i])

def main():
    kw = {'ai': False, 'rooms': False, 'keys': False, 'fog': False}
    for i in sys.argv[1:]:
        if i in kw.keys():
            kw[i] = True
    ai = kw.pop('ai')
    if ai:
        play_ai(**kw)
    else:
        play_local(**kw)

if __name__ == '__main__':
    import sys
    #c = Config(6)
    #l = Labyrinth(c, ((int(79*2.5)//2 | 1),int(25*2.5)|1) )
    #print(l.draw_to_str())
    main()

