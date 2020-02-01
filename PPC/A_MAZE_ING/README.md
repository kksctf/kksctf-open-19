# A_MAZE_ING


**Category:** PPC 

**Points:** 983 

**Description:**

Do you like rougelike games? Our monsters are decorating a Christmas tree so you can pass without a problem. Except one: you must hurry! Any unnecessary turn can be a reason for being late for holiday!  
  
`nc tasks.open.kksctf.ru 31397`  
  
@servidei9707  
  
P.S. `urld` to move. You can send sequence of turns at one time, ex. `rrddll`

## WriteUp

### Overview

Server sends us a maze on connecting to it with netcat. As usually, `#` means wall and ` ` means empty space.
But there are some another marks: `:(`, `Om`, `{}` and `<>`. If we try to do some turns, we can find that
each 2 characters appears as one cell, `:(` is a player, `{}` acts as wall. But if player steps on `Om` then
it can pass through one `{}` (so this `{}` dissapears).  
`:(` -- player  
`Om` -- key  
`{}` -- door  
`<>` -- exit  

When player reaches target, lew level generated and sent by server. So, as in many PPC tasks, we need to solve
many mazes in limited time.

So what do we need?
1. Parse maze
2. Solve maze :)
3. Repeat

### Parsing a maze

Parsing text with Python is not hard. Firstly, it's better to store one cell as one char, not two.
Secondly, let's find coordinates of all doors and keys, exit and player. This knowledge will provide us
"waypoints" to avoid bruteforcing of all possible paths (but task can be solved this way too).

### Solving a maze

So what's about solving it? I've chosen [A* pathfinding algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm),
which implementation in C++ was stored on my hdd for many years. For generating and solving this task, algorithm
was rewritten in Python.

Solving algorithm steps:
* Simply solve labyrinth with A* if there are no keys, return solution.
* Copy doors and keys arrays to keep them unique for each tested path.
* Find path to first key, save information about this path to an array.
* For each current path, each door and each key:
  *  If reached exit -- do not test current path, remember it.
  *  Find paths for each door that can be reached.
  *  Go to each door and try to find next key.
  *  If key found -- add this path to list of checked paths
  *  Remove current path from list (it is ended or updated with previous step)
* Return shortest path

### Solving the task

So, it's necessary to repeat it many times, until flag is received. There are 50 mazes to solve in 5 minutes, so it's impossible to do by hands.

Flag is `kks{A*_41g0ri7hm_|s_600D_3n0U6h!}`.

-----

Original solution based on task source code:  
[task_solver.py](service/task_solver.py)
