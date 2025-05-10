#! python3
# -*- utf-8 -*-
#
# screens.py - by: Michael Richard
# Module for handling screens in pygame projects


# Set static default window size
WIN_SIZE = (700, 700)

# Set width and height of border and calculate offset for contained surfaces
BORDER_SIZE = (24, 24)
BORDER_OFFSET = ((WIN_SIZE[0] - (BORDER_SIZE[0] * 2)), 
    (WIN_SIZE[1] - (BORDER_SIZE[1] * 2)))

# Height of in-game menu. Width will always be the same as the game_area surface.
MENU_HEIGHT = 80
GAME_BOARD_SIZE = (WIN_SIZE[0] * 0.4, WIN_SIZE[0] * 0.4)


try:
    import sys
    import pygame as pg
    from pygame.locals import *
except ImportError as err:
    print('Failed to load module: %s') % (err)
    sys.exit(2)



class GameGrid():
    """ Create interactive grid for gameplay """
    def __init__(self, gb_rect, width, height, margin):
        self.gb_rect = gb_rect
        self.width = width
        self.height = height
        self.margin = margin
        self.initGrid()

    def initGrid(self):
        self.grid = []
        gb_size = self.gb_rect.size
        m = self.margin

        self.cell_size = (((gb_size[0] // self.width)),
                          (gb_size[1] // self.height))
        cs = self.cell_size
        for y in range(self.height):
            for x in range(self.width):
                self.grid.append(pg.Rect((x * cs[0]), (y * cs[1]), 
                    cs[0], cs[1]))

    def drawGrid(self, surf, color=None):
        for cell in self.grid:
            pg.draw.rect(surf, color, cell)


def mkSurface(xy, color=None):
    """Make new surfaces with dimensions x and y
    Returns: Surface object"""
    return pg.Surface(xy)

def fillSurface(surf, color, rect=None):
    """Fill Surface objects with solid color.
    Include a rect to only fill a portion"""
    if rect is not None:
        surf.fill(color, rect)
    else:
        surf.fill(color)

"""
def fillGameBoard(surf):
    \"""Fill game_board Surface with Subsurfaces
    Returns: list of Subsurfaces\"""
    subs = []
    ga_surf = surf
    side = ga_surf.get_width() // 3
    
    for i in range(3):
        for j in range(3):
            sub = mkSurface((side,side))
            ga_r = ga_surf.get_rect()
            sub_rect = pg.Rect((ga_r.left + j*side, ga_r.top + i*side), (side, side))
            fillSurface(sub, (66, (188 - (i*20)), 167))
            subs.append((sub, sub_rect))
    
    return subs
"""

def doBlit(src, dest, area=None):
    """Commit blit of <src> to Surface object <surf> at location <dest>
    Returns: Rect object"""
    window = pg.display.get_surface()
    return window.blit(src, dest, area)

def main():
    # Pygame and display initialization
    pg.init()
    win_main = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption("pyTTT - Tic Tac Toe in Python")

    # Border initialization
    border = mkSurface(WIN_SIZE)
    border = border.convert()
    fillSurface(border, (10,10,10))

    # Game area initialization
    game_area = mkSurface(BORDER_OFFSET)
    game_area = game_area.convert()
    game_area_rect = game_area.get_rect()
    fillSurface(game_area, (210,158,68))

    # Menu bar initialization
    menu_bar = mkSurface((game_area.get_width(), MENU_HEIGHT))
    menu_bar = menu_bar.convert()
    menu_bar_pos = (BORDER_SIZE[0], (WIN_SIZE[1] - BORDER_SIZE[1]) - MENU_HEIGHT)
    fillSurface(menu_bar, (128,128,128))

    # Game board initialization
    game_board = mkSurface(GAME_BOARD_SIZE)
    game_board = game_board.convert()
    game_board_rect = game_board.get_rect()
    fillSurface(game_board, (255,255,255))

    area_center = game_area_rect.center
    game_board_rect.center = (area_center[0] + BORDER_SIZE[0], area_center[1] - 20)

    # TEST: testing symmetry of game_area
    """
    pg.draw.line(game_area, (10,10,10), (0, area_size[1]/2), 
        (WIN_SIZE[0], area_size[1]/2))
    pg.draw.line(game_area, (10,10,10), (area_size[0]/2, 0), 
        (area_size[0]/2, WIN_SIZE[1]))
    """

    # Blitting
    doBlit(border, (0,0))
    doBlit(game_area, BORDER_SIZE)
    doBlit(menu_bar, menu_bar_pos)
    doBlit(game_board, game_board_rect)

    # Game board grid initialization
    game_grid = GameGrid(game_board_rect, 3, 3, 4)
    game_grid.drawGrid(game_board, color=(0,0,255))

    gbs = game_board.get_size()
    gcs = game_grid.cell_size

    pg.draw.line(game_board, (10,10,10), (0, 0 + gcs[1]),
        (gbs[0], 0 + gcs[1]), 4)
    pg.draw.line(game_board, (10,10,10), (0, gbs[1] - gcs[1]),
        (gbs[0], gbs[1] - gcs[1]), 4)
    pg.draw.line(game_board, (10,10,10), (0 + gcs[0], 0),
        (0 + gcs[0], gbs[1]), 4)
    pg.draw.line(game_board, (10,10,10), (gbs[0] - gcs[0], 0),
        (gbs[0] - gcs[0], gbs[1]), 4)
    doBlit(game_board, game_board_rect)

    pg.display.flip()


    while 1:
        for event in pg.event.get():
            if event.type == QUIT:
                return

        pg.display.flip()


if __name__ == "__main__":
    main()

pg.quit()
