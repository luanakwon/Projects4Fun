from maze import Maze
import cv2
import numpy as np

ESCAPE = 27
NPAD_8 = 56
NPAD_4 = 52
NPAD_6 = 54
NPAD_2 = 50

def get_mazeDraw(mazeView):
    mazeDraw = cv2.resize(mazeView,(348,348),interpolation=cv2.INTER_NEAREST)
    mazeDraw = mazeDraw[48:300,48:300].astype(np.uint8)
    mazeDraw[120:132,120:132]-= 100
    return mazeDraw

myMaze = Maze(21)
pos = myMaze.startpoint
pos = (pos[0]*2+1,pos[1]*2+1)
r = 11

while True:
    mazeView = myMaze.get_view(*pos,r)
    cv2.imshow('Maze2',get_mazeDraw(mazeView))
    if pos == myMaze.endpoint:
        print('escaped!')
        break
    key = cv2.waitKey()
    if key == ESCAPE:
        break
    elif key == NPAD_8:
        # check if up is not wall
        if mazeView[r-1,r] != 0:
            print(f'{key},{pos} move up')
            pos = (pos[0],pos[1]-1)
        else: 
            print(f'{key}, {pos}, wall')
    elif key == NPAD_4:
        # check if up is not wall
        if mazeView[r,r-1] != 0:
            print(f'{key}, {pos}, move left')
            pos = (pos[0]-1,pos[1])
        else: 
            print(f'{key}, {pos}, wall')
    elif key == NPAD_6:
        # check if up is not wall
        if mazeView[r,r+1] != 0:
            print(f'{key}, {pos}, move right')
            pos = (pos[0]+1,pos[1])
        else: 
            print(f'{key}, {pos}, wall')
    elif key == NPAD_2:
        # check if up is not wall
        if mazeView[r+1,r] != 0:
            print(f'{key}, {pos}, move down')
            pos = (pos[0],pos[1]+1)
        else: 
            print(f'{key}, {pos}, wall')
    else:
        print('num pad 8,4,6,2 to move, esc to quit')
        continue

