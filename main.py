
import numpy as np
from time import time, ctime
from random import randrange, choice, randint
import pygame, sys
pygame.init()


# colors
YELLOW = (255, 255,   0)
ORANGE = (255, 140,   0)
PURPLE = (127,   0, 255)

# window
SCREEN_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)

WINDOW_SIZE = (SCREEN_SIZE[0]-100, SCREEN_SIZE[1]-100)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Invisible Maze')
window.fill('white')

DISPLAY_SIZE = (1920, 1080)
display = pygame.Surface(DISPLAY_SIZE)

# clock
Clock = pygame.time.Clock()
max_FPS = 10

# events
click = False
mouse_scale_x = display.get_width() / WINDOW_SIZE[0]
mouse_scale_y = display.get_height() / WINDOW_SIZE[1]
mouse_x = int(round(pygame.mouse.get_pos()[0] * mouse_scale_x))
mouse_y = int(round(pygame.mouse.get_pos()[1] * mouse_scale_y))

# maze cell
CASE_SIZE = 20
max_cols = DISPLAY_SIZE[0]//CASE_SIZE #96
max_rows = DISPLAY_SIZE[1]//CASE_SIZE #54

# font / win
font = 'asset\\prstartk.ttf'
ind_font = pygame.font.Font(font, 20)
win_message_img = pygame.font.Font(font, 70).render('YOU WIN !', True, 'green')
time_message_img = pygame.font.Font(font, 45).render('time :', True, 'green')

# menu imgs
title_img = pygame.font.Font(font, 70).render('INVISIBLE MAZE GAME', True, 'black')
choose_ind_img = pygame.font.Font(font, 20).render('Choose Maze Difficulty :', True, 'black')
echap_ind_img = pygame.font.Font(font, 15).render('PRESS [ECHAP] TO QUIT', True, 'black')
indication_img = pygame.image.load('asset\\indication_img.png').convert()
indication_img.set_colorkey('white')

# game const
debug = False


def get_event():
    global click, mouse_x, mouse_y
    click = False
    event_list = pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    mouse_x = int(round(pygame.mouse.get_pos()[0] * mouse_scale_x))
    mouse_y = int(round(pygame.mouse.get_pos()[1] * mouse_scale_y))
    return event_list, keys

def Win():
    global win, time_passed_img
    win = True
    time_passed = ctime(time()-game_start_time)[14:19]
    time_passed_img = pygame.font.Font(font, 55).render(str(time_passed), True, 'green')

def menu():
    easy_button = Button(DISPLAY_SIZE[0]/2, 350, 'EASY', 'green')
    medium_button = Button(DISPLAY_SIZE[0]/2, 475, 'MEDIUM', ORANGE)
    hard_button = Button(DISPLAY_SIZE[0]/2, 600, 'HARD', 'red')
    while True:
       Clock.tick(max_FPS)
       event_list, keys = get_event()
       
       if easy_button.is_pressed():
           return 'easy'
       if medium_button.is_pressed():
           return 'medium'
       if hard_button.is_pressed():
           return 'hard'
       
       display.fill('white')
       display.blit(title_img, (DISPLAY_SIZE[0]/2-title_img.get_width()/2, 75))
       display.blit(choose_ind_img, (DISPLAY_SIZE[0]/2-choose_ind_img.get_width()/2, 250))
       easy_button.draw()
       medium_button.draw()
       hard_button.draw()
       display.blit(echap_ind_img, (10, DISPLAY_SIZE[1]-25))
       display.blit(indication_img, (1225, 675))
       
       display.blit(ind_font.render(str(round(Clock.get_fps()))+' FPS', True, 'green'), (10, 10))
       window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
       pygame.display.update()


class Button():
    def __init__(self, x, y, text, color):
        text_surf = pygame.font.Font(font, 50).render(text, True, color)
        self.image = pygame.Surface((450, 100))
        self.image.fill('white')
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, self.image.get_width(), self.image.get_height()), 4)
        self.image.blit(text_surf, (self.image.get_width()/2-text_surf.get_width()/2+3, self.image.get_height()/2-text_surf.get_height()/2+11))
        self.rect = self.image.get_rect(center=(x,y))
        
    def is_pressed(self):
        if click and self.rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False
    
    def draw(self):
        display.blit(self.image, self.rect)


