import pygame as pg

# Инициализация
pg.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Платформер")
clock = pg.time.Clock()
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)

# Размеры
TILE_SIZE = 40
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_POWER = -15

# Шрифты
font_small = pg.font.Font(None, 36)
font_big = pg.font.Font(None, 72)

# ============ КЛАСС ИГРОКА ============
class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.health = 3
        self.invincible_timer = 0
        self.score = 0
        
    def update(self, platforms, enemies):
        # Неуязвимость
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer % 6 < 3:
                self.image.fill(GRAY)
            else:
                self.image.fill(RED)
        else:
            self.image.fill(RED)
        
        # Горизонтальное движение
        keys = pg.key.get_pressed()
        self.vel_x = 0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = PLAYER_SPEED
        
        # Прыжок
        if (keys[pg.K_UP] or keys[pg.K_SPACE] or keys[pg.K_w]) and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False
        
        # Применение гравитации
        self.vel_y += GRAVITY
        
        # Движение по X с проверкой столкновений
        self.rect.x += self.vel_x
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
        
        # Движение по Y с проверкой столкновений
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        # Проверка выхода за нижнюю границу
        if self.rect.top > SCREEN_HEIGHT:
            self.health = 0
            return False
        
        # Проверка столкновений с врагами
        hits = pg.sprite.spritecollide(self, enemies, False)
        for enemy in hits:
            if self.invincible_timer == 0:
                if self.vel_y > 0 and self.rect.bottom > enemy.rect.top:
                    enemy.kill()
                    self.vel_y = JUMP_POWER / 2
                    self.score += 10
                else:
                    self.health -= 1
                    self.invincible_timer = 60
                    if self.health <= 0:
                        return False
        return True
    
    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

# ============ КЛАСС ПЛАТФОРМЫ ============
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color=BROWN):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# ============ КЛАСС ВРАГА ============
class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, move_range=100):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.start_x = x
        self.move_range = move_range
        self.speed = 2
        self.direction = 1
    
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x > self.start_x + self.move_range:
            self.direction = -1
        elif self.rect.x < self.start_x - self.move_range:
            self.direction = 1
    
    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

# ============ КЛАСС МОНЕТЫ ============
class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE - 15, TILE_SIZE - 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

