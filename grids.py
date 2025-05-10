#! python3
# -*- utf-8 -*-
#
# screens.py - by: Michael Richard
# Module for handling screens in pygame projects



# RGB colors
WHITE = (255,255,255)
RED = (255,0,0)
AQUA = (0,255,255)
SILVER = (192,192,192)


try:
    import sys
    import pygame as pg
    from pygame.locals import *
except ImportError as err:
    print('Failed to load module: %s') % (err)
    sys.exit(2)



class Cell(pg.sprite.DirtySprite):
    """Handles individual cells in GameGrid() grids as sprites
    args: rect - Rect object that cell will be assigned to;
    gridx, gridy - x and y positions relating to grid starting from top left;
    color - default color fill of cell"""   
    def __init__(self, rect, gridx, gridy, 
            color=SILVER, sel_color=AQUA, multi_sel=False):
        super().__init__()
        self.image = pg.Surface(rect.size)
        self.rect = self.image.get_rect()
        self.color = color
        self.select_color = sel_color
        self.mouse_hover = False
        self.selected = False
        self.cell_draw()
        self.image.convert()


    def update(self):
        pass


    def cell_draw(self):
        if self.selected:
            self.image.fill(self.select_color)
        else:
            self.image.fill(self.color)
        self.dirty = 1


    def select_cell(self):
        self.selected = not self.selected
        self.cell_draw()


    def cell_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.mouse_hover = not self.mouse_hover
            self.cell_draw()



class GameGrid():
    """ Create interactive grid for gameplay """
    def __init__(self, container, width, height, margin=0, multi_sel=False):
        self.container_rect = container.get_rect()
        self.width = width
        self.height = height
        self.margin = margin
        self.multi_select = multi_sel
        self.initGrid()


    def initGrid(self):
        """ Calculate grid size based on given width and height and 
        store in a list of rects"""
        self.grid = []
        c_size = self.container_rect.size
        self.cell_size = (((c_size[0] // self.width)), 
                                (c_size[1] // self.height))
        cs = self.cell_size

        for y in range(self.height):
            for x in range(self.width):
                rect = pg.Rect((x * cs[0]), (y * cs[1]), cs[0], cs[1])
                self.grid.append(Cell(rect,x,y))


    def justifySurface(self, surf):
        """justifies containing surface due to round down in cell calculation
        Returns: justified Rect of <serf>"""
        s_rect = surf.get_rect()
        new_width = self.cell_size[0] * self.width
        new_height = self.cell_size[1] * self.height
        s_rect = pg.Rect(s_rect.x, s_rect.y, new_width, new_height)
        self.container_rect = s_rect

        return s_rect


    def drawLines(self, surf, width, color=(0,0,0)):
        """Draws lines seperating each cell (Does not add lines to containing surface)"""
        con = self.container_rect.size
        line_x = {'start':[], 'end':[]}
        line_y = {'start':[], 'end':[]}
        
        for cell in self.grid:
            c_rect = cell.rect
            # Collect coords for lines along x axis
            if c_rect.x == 0 and (c_rect.y != 0 and c_rect.y != con[1]):
                line_x['start'].append(c_rect.topleft)

            if (c_rect.topright[0] == con[0] and 
                    (c_rect.topright[1] != 0 and c_rect.topright[1] != con[1])):
                line_x['end'].append(c_rect.topright)

            # Collect coords for lines along y axis
            if c_rect.y == 0 and (c_rect.x != 0 and c_rect.y != con[1]):
                line_y['start'].append(c_rect.topleft)
            
            if (c_rect.bottomleft[1] == con[1] and 
                    (c_rect.bottomleft[0] != 0 and c_rect.bottomleft[0] != con[0])):
                line_y['end'].append(c_rect.bottomleft)

        # Draw lines
        for i in line_x['start']:
            pg.draw.line(surf, color, line_x['start'][i], line_x['end'][i], width)
        
        for i in line_y['start']:
            pg.draw.line(surf, color, line_y['start'][i], line_y['end'][i], width)          
        

    def set_selections(self, cell):
        if not self.multi_select:
            for c in self.grid:
                c.selected = False
        cell.select_cell()


    def draw_grid_all(self):
        for c in self.grid:
            c.cell_draw()


    def add_to_group(self, group):
        for c in self.grid:
            group.add(c)
