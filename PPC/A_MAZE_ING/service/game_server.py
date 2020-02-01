#!/usr/bin/env python3

import sys
import threading
import socket
import time
import random

import labyrinth
from labyrinth import GameError
import solver

FLAG = "kks{A*_41g0ri7hm_|s_600D_3n0U6h!}"
PORT = 31397
CONNECTED = []
LOCK = threading.Lock()
SOCK = socket.socket()
#NEEDED_CORRECT = 5 # correct solutions needed
NEEDED_CORRECT = 50
MAX_TIME = 300 # maximum time in seconds
MOTD = """

"""

def handler(conn, addr):
    timer = time.time()

    for nc in range(NEEDED_CORRECT):
        solution = ''
        while len(solution) == 0:
            l = labyrinth.Labyrinth(labyrinth.Config(rooms = True, keys = True))
            try: solution = solver.solve_labyrinth(l)
            except: pass
        print(l.draw_to_str())
        print('keys:', l.keys, 'doors:', l.doors)

        correct_len = False
        finished = False
        turns = ''
        time_out = False

        while not time_out and not finished:
            question = l.draw_to_str()
            conn.send(question.encode())
            try:
                s = conn.recv(4096) # getting user input
            except:
                conn.close()
                return

            try:
                ans = s.decode().strip() # handle user input
            except ValueError:
                try:
                    conn.send("Don't even try to trick me\nGo away!\n".encode())
                except:
                    pass
                sys.stderr.write("Value error occured! Input were: {}\nClient: {}\n".format(s, addr))
                conn.close()
                return

            turns += ans
            for i in ans:
                try:
                    l.turn(i)
                except ValueError:
                    try:
                        conn.send("Don't even try to trick me\nGo away!\n".encode())
                    except:
                        pass
                    sys.stderr.write("Value error occured! Input were: {}\nClient: {}\n".format(s, addr))
                    conn.close()
                    return
                except GameError as e:
                    try:
                        conn.send("{}\n".format(e).encode())
                    except:
                        pass
                    sys.stderr.write("Game error occured: {}. Input were: {}\nClient: {}\n".format(e, s, addr))
                    conn.close()
                    return
                except BaseException as e:
                    sys.stderr.write('{}; {}\n'.format(type(e), e))
                    sys.stderr.write("Unknown error.\nClient: {}\nData: {}\n".format(addr, s))
                    conn.close()
                    return

            if l.reached_exit():
                finished = True
                correct_len = (len(turns) <= len(solution))
            time_out = (time.time()-timer >= MAX_TIME)
            #print(correct_len, time_out)

        if not correct_len:
            conn.send("Too many turns for this map. More optimal way exists!\n".encode())
            conn.close() ; return
        if time_out:
            conn.send("Time is up, try again\n".encode())
            conn.close() ; return

    sys.stdout.write("{} successfully solved task\nTime: {}\n".format(addr, round(time.time()-timer, 4)))
    conn.send("Gratz! Your flag is: {}\n".format(FLAG).encode())

    conn.close()
    return

def main():
    SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SOCK.bind(('', PORT))
    SOCK.listen(1)
    print('Listening port', PORT)
    while True:
        conn, addr = SOCK.accept()
        sys.stdout.write("{} connected\n".format(addr))
        conn.send(MOTD.encode())
        threading.Thread(target=handler, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