# ============ КЛАСС ВЫХОДА ============
class Exit(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

# ============ КЛАСС КАМЕРЫ ============
class Camera:
    def __init__(self, width, height):
        self.camera_x = 0
        self.camera_y = 0
        self.width = width
        self.height = height
    
    def update(self, target):
        self.camera_x = target.rect.centerx - SCREEN_WIDTH // 2
        self.camera_y = target.rect.centery - SCREEN_HEIGHT // 2
        
        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_y < 0:
            self.camera_y = 0
        if self.camera_x > self.width - SCREEN_WIDTH:
            self.camera_x = self.width - SCREEN_WIDTH
    
    def apply(self, rect):
        return rect.move(-self.camera_x, -self.camera_y)

# ============ ЗАГРУЗКА УРОВНЕЙ ============
def load_level(level_num):
    platforms = pg.sprite.Group()
    enemies = pg.sprite.Group()
    coins = pg.sprite.Group()
    exits = pg.sprite.Group()
    
    if level_num == 1:
        # Сплошная земля внизу
        for i in range(40):
            platforms.add(Platform(i * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE, BROWN))
        
        # Платформы
        platforms.add(Platform(TILE_SIZE * 2, 500, TILE_SIZE * 3, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 8, 450, TILE_SIZE * 2, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 15, 400, TILE_SIZE * 2, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 22, 350, TILE_SIZE * 2, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 30, 480, TILE_SIZE * 3, TILE_SIZE, BROWN))
        
        # Монеты
        coins.add(Coin(TILE_SIZE * 5, 470))
        coins.add(Coin(TILE_SIZE * 10, 420))
        coins.add(Coin(TILE_SIZE * 17, 370))
        coins.add(Coin(TILE_SIZE * 24, 320))
        coins.add(Coin(TILE_SIZE * 33, 450))
        
        # Выход
        exits.add(Exit(TILE_SIZE * 37, SCREEN_HEIGHT - TILE_SIZE - TILE_SIZE//2))
        
        # Враги
        enemies.add(Enemy(TILE_SIZE * 10, 430, 100))
        enemies.add(Enemy(TILE_SIZE * 25, 460, 120))
        
        player_start = (TILE_SIZE * 2, 470)
        
    elif level_num == 2:
        # Земля
        for i in range(40):
            platforms.add(Platform(i * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE, BROWN))
        
        # Платформы
        platforms.add(Platform(TILE_SIZE * 3, 500, TILE_SIZE * 4, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 12, 450, TILE_SIZE * 3, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 20, 400, TILE_SIZE * 4, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 28, 470, TILE_SIZE * 3, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 33, 380, TILE_SIZE * 2, TILE_SIZE, BROWN))
        
        # Монеты
        for i in range(6):
            coins.add(Coin(TILE_SIZE * (7 + i*3), 420))
        coins.add(Coin(TILE_SIZE * 35, 350))
        
        # Выход
        exits.add(Exit(TILE_SIZE * 36, SCREEN_HEIGHT - TILE_SIZE - TILE_SIZE//2))
        
        # Враги
        enemies.add(Enemy(TILE_SIZE * 8, 430, 150))
        enemies.add(Enemy(TILE_SIZE * 18, 380, 100))
        enemies.add(Enemy(TILE_SIZE * 30, 450, 80))
        
        player_start = (TILE_SIZE * 3, 470)
    
    elif level_num == 3:
        # Земля
        for i in range(40):
            platforms.add(Platform(i * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE, BROWN))
        
        # Платформы
        platforms.add(Platform(TILE_SIZE * 3, 500, TILE_SIZE * 3, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 10, 450, TILE_SIZE * 2, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 16, 400, TILE_SIZE * 3, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 23, 350, TILE_SIZE * 2, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 28, 300, TILE_SIZE * 2, TILE_SIZE, BROWN))
        platforms.add(Platform(TILE_SIZE * 33, 470, TILE_SIZE * 4, TILE_SIZE, BROWN))
        
        # Монеты
        for i in range(10):
            coins.add(Coin(TILE_SIZE * (5 + i*3), 470))
        
        # Выход
        exits.add(Exit(TILE_SIZE * 38, SCREEN_HEIGHT - TILE_SIZE - TILE_SIZE//2))
        
        # Враги
        enemies.add(Enemy(TILE_SIZE * 5, 480, 120))
        enemies.add(Enemy(TILE_SIZE * 14, 430, 100))
        enemies.add(Enemy(TILE_SIZE * 20, 380, 150))
        enemies.add(Enemy(TILE_SIZE * 25, 330, 80))
        enemies.add(Enemy(TILE_SIZE * 32, 450, 80))
        
        player_start = (TILE_SIZE * 3, 470)
    
    return platforms, enemies, coins, exits, player_start

# ============ МЕНЮ ============
def show_menu():
    selected = 0
    options = ["START GAME", "EXIT"]
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pg.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pg.K_RETURN:
                    if selected == 0:
                        return True
                    elif selected == 1:
                        return False
        
        screen.fill(BLACK)
        
        title = font_big.render("PLATFORMER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = font_small.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, 300 + i * 50))
            screen.blit(text, rect)
        
        controls = font_small.render("Controls: ARROWS / WASD + SPACE", True, GRAY)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH//2, 500))
        screen.blit(controls, controls_rect)
        
        pg.display.flip()
        clock.tick(FPS)

# ============ ЭКРАН GAME OVER ============
def show_game_over(score):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return True  # Рестарт
                elif event.key == pg.K_q:
                    return False  # Выход в меню
        
        screen.fill(BLACK)
        
        game_over = font_big.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(game_over, game_over_rect)
        
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        screen.blit(score_text, score_rect)
        
        restart_text = font_small.render("Press R to restart  |  Press Q to quit", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 450))
        screen.blit(restart_text, restart_rect)
        
        pg.display.flip()
        clock.tick(FPS)

# ============ ЭКРАН ПОБЕДЫ ============
def show_win_screen(score):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return True  # Рестарт
                elif event.key == pg.K_q:
                    return False  # Выход в меню
        
        screen.fill(BLACK)
        
        win_text = font_big.render("YOU WIN!", True, GREEN)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(win_text, win_rect)
        
        score_text = font_small.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        screen.blit(score_text, score_rect)
        
        restart_text = font_small.render("Press R to restart  |  Press Q to quit", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 450))
        screen.blit(restart_text, restart_rect)
        
        pg.display.flip()
        clock.tick(FPS)

# ============ ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ============
def game_loop():
    current_level = 1
    total_score = 0
    
    while current_level <= 3:
        # Загрузка уровня
        platforms, enemies, coins, exits, player_start = load_level(current_level)
        player = Player(player_start[0], player_start[1])
        
        # Камера
        level_width = 40 * TILE_SIZE
        camera = Camera(level_width, SCREEN_HEIGHT)
        
        running = True
        level_complete = False
        
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
            
            # Обновление игрока
            alive = player.update(platforms, enemies)
            
            # Если игрок умер
            if not alive:
                result = show_game_over(total_score + player.score)
                if result:  # Нажата R - рестарт
                    return True
                else:  # Нажата Q - выход
                    return False
            
            # Обновление врагов
            enemies.update()
            
            # Сбор монет
            coin_hits = pg.sprite.spritecollide(player, coins, True)
            for coin in coin_hits:
                player.score += 10
                total_score += 10
            
            # Проверка выхода
            exit_hits = pg.sprite.spritecollide(player, exits, False)
            if exit_hits:
                level_complete = True
                running = False
            
            # Обновление камеры
            camera.update(player)
            
            # Отрисовка
            screen.fill(BLACK)
            
            for platform in platforms:
                screen.blit(platform.image, camera.apply(platform.rect))
            
            for enemy in enemies:
                screen.blit(enemy.image, camera.apply(enemy.rect))
            
            for coin in coins:
                screen.blit(coin.image, camera.apply(coin.rect))
            
            for exit in exits:
                screen.blit(exit.image, camera.apply(exit.rect))
            
            screen.blit(player.image, camera.apply(player.rect))
            
            # UI
            health_text = font_small.render(f"Health: {player.health}", True, WHITE)
            screen.blit(health_text, (10, 10))
            
            score_text = font_small.render(f"Score: {total_score + player.score}", True, WHITE)
            screen.blit(score_text, (10, 50))
            
            level_text = font_small.render(f"Level: {current_level}/3", True, WHITE)
            screen.blit(level_text, (10, 90))
            
            controls_text = font_small.render("ESC - Menu", True, GRAY)
            screen.blit(controls_text, (SCREEN_WIDTH - 100, 10))
            
            pg.display.flip()
            clock.tick(FPS)
        
        if level_complete:
            total_score += player.score
            current_level += 1
    
    # Все уровни пройдены
    result = show_win_screen(total_score)
    if result:
        return True  # Рестарт
    else:
        return False  # Выход

# ============ ЗАПУСК ИГРЫ ============
def main():
    while True:
        if show_menu():
            restart = game_loop()
            if not restart:
                break
        else:
            break
    
    pg.quit()

if __name__ == "__main__":
    main()