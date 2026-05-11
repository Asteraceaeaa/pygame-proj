import datetime
import socket
import sys

script_name = sys.argv[0]

computer_name = socket.gethostname()

now = datetime.datetime.now()
datetime_str = now.strftime("%d.%m.%Y  %H:%M:%S")  # 12.05.2026  14:25:03

with open("LastRunning(log).txt", "a+") as f:
    f.write(f"File {script_name} launched by {computer_name} at {datetime_str}\n")


"""ИГРА"""

import pygame as pg
# from constants import *

pg.init()

WIDTH = 800
HEIGHT = 600

font_b = pg.font.Font("fonts/Luxembourg1910Ombre.ttf", 100)
font_m = pg.font.Font("fonts/Luxembourg1910Ombre.ttf", 50)
font_s = pg.font.Font("fonts/Luxembourg1910Ombre.ttf", 30)

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

running = True
state = 0 
states = ["МЕНЮ", "ВЫБОР УРОВНЯ", ["Уровень 1", "Уровень 2", "Уровень 3"]]
cur_level = 0
while running:

    if state == 0:
        print(f"Текущий статус: {states[state]}")
        menu = True

        options = ["START GAME", "EXIT"]
        selected = 0
        while menu:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    menu = False
                    running = False
                    print("Exit...")
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = 0 if selected == 1 else 1
                    elif event.key == pg.K_DOWN:
                        selected = 1 if selected == 0 else 0
                    elif event.key == pg.K_RETURN:
                        menu = False
                        state = 1
                        if selected == 1:
                            running = False
                            state = 0
                            print("Exit...")
                            
                            

            screen.fill("Black")

            title = font_b.render(states[state], True, "White")
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
            screen.blit(title, title_rect)

            for i, option in enumerate(options):
                color = "Yellow" if i == selected else "White"
                text = font_s.render(option, True, color)
                rect = text.get_rect(center=(WIDTH//2, HEIGHT//2.5 + i * 50))
                screen.blit(text, rect)

            pg.display.flip()
            clock.tick(60)

    if state == 1:
        print(f"Текущий статус: {states[state]}")

        level_manager = True
        options = ["1 Уровень", "2 Уровень", "3 Уровень", "Вернуться в меню"]
        selected = 0
        while level_manager:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    menu = False
                    running = False
                    print("Exit...")
                
                if event.type == pg.KEYDOWN:
                    
                    if event.key == pg.K_UP:
                        selected -= 1 if selected != 0 else -3
                    elif event.key == pg.K_DOWN:
                        selected += 1 if selected != 3 else -3
                    elif event.key == pg.K_RETURN:
                        level_manager = False
                        state = 2
                        cur_level = selected if selected != 3 else 0
                        
                        if selected == 3:
                            state = 0
                            print("Exit to menu...")
                            
                        # print(selected)

            screen.fill("Black")
            if state != 1: break
            title = font_b.render(states[state], True, "White")
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
            screen.blit(title, title_rect)

            for i, option in enumerate(options):
                color = "Yellow" if i == selected else "White"
                text = font_s.render(option, True, color)
                rect = text.get_rect(center=(WIDTH//2, HEIGHT//2.5 + i * 50))
                screen.blit(text, rect)

            pg.display.flip()
            clock.tick(60)
    if state == 2:
        print(f"Выбрано: {states[state][cur_level]}")
        break

pg.quit()

