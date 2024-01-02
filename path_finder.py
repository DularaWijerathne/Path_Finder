import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
]


def print_maze(maze, stdscr, goal, path=[]):
    blue_black = curses.color_pair(1)
    red_black = curses.color_pair(2)
    green_black = curses.color_pair(3)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, ".", red_black)
            elif value == goal:
                stdscr.addstr(i, j * 2, value, green_black)
            else:
                stdscr.addstr(i, j * 2, value, blue_black)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


def find_path(maze, stdscr):
    start = "O"
    goal = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, goal, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == goal:
            return path

        neighbours = find_neighbors(maze, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue  # if the neighbour is in visted set, then end the current iteration and continue to next iteration

            r, c = neighbour
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)


def find_neighbors(maze, row, col):
    neighbours = []

    if row > 0:  # UP
        neighbours.append((row - 1, col))
    if row < len(maze):  # DOWN
        neighbours.append((row + 1, col))
    if col > 0:  # LEFT
        neighbours.append((row, col - 1))
    if col < len(maze[0]):  # RIGHT
        neighbours.append((row, col + 1))

    return neighbours


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()  # get character - similar as 'input()' in python


wrapper(main)
# Here we are passing the 'main' function, not calling it. This initialize the curses model, then call the function and then passes the 'stdscr' object.
