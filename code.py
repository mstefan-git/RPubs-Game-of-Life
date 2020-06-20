import pygame as pg
import copy
from dataclasses import dataclass

# set parameter values
res  = 800 # pixels
size =  40 # no. of squares per row/col

# load and scale .png-files
black = pg.image.load("img_black.png")
white = pg.image.load("img_white.png")
scale = res // size
black = pg.transform.scale(black,(scale-1,scale-1))
white = pg.transform.scale(white,(scale-1,scale-1))

# Cell class
neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
@dataclass
class Cell():
    
    row : int
    col : int
    is_alive : bool = False
    n_neighbors : int = 0
            
    def countNeighbors(self):
        n = 0
        for pos in neighbors:
            row = self.row + pos[0]
            col = self.col + pos[1]
            if 0 <= row < size and 0 <= col < size:
                cell = matrix[row*size+col]
                if cell.is_alive:
                    n += 1
        self.n_neighbors = n

    def show(self):
        pos = (self.row*scale, self.col*scale)
        if self.is_alive:
            screen.blit(black,pos)
        else:
            screen.blit(white,pos)

# create matrix/grid
matrix = [Cell(i,j) for i in range(size) for j in range(size)]

# empty list in which to store matrix of each round
game_round = 0
previous_rounds = []
 
# run game
pg.init()
screen = pg.display.set_mode([res,res])
while True:
 
    # show screen
    for cell in matrix:
        cell.show()
    pg.display.flip()
       
    # check user action
    for event in pg.event.get():
                
        # user closes screen
        if event.type == pg.QUIT:
            pg.quit()
            break
        
        # user clicks mouse
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseX, mouseY = pg.mouse.get_pos()
            row = mouseX // scale
            col = mouseY // scale
            i = row*size+col
            cell = matrix[i]
            
            # left click to spawn cell
            if pg.mouse.get_pressed()[0]:
                cell.is_alive = True
                
            # right click to kill cell
            if pg.mouse.get_pressed()[2]:
                cell.is_alive = False
                
        # user hits keys
        if event.type == pg.KEYDOWN:
            
            # "right arrow" key for next round
            if event.key == pg.K_RIGHT:
                
                # store current matrix in matrices list
                game_round += 1 
                previous_rounds.append(copy.deepcopy(matrix))
                
                # recount neighbors
                for cell in matrix:
                    cell.countNeighbors()
                        
                # spawn/kill new cells
                for cell in matrix:
                    if cell.is_alive == True and cell.n_neighbors != 2:
                        cell.is_alive = False
                    if cell.is_alive == False and cell.n_neighbors == 3:
                        cell.is_alive = True

            # "left arrow" key for previous round
            if event.key == pg.K_LEFT:
                if game_round > 0:
                    matrix = previous_rounds[-1]
                    del previous_rounds[-1]
                    game_round -= 1

            # "r" for restart
            if event.key == pg.K_r:
                for cell in matrix:
                    cell.is_alive = False
        