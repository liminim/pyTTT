#! python3
# -*- utf-8 -*-



# Set static default window size
WIN_SIZE = (800, 600)

# Set width and height of border and calculate offset for contained surfaces
BORDER_SIZE = (16, 16)
BORDER_COLOR = (20,20,20)
BORDER_OFFSET = ((WIN_SIZE[0] - (BORDER_SIZE[0] * 2)), 
    (WIN_SIZE[1] - (BORDER_SIZE[1] * 2)))

# Height of in-game menu. Width will always be the same as the game_area surface.
MENU_HEIGHT = 80
MENU_BG_COLOR = (128,128,128)

# Game area static values
AREA_COLOR = (210,158,68)
GAME_BOARD_SIZE = (400, 400)
GRID_WIDTH = 3
GRID_HEIGHT = 3

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)



try:
    import sys
    import ui
    import grids
    import pygame as pg
    from pygame.locals import *
except ImportError as err:
    print('Failed to load module: %s') % (err)
    sys.exit(2)



def init_ui(screen):
    """UI Initialization"""
    border = ui.init_border(BORDER_SIZE)
    border.fill(BORDER_COLOR)

    game_area = ui.init_game_area(BORDER_OFFSET)
    ga_rect = game_area.get_rect()
    game_area.fill(AREA_COLOR)

    menu_bar = ui.init_menu_bar(game_area.get_width(), MENU_HEIGHT)
    menu_bar_rect = ga_rect
    menu_bar_rect.topleft = (ga_rect.left, (ga_rect.bottom - MENU_HEIGHT))
    menu_bar.fill(MENU_BG_COLOR)

    game_board = ui.init_game_board(GAME_BOARD_SIZE)
    game_board.fill(WHITE)

    game_grid = grids.GameGrid(game_board, GRID_WIDTH, GRID_HEIGHT)
    # Justify game_board area due to rounding in cell width/height division
    new_gb = game_grid.justifySurface(game_board)
    game_board = ui.init_game_board(new_gb.size)
    gb_rect = game_board.get_rect()
    gb_rect.center = ga_rect.center
    game_grid.drawLines(game_board, 5)

    screen.blit(border, (0,0))
    screen.blit(game_area, BORDER_SIZE)
    screen.blit(menu_bar, menu_bar_rect)
    screen.blit(game_board, gb_rect)
    game_grid.draw_grid_all()

    return ({
            'border': border,
            'game_area': game_area,
            'menu_bar': menu_bar,
            'game_board': game_board
            }, game_grid)
    



def main():
    # Pygame and display initialization
    pg.init()
    win_main = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption("pyTTT - Tic Tac Toe in Python")
    containers, game_grid = init_ui(win_main)

    # Initialize sprite groups
    grp_cells = pg.sprite.LayeredDirty()
    game_grid.add_to_group(grp_cells)
    grp_cells.clear(containers['game_board'], containers['border'])
    print(grp_cells.sprites())
    
    clock = pg.time.Clock()
    run = True
    while run:

        clock.tick(60)
        gb_rect = containers['game_board'].get_rect()
        menu_rect = containers['menu_bar'].get_rect()

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

                elif event.type == pg.MOUSEMOTION:
                    pos = event.pos
                    gb_mouseover = gb_rect.collidepoint(pos)
                    menu_mouseover = gb_rect.collidepoint(pos)
                    # Detect if mouse is over game_board surface
                    if gb_mouseover:
                        active_surf = containers['game_board']
                        for cell in game_grid.grid:
                            if cell.rect.collidepoint(pos):
                                cell.mouse_hover = True
                            else:
                                cell.mouse_hover = False

                    # Detect if mouse is over menu_bar surface
                    elif menu_mouseover:
                        active_surf = containers['menu_bar']
                        pass

        update_rects = grp_cells.draw(containers['game_board'])
        pg.display.update(update_rects)


if __name__ == "__main__":
    main()
