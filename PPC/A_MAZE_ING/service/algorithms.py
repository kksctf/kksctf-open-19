import sys, time
from collections import deque, namedtuple
from graph import Graph

State = namedtuple('State', ('cur', 'last_vert', 'last_dir', 'last_cell'))

_offsets = list(zip([0,0,-1,1], [-1,1,0,0]))
_directions = dict(zip(_offsets, 'udlr')) ; _directions[(0,0)] = ''
def _get_nearest_list(cell):
    return [(cell[0]+j[0], cell[1]+j[1]) for j in _offsets]

def get_direction(st, end):
    try:
        return _directions[ (end[0] - st[0], end[1] - st[1]) ]
    except KeyError:
        if abs(st[0]-end[0]) > 1 or abs(st[1]-end[1]) > 1: raise ValueError('st and end must be neighbors')
        if (abs(st[0]-end[0]) == 1) == (abs(st[1]-end[1]) == 1):
            raise ValueError('x and y cannot be non-zero at one time')


def generate_graph(field, start, end, ignored = [], debug = False):
    states = [ [ None for j in range(field.size[1]) ] for i in range(field.size[0]) ]
    visited = [ [ False for j in range(field.size[1]) ] for i in range(field.size[0]) ] #step

    g = Graph()
    g.add_vert(start)
    g.add_vert(end)

    q = deque([State(start, start, '', start)])
    while q:
        #get next cell, set it's state
        st = q.popleft()
        states[st.cur[0]][st.cur[1]] = st
        visited[st.cur[0]][st.cur[1]] = True

        if debug:
            #draw
            print()
            field.set_cell('@', st.cur)
            field.draw()
            field.set_cell('-', st.cur)
            time.sleep(0.03)

        is_end = (st.cur == end)

        #check all nearest
        nearest_list = _get_nearest_list(st.cur)
        near = []
        near_unvisited = []
        for i in nearest_list: #[(cur[0]+j[0], cur[1]+j[1]) for j in zip([0,0,-1,1], [-1,1,0,0])]:
            if not field.is_wall(i) and not i in ignored:
                near.append(i)
                if not visited[i[0]][i[1]]:
                    near_unvisited.append(i)
        is_junction = (len(near) > 2)

        #add verticle (avoid 1st)
        if (is_junction or st.cur == end) and st.cur != start:
            g.add_vert(st.cur)
            g.add_edge_by_values( st.last_vert, st.cur, st.last_dir, get_direction(st.cur, st.last_cell) )
            if debug: print('ADDING edge on NEW junction:', g.edge_ctr-1, g.edges[g.edge_ctr-1], st)



        #add edges
        for i in near:
            #1.
            if (len(near_unvisited) == 0 or is_end or end in near) and not is_junction:
                if i != st.last_vert and g.find_vert(i) != None:
                    g.add_edge_by_values(st.last_vert, i, st.last_dir, get_direction(i, st.cur))
                    if debug: print('ADDING edge found on junction:', g.edge_ctr-1, g.edges[g.edge_ctr-1], st)

            j = states[i[0]][i[1]]
            #2.
            if j != None and j.cur != st.last_cell and g.find_vert(j.cur) == None: #i in [c.cur for c in q]:
                if debug: print('MEET')
                if is_junction:
                    g.add_edge_by_values(st.cur, j.last_vert, get_direction(st.cur, j.cur), j.last_dir)
                else:
                    g.add_edge_by_values(st.last_vert, j.last_vert, st.last_dir, j.last_dir)
                if debug: print('ADDING edge found on opposite path:', g.edge_ctr-1, g.edges[g.edge_ctr-1], st)

            #3.
            if is_junction and j != None and i in g.verts.values():
                g.add_edge_by_values( st.cur, j.cur, get_direction(st.cur, j.cur), get_direction(j.cur, st.cur) )
                if debug: print('ADDING edge to EXISTING vert:', g.edge_ctr-1, g.edges[g.edge_ctr-1], st)

        #debugding cells
        #for i in g.verts.keys():
            #field.set_cell('0123456789abcdefghijklmnopqrstuvwxyz'[i], g.verts[i])

        if is_end:
            if debug: print('end')
            continue

        for i in near_unvisited:
            if i in [c.cur for c in q]: continue
            if len(near) > 2:
                q.append(State(i, st.cur, get_direction(st.cur, i), st.cur))
                if debug: print('junction!', q[-1])
            else:
                q.append(State(i, st.last_vert, st.last_dir if st.last_dir != '' else get_direction(st.cur, i), st.cur))
                if debug: print('straight', q[-1])

    if debug:
        print(g.verts)
        e = g.edges.items()
        for i in sorted(e, key = lambda x: x[1].v1 * len(g.verts) + x[1].v2):
            print(i)
        #for i in g.edges.keys():
        #    print(i, g.edges[i])
        #for i in g.verts.keys():
        #    field.set_cell('0123456789abcdefghijklmnopqrstuvwxyz'[i], g.verts[i])
        print()
        field.draw()

    return g


def test_generate_graph():
    import field
    f = field.Field((15,7), walkable = '-@0123456789abcdefghijklmnopqrstuvwxyz')
    f.field = [
            '#'*15,
            '#             #',
            '###  ###### ###',
            '### ####### ###',
            '### ####### ###',
            '###           #',
            '#'*15
            ]
    g1 = generate_graph(f, (1,1), (8,1), debug = True)
    g1_expected = Graph()
    g1.verts = {0: (1, 1), 1: (8, 1), 2: (3, 1), 3: (3, 2), 4: (4, 1), 5: (11, 5), 6: (11, 1)}
    g1.edges = {0: Graph.Edge(v1=0, v2=2, dir1='r', dir2='l'), 1: Graph.Edge(v1=2, v2=3, dir1='d', dir2='u'), 2: Graph.Edge(v1=2, v2=4, dir1='r', dir2='l'), 3: Graph.Edge(v1=3, v2=4, dir1='r', dir2='d'), 4: Graph.Edge(v1=1, v2=4, dir1='l', dir2='r'), 5: Graph.Edge(v1=3, v2=5, dir1='d', dir2='l'), 6: Graph.Edge(v1=5, v2=6, dir1='u', dir2='d'), 7: Graph.Edge(v1=1, v2=6, dir1='r', dir2='l')}
    #print(g1.verts == g1_expected.verts and g1.edges == g1_expected.edges)
    #print('press enter'); input()
    f.field = [
            '#'*15,
            '#   #         #',
            '# # # ### ### #',
            '#   #       # #',
            '### ### ### # #',
            '###           #',
            '#'*15
            ]
    g2 = generate_graph(f, (1,1), (8,1), debug = True)
    #print('press enter'); input()
    f.field = [
            '#'*15,
            '#   #         #',
            '# # #   # ### #',
            '#   #   #   # #',
            '### ### ### # #',
            '###           #',
            '#'*15
            ]
    g3 = generate_graph(f, (1,1), (8,1), debug = True)
    #print('press enter'); input()

    try:
        import labyrinth
    except Exception as e:
        print(e)
        return
    f = labyrinth.Labyrinth()
    #f.walkable += '0123456789abcdefghijklmnopqrstuvwxyz@-'
    f.walkable += '@-'
    t = time.time()
    g4 = generate_graph(f, (1,1), f.exit_coords, ignored = [(f.exit_coords[0]-2, f.exit_coords[1]-1)], debug = False)
    tt = time.time()
    #print('time:', tt - t)

if __name__ == '__main__':
    test_generate_graph()