class Maze():
    vDir = { "Down": (0, +1), "Up": (0, -1), "Left": (-1, 0), "Right": (+1, 0) }
    distance = 30
    
    def generate_maze(self, difficulty):
        if difficulty == 'easy':
            return self.generate_DFS_maze()
        if difficulty == 'medium':
            return self.generate_Prim_maze()
        if difficulty == 'hard':
            return self.generate_Kruskal_maze()
        
    def find_air(self, maze):
        air_cell_list = []
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell:
                    air_cell_list.append((x,y))
        return air_cell_list
    
    def invert_axis(self, maze):
        new_maze = [[False for x in range(len(maze))] for y in range(len(maze[0]))]
        for y in range(len(new_maze)):
            for x in range(len(new_maze[0])):
                new_maze[y][x] = maze[x][y]
        return new_maze
        
    def FindNeighbors_DFS(self, maze_map, c):
        neigh = []
        for d,vd in self.vDir.items():
            x, y = c
            x += vd[0]
            y += vd[1]
            if (0 <= x < max_cols) and (0 <= y < max_rows):
                if not maze_map[y][x]:
                    xv, yv = (x,y)
                    xv += vd[0]
                    yv += vd[1]
                    if (0 <= xv < max_cols) and (0 <= yv < max_rows):
                        if not maze_map[yv][xv]:
                            neigh.append(((x, y), (xv, yv)))
        return neigh
        
    def generate_DFS_maze(self):
        maze_map = [[False for x in range(max_cols)] for y in range(max_rows)]
        bonus_nb = 12
        bonus_list = []
        start_cell = (randrange(max_cols), randrange(max_rows))
        pc = []
        pc.append(start_cell)
        while True:
            event_list, keys = get_event()
            curr_c = pc.pop()
            maze_map[curr_c[1]][curr_c[0]] = True
            pc.append(curr_c)
            v = self.FindNeighbors_DFS(maze_map, curr_c)
            if len(v) > 0:
                idx = randrange(len(v))
                m, vo = v.pop(idx)
                maze_map[m[1]][m[0]] = True
                pc.append(vo)
            else:
                curr_c = pc.pop()
                if curr_c == start_cell:
                    break
            if len(pc) <= 0:
                break
        air_cell_list = self.find_air(maze_map)
        end_find = False
        while not end_find:
            end_cell = choice(air_cell_list)
            if not ((end_cell[0]-start_cell[0] <= self.distance) and (end_cell[1]-start_cell[1] <= self.distance)):
                end_find = True
            else:
                event_list, keys = get_event()
        for i in range(bonus_nb):
            pos_find = False
            while not pos_find:
                pos = choice(air_cell_list)
                if pos != start_cell and pos != end_cell and not pos in bonus_list:
                    bonus_list.append(pos)
                    pos_find = True
                else:
                    event_list, keys = get_event()
        return maze_map, start_cell[0], start_cell[1], end_cell, bonus_list
    
    def find_Kruskal(self, cells, p, q):
        if p != cells[p] or q != cells[q]:
            cells[p], cells[q] = self.find_Kruskal(cells, cells[p], cells[q])
        return cells[p], cells[q]
    
    def generate_Kruskal_maze(self):
        maze = np.tile([[1, 2], [2, 0]], (max_rows // 2, max_cols // 2))
        maze = maze[:-1, :-1]
        bonus_nb = 15
        bonus_list = []
        cells = {(i, j): (i, j) for i, j in np.argwhere(maze == 1)}
        walls = np.argwhere(maze == 2)
        np.random.shuffle(walls)
        for wi, wj in walls:
            if wi % 2:
                p, q = self.find_Kruskal(cells, (wi - 1, wj), (wi + 1, wj))
            else:
                p, q = self.find_Kruskal(cells, (wi, wj - 1), (wi, wj + 1))
            maze[wi, wj] = p != q
            if p != q:
                cells[p] = q
        maze = maze.tolist()
        maze.append([False for i in range(max_cols)])
        for y, row in enumerate(maze):
            maze[y].append(False)
        air_cell_list = self.find_air(maze)
        start_cell = choice(air_cell_list)
        end_find = False
        while not end_find:
            end_cell = choice(air_cell_list)
            if not ((end_cell[0]-start_cell[0] <= self.distance) and (end_cell[1]-start_cell[1] <= self.distance)):
                end_find = True
            else:
                event_list, keys = get_event()
        for i in range(bonus_nb):
            pos_find = False
            while not pos_find:
                pos = choice(air_cell_list)
                if pos != start_cell and pos != end_cell and not pos in bonus_list:
                    bonus_list.append(pos)
                    pos_find = True
                else:
                    event_list, keys = get_event()
        return maze, start_cell[0], start_cell[1], end_cell, bonus_list
    
    def __frontier_prim(self, grid, x, y):
        f = set()
        if x >= 0 and x < max_cols and y >= 0 and y < max_rows:
            if x > 1 and not grid[x-2][y]:
                f.add((x-2, y))
            if x + 2 < max_cols and not grid[x+2][y]:
                f.add((x+2, y))
            if y > 1 and not grid[x][y-2]:
                f.add((x, y-2))
            if y + 2 < max_rows and not grid[x][y+2]:
                f.add((x, y+2))
        return f

    def __neighbours_prim(self, grid, x, y):
        n = set()
        if x >= 0 and x < max_cols and y >= 0 and y < max_rows:
            if x > 1 and grid[x-2][y]:
                n.add((x-2, y))
            if x + 2 < max_cols and grid[x+2][y]:
                n.add((x+2, y))
            if y > 1 and grid[x][y-2]:
                n.add((x, y-2))
            if y + 2 < max_rows and grid[x][y+2]:
                n.add((x, y+2))
        return n

    def __connect_prim(self, grid, x1, y1, x2, y2):
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        grid[x1][y1] = True
        grid[x][y] = True
        return grid
    
    def generate_Prim_maze(self):
        grid = np.zeros((max_cols, max_rows), dtype=bool)
        bonus_nb = 12
        bonus_list = []
        s = set()
        x, y = (randint(0, max_cols - 1), randint(0, max_rows - 1))
        grid[x][y] = True
        fs = self.__frontier_prim(grid, x, y)
        for f in fs:
            s.add(f)
        while s:
            x, y = choice(tuple(s))
            s.remove((x, y))
            ns = self.__neighbours_prim(grid, x, y)
            if ns:
                nx, ny = choice(tuple(ns))
                grid = self.__connect_prim(grid, x, y, nx, ny)
            fs = self.__frontier_prim(grid, x, y)
            for f in fs:
                s.add(f)
        maze = grid.tolist()
        maze = self.invert_axis(maze)
        maze.append([False for i in range(max_cols)])
        for y, row in enumerate(maze):
            maze[y].append(False)
        air_cell_list = self.find_air(maze)
        start_cell = choice(air_cell_list)
        end_find = False
        while not end_find:
            end_cell = choice(air_cell_list)
            if not ((end_cell[0]-start_cell[0] <= self.distance) and (end_cell[1]-start_cell[1] <= self.distance)):
                end_find = True
            else:
                event_list, keys = get_event()
        for i in range(bonus_nb):
            pos_find = False
            while not pos_find:
                pos = choice(air_cell_list)
                if pos != start_cell and pos != end_cell and not pos in bonus_list:
                    bonus_list.append(pos)
                    pos_find = True
                else:
                    event_list, keys = get_event()
        return maze, start_cell[0], start_cell[1], end_cell, bonus_list


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((CASE_SIZE, CASE_SIZE))
        self.image.fill('red')
        self.way = []
        
    def update(self):
        # x axis
        if keys[pygame.K_LEFT]:
            try:
                if maze_map[self.y][self.x-1] and self.x-1 != -1:
                    self.x -= 1
            except:...
        if keys[pygame.K_RIGHT]:
            try:
                if maze_map[self.y][self.x+1]:
                    self.x += 1
            except:...
        if not (self.x, self.y) in self.way:
            self.way.append((self.x, self.y))
        # y axis
        if keys[pygame.K_UP]:
            try:
                if maze_map[self.y-1][self.x] and self.y-1 != -1:
                    self.y -= 1
            except:...
        if keys[pygame.K_DOWN]:
            try:
                if maze_map[self.y+1][self.x]:
                    self.y += 1
            except:...
        if not (self.x, self.y) in self.way:
            self.way.append((self.x, self.y))
        return (self.x, self.y)


# Debug
class Expansion():
    def __init__(self, x, y):
        self.adjacents = [(0,-1), (1,0), (0,1), (-1,0)]
        self.origin = (x, y)
        self.visited = []
        self.currents = [self.origin]
        self.next = []
        
    def expand(self, maze):
        if self.currents:
            self.next = []
            for cell in self.currents:
                for (x, y) in self.adjacents:
                    if cell[0]+x != -1 and cell[1]+y != -1:
                        try:
                            if maze[cell[1]+y][cell[0]+x]:
                                if not (cell[0]+x, cell[1]+y) in self.visited and not (cell[0]+x, cell[1]+y) in self.currents:
                                    self.next.append((cell[0]+x, cell[1]+y))
                        except: ...
                self.currents.remove(cell)
                if not cell in self.visited:
                    self.visited.append(cell)
            for cell in self.next:
                self.currents.append(cell)
        
    def render_expansion(self):
        for (x, y) in self.visited:
            pygame.draw.rect(display, PURPLE, pygame.Rect(x*CASE_SIZE, y*CASE_SIZE, CASE_SIZE, CASE_SIZE))
        for (x, y) in self.currents:
            pygame.draw.rect(display, ORANGE, pygame.Rect(x*CASE_SIZE, y*CASE_SIZE, CASE_SIZE, CASE_SIZE))


try:
    difficulty = menu()
    maze_gen = Maze()
    maze_map, x, y, end_cell, bonus_list = maze_gen.generate_maze(difficulty)
    expa = Expansion(x, y)
    player = Player(x, y)
    see_wall = True
    win = False
    game_start_time = time()
    current_time = time()
    bonus_ti = 14
    
    while True:
        Clock.tick(max_FPS)
        event_list, keys = get_event()
        
        # update game
        if not win:
            current_time = ctime(time()-game_start_time)[14:19]
            player_pos = player.update()
            if player_pos == end_cell:
                Win()
            if player_pos in bonus_list:
                bonus_list.remove(player_pos)
                bonus_ti += 10
                see_wall = True
            if bonus_ti != 0:
                bonus_ti -= 1/10
                if bonus_ti < 0:
                    bonus_ti = 0
            if bonus_ti == 0 and see_wall == True:
                see_wall = False # Debug True
        
        # reset screen
        display.fill('white')
        
        # render map
        if see_wall or win:
            for y, row in enumerate(maze_map):
                for x, cell in enumerate(row):
                    if not cell:
                        pygame.draw.rect(display, 'black', pygame.Rect(x*CASE_SIZE, y*CASE_SIZE, CASE_SIZE, CASE_SIZE))
        
        # debug
        if debug:
            expa.expand(maze_map)
            expa.render_expansion()
        
        # render way
        for (x, y) in player.way:
            pygame.draw.rect(display, YELLOW, pygame.Rect(x*CASE_SIZE, y*CASE_SIZE, CASE_SIZE, CASE_SIZE))
        
        # render bonus
        for (x, y) in bonus_list:
            pygame.draw.rect(display, 'blue', pygame.Rect(x*CASE_SIZE, y*CASE_SIZE, CASE_SIZE, CASE_SIZE))
        
        # render end_cell
        pygame.draw.rect(display, 'green', pygame.Rect(end_cell[0]*CASE_SIZE, end_cell[1]*CASE_SIZE, CASE_SIZE, CASE_SIZE))
        
        # render player
        display.blit(player.image, (player.x*CASE_SIZE, player.y*CASE_SIZE))
        
        # render win message
        if win:
            display.blit(win_message_img, (DISPLAY_SIZE[0]/2-win_message_img.get_width()/2, 150))
            display.blit(time_message_img, (DISPLAY_SIZE[0]/2-time_message_img.get_width()/2, 260))
            display.blit(time_passed_img, (DISPLAY_SIZE[0]/2-time_passed_img.get_width()/2, 330))
        
        # FPS and time indication
        display.blit(ind_font.render(str(round(Clock.get_fps()))+' FPS', True, 'green'), (10, 10))
        display.blit(ind_font.render(str(current_time), True, 'green'), (10, 45))
        
        # update screen
        window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
        pygame.display.update()
        
except Exception as e:
    pygame.quit()
    raise e
