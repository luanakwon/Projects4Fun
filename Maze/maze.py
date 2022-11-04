import numpy as np
import random

class Maze:
    def __init__(self, size: int, allow_cycle=False):
        """
        size : size of total maze (size, size)
        allow_cycle: if True, there can be a cyclic graph
                     if False, maze can be described as a tree
        """
        self.size = size
        # maze representation.
        self.maze = np.zeros((size,size),dtype=np.uint8)
        self.startpoint = (size//2,size//2)
        # endpoint
        a = random.randint(0,self.size-1)
        b = random.randint(0,4)
        if b == 0:
            self.endpoint = (1,2*a+1)
        elif b == 1:
            self.endpoint = (2*a+1,2*size-1)
        elif b == 2:
            self.endpoint = (2*size-1,2*a+1)
        else:
            self.endpoint = (2*a+1,1)

        self.build_maze(allow_cycle=allow_cycle,start = self.startpoint)
        self.__mazeView = self.build_view(*self.startpoint,size//2)
        
    def get_repr_code(self,prev_code, my_cor, root_cor):
        """
        0 : not visited
        3 : visited, root from both right n up
        5 : visited, root from both right n left
        9 : visited, root from both right n down
        6 : visited, root from both up n left
        10 : visited, root from both up n down
        12 : visited, root from both left n down
        7 : visited, root from right, up n left
        11 : visited, root from right, up n down
        13 : visited, root from right, left n down
        14 : visited, root from up, left n down
        15 : visited, root from all dir
        16 : starting point
        1***** : endpoint
        """  
        if my_cor[0]-root_cor[0] == -1 and my_cor[1]-root_cor[1] == 0:
            return prev_code+1        # 1 : visited, root from right
        elif my_cor[0]-root_cor[0] == 0 and my_cor[1]-root_cor[1] == 1:
            return prev_code+2        # 2 : visited, root from up
        elif my_cor[0]-root_cor[0] == 1 and my_cor[1]-root_cor[1] == 0:
            return prev_code+4        # 4 : visited, root from left
        elif my_cor[0]-root_cor[0] == 0 and my_cor[1]-root_cor[1] == -1:
            return prev_code+8        # 8 : visited, root from down         

    def build_maze(self,allow_cycle, start):
        # set start
        s_x, s_y = start
        self.maze[s_y,s_x] = 16
        # builder queue
        b_queue = [start]
        while b_queue:
            _x, _y = b_queue.pop()
            next_cell = [(_x+1,_y),(_x,_y-1),(_x-1,_y),(_x,_y+1)]
            # check boundary
            next_cell = [(x,y) for x,y in next_cell \
                if 0 <= x and x < self.size and 0 <= y and y < self.size]
            # if not allow cycle
            if not allow_cycle:
                # remove visited
                next_cell = [(x,y) for x,y in next_cell \
                    if self.maze[y,x] == 0]
                # random pick cells to branch
                next_cell_todo = []
                for i in range(len(next_cell)):
                    p_thres = 1/(2**i)
                    if random.random() < p_thres:
                        idx = random.randint(0,len(next_cell)-1)
                        next_cell_todo.append(next_cell.pop(idx))
                # modify n append picked cells
                for x,y in next_cell_todo:
                    self.maze[y,x] = self.get_repr_code(self.maze[y,x],(x,y),(_x,_y))
                    b_queue.append((x,y))

            if allow_cycle:
                raise NotImplementedError('TODO')   

    def build_view(self,x,y,radius):
        W = 4*radius+3
        blank = np.zeros((W,W),dtype=np.uint8)
        yfrom = max(0,y-radius)
        yfrom_off = (yfrom-(y-radius))*2
        yto = min(self.size,y+radius+1)
        yto_off = ((y+radius+1)-yto)*2
        xfrom = max(0,x-radius)
        xfrom_off = (xfrom-(x-radius))*2
        xto = min(self.size,x+radius+1)
        xto_off = ((x+radius+1)-xto)*2
        maze_crop = self.maze[yfrom:yto,xfrom:xto]

        # middle
        blank[yfrom_off+1:W-yto_off ,xfrom_off+1:W-xto_off][::2,::2] = 1
        # right 0001
        blank[yfrom_off+1:W-yto_off ,xfrom_off+2:W-xto_off+1][::2,::2] += (maze_crop%2)
        # up 0010
        blank[yfrom_off  :W-yto_off-1 ,xfrom_off+1:W-xto_off][::2,::2] += ((maze_crop//2)%2)
        # left 0100
        blank[yfrom_off+1:W-yto_off ,xfrom_off  :W-xto_off-1][::2,::2] += ((maze_crop//4)%2)
        # down 1000
        blank[yfrom_off+2:W-yto_off+1 ,xfrom_off+1:W-xto_off][::2,::2] += ((maze_crop//8)%2)
        
        blank = ((blank>0)*255).astype(np.uint8)
        blank[self.endpoint[1],self.endpoint[0]] = 100

        return blank
        
    def get_view(self,x,y,radius):
        W = 2*radius+1
        blank = np.zeros((W,W),dtype=np.uint8)
        yfrom = max(0,y-radius)
        yfrom_off = (yfrom-(y-radius))
        yto = min(self.size*2+1,y+radius+1)
        yto_off = ((y+radius+1)-yto)
        xfrom = max(0,x-radius)
        xfrom_off = (xfrom-(x-radius))
        xto = min(self.size*2+1,x+radius+1)
        xto_off = ((x+radius+1)-xto)

        blank[yfrom_off:W-yto_off,xfrom_off:W-xto_off] = self.__mazeView[yfrom:yto,xfrom:xto]
        return blank

