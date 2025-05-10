#! python3
# -*- utf-8 -*-


import pygame as pg
import thorpy as tp


# List of playable games
GAMES_LIST = [
    "TicTacToe"
    "Checkers<WIP>"
]


def mk_menu(frame):
    
    rect_frame = frame.get_rect()
    
    title = tp.make_text("Michael's Game Chest")
    
    # play menu init
    btns_games = [tp.make_button(name) for name in GAMES_LIST]
    box_play = tp.make_ok_box(btns_games, ok_text="Close")
    btn_play = tp.make_button("Play")
    tp.set_launcher(btn_play, box_play)
    
    # options menu init
    varset = tp.VarSet()
    varset.add('account', value="Enter your name", text="Account Name:")
    btn_options = tp.ParamSetterLauncher.make([varset], "Options", "Options")
    
    btn_quit = tp.make_button("Quit", func=tp.functions.quit_menu_func)
    
    return [btn_play, btn_options, btn_quit]


app = tp.Application(size=(800, 600), caption="MenuTest")
background = tp.Background((200,0,0),
                            elements=[])
box_menu = tp.Box.make(mk_menu(background))

tp.store(background, [box_menu])

menu = tp.Menu(elements=background, fps=45)
menu.play()

app.quit()
