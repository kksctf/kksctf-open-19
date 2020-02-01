

class GameError(Exception):
    pass

class Field():
    #__charset = '# @!_k+~-' #wall empty player target visited key door fog path

    ########
    ##init##
    def __init__(self, size = (79//2, 25), empty = ' ', wall = '#', **kwargs): #walkable = ' _k', unwalkable = '#+'):
        '''kwargs:
            walkable = ' '
            unwalkable = '#'
            '''
        self.size = size
        self.walkable = empty
        self.unwalkable = wall
        for i in kwargs.keys():
            if i == 'walkable':
                self.walkable = (empty if not empty in kwargs[i] else '') + kwargs[i]
            elif i == 'unwalkable':
                self.unwalkable = (wall if not wall in kwargs[i] else '') + kwargs[i]
            else:
                raise ValueError('Field init: unknown argument: {}'.format(i))

        #self.player_coords = [1,1]
        #self.exit_coords = (self.size[0]-2, self.size[1]-2)
        self.field = [ [self.unwalkable[0]]*self.size[0] ] * self.size[1]

    ########
    ##util##
    def set_char_in_line(self, s, pos, toins):
        s = s[:pos] + toins + s[pos+1:]
        return s

    def set_str_in_line(self, s, pos, toins):
        s = s[:pos] + toins + s[pos+len(toins):]
        return s

    def set_cell(self, tile, *args):
        '''__set_cell(self, coords_tuple)\n__set_cell(self, x, y)'''
        if not (tile in self.walkable or tile in self.unwalkable):
            raise ValueError('__set_cell: tile is not in charset')
        if len(args) == 2:
            if type(args[0]) != int or type(args[1]) != int:
                raise TypeError('__set_cell: x and y must have type int')
            coords = (args[0], args[1])
        elif len(args) == 1:
            if (len(args[0]) != 2) or (type(args[0][0]) != int) or (type(args[0][1]) != int):
                raise TypeError('__set_cell: coords must be tuple(int, int)')
            coords = args[0]
        elif len(args) > 2:
            raise TypeError('__set_cell expected at most 4 arguments, got {}'.format(len(args)+2))
        else:
            raise TypeError('__set_cell expected at least 3 arguments, got {}'.format(2))
        self.field[coords[1]] = self.field[coords[1]][:coords[0]] + tile + self.field[coords[1]][coords[0]+1:] #TODO: replace with __set_char_in_line

    def get_cell(self, *args):
        '''get_cell(self, coords_tuple)\nget_cell(self, x, y)'''
        if len(args) == 2:
            if type(args[0]) != int or type(args[1]) != int:
                raise TypeError('get_cell: x and y must have type int')
            coords = (args[0], args[1])
        elif len(args) == 1:
            if (len(args[0]) != 2) or (type(args[0][0]) != int) or (type(args[0][1]) != int):
                raise TypeError('get_cell: coords must be tuple(int, int)')
            coords = args[0]
        elif len(args) > 2:
            raise TypeError('get_cell expected at most 3 arguments, got {}'.format(len(args)+1))
        else:
            raise TypeError('get_cell expected at least 2 arguments, got {}'.format(1))
        if coords[0] < 0 or coords[1] < 0 or coords[0] >= self.size[0] or coords[1] >= self.size[1]:
            raise GameError('get_cell: coords outside of field')
        return self.field[coords[1]][coords[0]]

    ##########
    ##checks##
    def is_wall(self, *args):
        '''is_wall(self, coords_tuple)\nis_wall(self, x, y)'''
        try:
            cell = self.get_cell(*args)
        except GameError:
            return True
        #TODO: closed door == wall
        return cell in self.unwalkable

    def drawing_line_extra(self, cur_line, i, **kwargs):
        return cur_line

    def draw_to_str(self, **kwargs):
        res = ''

        for i in range(len(self.field)):
            cur_line = self.field[i]

            cur_line = self.drawing_line_extra(cur_line, i, **kwargs)

            for j in set(cur_line):
                cur_line = cur_line.replace(j, j*2)

            if i != len(self.field)-1:
                cur_line += '\n'

            res += cur_line

        return res

    def draw(self):
        print(self.draw_to_str())

