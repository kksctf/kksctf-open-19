


def _get_at_c(l, c):
    return l[c[0]][c[1]]

def _set_at_c(l, c, val):
    l[c[0]][c[1]] = val

class Astar:
    def __init__(self, lab):
        self.lab = lab
        self.field = self.lab.field.copy()
        self.chars_walkable = ' k!'
        self.chars_unwalkable = '#+'

        self.on_closed_list = 10

        self.parents = [ [ None for j in range(lab.size[1]+2) ] for i in range(lab.size[0]+2) ]
        self.openlist = [ None for i in range(lab.size[0] * lab.size[1] + 2) ]
        self.whichlist = [ [ None for j in range(lab.size[1]+2) ] for i in range(lab.size[0]+2) ]
        self.opens = [ None for i in range(lab.size[0] * lab.size[1] + 2) ]
        self.fcost = [ None for i in range(lab.size[0] * lab.size[1] + 2) ]
        self.gcost = [ [ None for j in range(lab.size[1]+2) ] for i in range(lab.size[0]+2) ]
        self.hcost = [ None for i in range(lab.size[0] * lab.size[1] + 2) ]

        self.letterpath = ''

    def find_path(self, start, end, banned = []): #*args): #start_x, start_y, target_x = None, target_y = None):
        '''returns string of "udlr" as the way and None if way does not exist
        '''#find_path(self, start_coords, target_coords)\nfind_path(self, start_x, start_y, target_x, target_y)'''
        #if len(args) == 4:
        #    if type(args[0]) != int or type(args[1]) != int or type(args[2]) != int or type(args[3]) != int:
        #        raise TypeError('find_path: start_x, start_y, target_x and target_y must have type int')
        #    c_st = (args[0], args[1])
        #    c_trg = (args[2], args[3])
        #elif len(args) == 2:
        #    if (len(args[0]) != 2) or (type(args[0][0]) != int) or (type(args[0][1]) != int) or (len(args[1]) != 2) or (type(args[1][0]) != int) or (type(args[1][1]) != int):
        #        raise TypeError('find_path: coords must be tuple(int, int)')
        #    c_st = args[0]
        #    c_trg = args[1]
        #else:
        #    raise TypeError('find_path expected 3 or 5 arguments, got {}'.format(len(args)+1))
        c_st = start
        c_trg = end
        on_open_list = 0
        parent_value = [0,0]
        #a = 0
        #b = 0
        c = [0,0]
        m = 0
        u = 0
        v = 0
        temp = 0
        corner = 0
        num_of_open_list_items = 0
        added_gcost = 0
        temp_gcost = 0
        path = 0
        tempx = 0
        path_coords = [0,0]
        path_len = 0
        cell_position = 0
        new_open_list_item_id = 0

        if c_st[0] == c_trg[0] and c_st[1] == c_trg[1]:
            return ''
        #prepare for doors generation, that's more smart
        #if self.lab.is_wall(c_trg):
        #    return None

        #reset values
        if self.on_closed_list > 1000000: #reset whichlist occasionally
            for i in range(len(self.whichlist)):
                for j in range(len(self.whichlist[i])):
                    self.whichlist[i][j] = 0
            self.on_closed_list = 10

        self.on_closed_list += 2
        on_open_list = self.on_closed_list - 1

        _set_at_c(self.gcost, c_st, 0)

        num_of_open_list_items = 1
        self.openlist[1] = 1
        self.opens[1] = list(c_st)

        while True:
            if num_of_open_list_items != 0:
                parent_value = self.opens[self.openlist[1]]
                _set_at_c(self.whichlist, parent_value, self.on_closed_list)

                num_of_open_list_items -= 1 #heap

                self.openlist[1] = self.openlist[num_of_open_list_items + 1]
                v = 1

                while True:
                    u = v
                    if 2*u + 1 <= num_of_open_list_items:
                        if self.fcost[self.openlist[u]] >= self.fcost[self.openlist[2*u]]:
                            v = 2*u
                        if self.fcost[self.openlist[v]] >= self.fcost[self.openlist[2*u+1]]:
                            v = 2*u+1
                    elif 2*u <= num_of_open_list_items:
                        if self.fcost[self.openlist[u]] >= self.fcost[self.openlist[2*u]]:
                            v = 2*u

                    if u != v:
                        self.openlist[u], self.openlist[v] = self.openlist[v], self.openlist[u]
                    else:
                        break
                #
                for c in [ (parent_value[0]+i[0], parent_value[1]+i[1]) for i in zip([0,0,-1,1], [-1,1,0,0]) ]:
                #for b in range(parent_value[1] - 1, parent_value[1] + 2):
                #    for a in range(parent_value[0] - 1, parent_value[0] + 2):
                    if c[0] < 0 or c[1] < 0 or c[0] >= self.lab.size[0] or c[1] >= self.lab.size[0]:
                        continue
                    if _get_at_c(self.whichlist, c) == self.on_closed_list:
                        continue
                    if (self.lab.is_wall(c) and not self.lab.get_cell(c) in self.chars_walkable) or (c in banned):
                        continue

                    corner = False
                    if _get_at_c(self.whichlist, c) != on_open_list:
                        new_open_list_item_id += 1
                        m = num_of_open_list_items + 1
                        self.openlist[m] = new_open_list_item_id

                        self.opens[new_open_list_item_id] = c
                        if abs(c[0] - parent_value[0]) == 1 and abs(c[1] - parent_value[1]) == 1:
                            added_gcost = 14 #not needed
                        else:
                            added_gcost = 10

                        _set_at_c(self.gcost, c, _get_at_c(self.gcost, parent_value) + added_gcost)

                        self.hcost[self.openlist[m]] = 10 * ( abs(c[0] - c_trg[0]) + abs(c[1] - c_trg[1]) )
                        self.fcost[self.openlist[m]] = _get_at_c(self.gcost, c) + self.hcost[self.openlist[m]]
                        _set_at_c(self.parents, c, parent_value)

                        while m != 1:
                            if self.fcost[self.openlist[m]] <= self.fcost[self.openlist[m//2]]:
                                self.openlist[m], self.openlist[m//2] = self.openlist[m//2], self.openlist[m]
                                m = m//2
                            else:
                                break
                        num_of_open_list_items += 1

                        _set_at_c(self.whichlist, c, on_open_list)

                    else:
                        if abs(c[0] - parent_value[0]) == 1 and abs(c[1] - parent_value[1]) == 1:
                            added_gcost = 14 #not needed
                        else:
                            added_gcost = 10
                        temp_gcost = _get_at_c(self.gcost, parent_value) + added_gcost

                        if temp_gcost < _get_at_c(self.gcost, c):
                            _set_at_c(self.parents, c, parent_value)
                            _set_at_c(self.gcost, c, temp_gcost)

                            for x in range(1, num_of_open_list_items+1):
                                if self.opens[self.openlist[x]][0] == c[0] and self.opens[self.openlist[x]][1] == c[1]:
                                    self.fcost[self.openlist[x]] = _get_at_c(self.gcost, c) + self.hcost[self.openlist[x]]

                                    m = x
                                    while m != 1:
                                        if self.fcost[self.openlist[m]] < self.fcost[self.openlist[m//2]]:
                                            self.openlist[m], self.openlist[m//2] = self.openlist[m//2], self.openlist[m]
                                            m = m//2
                                        else:
                                            break
                                    break
                            #
            ##if num_of_open_list_items != 0
            else:
                path = -1 #no path
                return None #break

            if _get_at_c(self.whichlist, c_trg) == on_open_list:
                path = 1 #path found
                break

        ##while True
        if path == 1:
            path_coords = c_trg
            while path_coords[0] != c_st[0] or path_coords[1] != c_st[1]:
                parent = _get_at_c(self.parents, path_coords)
                d = (path_coords[0] - parent[0], path_coords[1] - parent[1])
                self.letterpath += {(0,-1): 'u', (0,1): 'd', (-1,0): 'l', (1,0): 'r'}[d]
                path_coords = parent
                path_len += 1
            self.letterpath = self.letterpath[::-1]
            return self.letterpath
        else:
            return None

