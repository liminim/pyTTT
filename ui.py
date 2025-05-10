#! python3
# -*- utf-8 -*-
#
# ui.py
# initialize and manage user interface for various board games
# By: Michael Richard



try:
    import pygame as pg
    import sys
    from pygame.locals import *
except ImportError as err:
    print('Failed to load module: %s') % (err)
    sys.exit(2)


def init_border(size):
    """Border initialization
    args: size - tuple of size of surface in format (x,y)
    returns: border surface"""
    border = pg.Surface(size)
    return border.convert()


def init_game_area(offset):
    """Game area initialization
    args: offset - offset based on border size
    returns: game_area surface"""
    game_area = pg.Surface(offset)
    game_area = game_area.convert()
    game_area.fill((210,158,68))
    return game_area.convert()

def init_menu_bar(width, height):
    """Menu bar initialization
    args: width - menu bar width
    height - menu bar height
    returns: menu_bar surface"""
    menu_bar = pg.Surface((width, height))
    return menu_bar.convert()


def init_game_board(size):
    """Game board initialization
    args: size - tuple of game board size in format (x,y)
    container - containing surface
    b_size - border size
    returns: game_board surface"""
    game_board = pg.Surface(size)
    return game_board.convert()
