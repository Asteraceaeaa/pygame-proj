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

screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()

running = True
state = 0
states = ["МЕНЮ", "ВЫБОР УРОВНЯ", ["Уровень 1", "Уровень 2", "Уровень 3"], ["Вы проиграли!", "Пауза", "Вы выиграли!"]]
cur_level = 0

while running:

    if state == 0:
        # MENU
        print(f"Текущий статус: {states[state]}")
        menu = True

        options = ["Начать игру", "Выход"]
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

            WIDTH_RESIZABLE = screen.get_width()
            HEIGHT_RESIZABLE = screen.get_height()

            title = font_b.render(states[state], True, "White")
            title_rect = title.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//4))
            screen.blit(title, title_rect)

            for i, option in enumerate(options):
                color = "Yellow" if i == selected else "White"
                text = font_s.render(option, True, color)
                rect = text.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//2.5 + i * 50))
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


            # Отрисовка
            screen.fill("Black")

            WIDTH_RESIZABLE = screen.get_width()
            HEIGHT_RESIZABLE = screen.get_height()

            if state != 1: break
            title = font_b.render(states[state], True, "White")
            title_rect = title.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//4))
            screen.blit(title, title_rect)

            for i, option in enumerate(options):
                color = "Yellow" if i == selected else "White"
                text = font_s.render(option, True, color)
                rect = text.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//2.5 + i * 50))
                screen.blit(text, rect)

            pg.display.flip()
            clock.tick(60)

    if state == 2:
        substate = -1
        print(f"Выбрано: {states[state][cur_level]}")
        game = True
        alive = True

        # Переменные для паузы (добавьте в начало игры)
        pause = False
        pause_selected = 0
        pause_options = ["Продолжить", "Начать заново", "Выйти в меню"]


        hero_x = screen.get_width() // 2
        hero_y = screen.get_height() // 2
        hero_speed = 5
        facing_right = True  # True - смотрит вправо, False - влево

        hero_right_img = pg.image.load("assets/hero/frame_028.png")
        hero_left_img = pg.image.load("assets/hero/frame_016.png")
        hero_right_img = pg.transform.scale(hero_right_img, (50, 50))
        hero_left_img = pg.transform.scale(hero_left_img, (50, 50))

        enemy = pg.Surface((100, 100))
        enemy.fill("Red")

        while game:
            # Вместо вашего пустого while pause:
            WIDTH_RESIZABLE = screen.get_width()
            HEIGHT_RESIZABLE = screen.get_height()

            # В игровом цикле замените пустой while pause на:
            if pause:
                # Рисуем затемненный фон
                dark_overlay = pg.Surface((WIDTH_RESIZABLE, HEIGHT_RESIZABLE))
                dark_overlay.set_alpha(180)
                dark_overlay.fill((0, 0, 0))
                screen.blit(dark_overlay, (0, 0))
                
                # Заголовок "ПАУЗА"
                pause_title = font_b.render("ПАУЗА", True, "Yellow")
                title_rect = pause_title.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//4))
                screen.blit(pause_title, title_rect)
                
                # Отрисовка пунктов меню паузы
                for i, option in enumerate(pause_options):
                    color = "Yellow" if i == pause_selected else "White"
                    text = font_s.render(option, True, color)
                    rect = text.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//2 + i * 60))
                    screen.blit(text, rect)
                
                # Обработка событий в меню паузы
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                        game = False
                        pause = False
                    
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            pause_selected = (pause_selected - 1) % len(pause_options)
                        elif event.key == pg.K_DOWN:
                            pause_selected = (pause_selected + 1) % len(pause_options)
                        elif event.key == pg.K_RETURN:
                            if pause_selected == 0:  # Продолжить
                                pause = False
                            elif pause_selected == 1:  # Начать заново
                                # Сброс игры
                                hero_x = WIDTH // 2
                                hero_y = HEIGHT // 2
                                pause = False
                                # Здесь сбросить все переменные уровня
                            elif pause_selected == 2:  # Выйти в меню
                                state = 0
                                game = False
                                pause = False
                        elif event.key == pg.K_ESCAPE:  # Выход из паузы по ESC
                            pause = False
                
                pg.display.flip()
                clock.tick(60)
                continue  # Пропускаем остальную логику игры в этом кадре
            


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game = False
                    running = False
                    state = 0

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pause = True
                        # substate = 2
                    

            """Логика управления"""
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                hero_x -= hero_speed
                facing_right = False
            if keys[pg.K_RIGHT]:
                hero_x += hero_speed
                facing_right = True
            if keys[pg.K_UP]:
                hero_y -= hero_speed
            if keys[pg.K_DOWN]:
                hero_y += hero_speed

            """Логика уровня"""




            screen.fill("Blue")

            screen.blit(enemy, (WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//2))

            if facing_right:
                screen.blit(hero_right_img, (hero_x, hero_y))
            else:
                screen.blit(hero_left_img, (hero_x, hero_y))

            if state != 2: break


            title = font_b.render(states[state][cur_level], True, "White")


            pg.display.flip()  # <-- ОБЯЗАТЕЛЬНО добавь
            clock.tick(60)     # <-- ОБЯЗАТЕЛЬНО добавь


    if state == 3:
        print(f"Текущий статус: {states[state]}")
        game_over = True

        options = ["Начать заново", "Выйти в меню"]
        selected = 0
        while game_over:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = False
                    running = False
                    print("Exit...")
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = 0 if selected == 1 else 1
                    elif event.key == pg.K_DOWN:
                        selected = 1 if selected == 0 else 0
                    elif event.key == pg.K_RETURN:
                        game_over = False
                        state = 2
                        if selected == 1:
                            running = False
                            state = 0
                            print("Exit...")
                            

            WIDTH_RESIZABLE = screen.get_width()
            HEIGHT_RESIZABLE = screen.get_height()

            screen.fill("Black")

            title = font_b.render(states[state], True, "White")
            title_rect = title.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//4))
            screen.blit(title, title_rect)

            for i, option in enumerate(options):
                color = "Yellow" if i == selected else "White"
                text = font_s.render(option, True, color)
                rect = text.get_rect(center=(WIDTH_RESIZABLE//2, HEIGHT_RESIZABLE//2.5 + i * 50))
                screen.blit(text, rect)

            pg.display.flip()
            clock.tick(60)
    

pg.quit()

