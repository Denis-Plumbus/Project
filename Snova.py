import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Установка размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Поймай звезды")

# Параметры платформы
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (207, 0, 148)
PLATFORM_SPEED = 10

# Параметры звезд
STAR_SIZE = 30
STAR_SPEED = 4
STAR_COUNT = 4

# Функция для загрузки изображений из папки data
def load_image(filename):
    return pygame.image.load(os.path.join('data', filename)).convert()

# Загрузка и масштабирование фонового изображения
background_image = load_image("fon.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLATFORM_WIDTH, PLATFORM_HEIGHT])
        self.image.fill(PLATFORM_COLOR)
        self.image.set_colorkey((0, 0, 0))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT

    # Метод для движения платформы
    def move(self, direction):
        if direction == "left":
            self.rect.x -= PLATFORM_SPEED
        elif direction == "right":
            self.rect.x += PLATFORM_SPEED
        # Ограничение движения платформы по горизонтали
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - PLATFORM_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLATFORM_WIDTH

# Класс звезды
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('star.png')
        self.image = pygame.transform.scale(self.image, (STAR_SIZE, STAR_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - STAR_SIZE)
        self.rect.y = random.randint(-SCREEN_HEIGHT, 0)
        self.speedy = STAR_SPEED

    # Метод для обновления положения звезды
    def update(self):
        self.rect.y += self.speedy
        # Перемещение звезды вверх и случайное положение, если она вышла за пределы экрана
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-SCREEN_HEIGHT, 0)
            self.rect.x = random.randint(0, SCREEN_WIDTH - STAR_SIZE)
            global missed_stars
            missed_stars += 1

# Группы спрайтов
all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
# Создание экземпляра платформы и добавление ее в группу спрайтов
platform = Platform()
all_sprites.add(platform)

# Создание звезд и добавление их в группу спрайтов
for _ in range(STAR_COUNT):
    star = Star()
    all_sprites.add(star)
    stars.add(star)

# Переменные для отслеживания результатов игры
caught_stars = 0
missed_stars = 0
stars_for_win = 26  # Изначальное количество звезд для победы

# Функция для отображения текста на экране
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Функция для отображения экрана ввода
def show_intro_screen():
    SCREEN.blit(background_image, [0, 0])
    draw_text(SCREEN, "Нажмите кнопку мыши, чтобы начать", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (255, 255, 255))
    pygame.display.flip()

# Функция для отображения меню
def show_menu(result=None):
    SCREEN.blit(background_image, [0, 0])
    if result == "win":
        draw_text(SCREEN, "Вы выиграли!", 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, (255, 255, 255))
    elif result == "lose":
        draw_text(SCREEN, "Вы проиграли!", 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, (255, 255, 255))
    draw_text(SCREEN, f"Пойманных звезд: {caught_stars}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (255, 255, 255))
    draw_text(SCREEN, f"Пропущенных звезд: {missed_stars}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, (255, 255, 255))
    pygame.draw.rect(SCREEN, (0, 255, 0), (300, 400, 200, 50))
    draw_text(SCREEN, "Перезапустить", 30, 400, 425, (255, 255, 255))
    pygame.display.flip()

# Функция для перезапуска игры
def restart_game():
    global caught_stars, missed_stars, game_over, platform, stars_for_win
    caught_stars = 0
    missed_stars = 0
    game_over = False
    all_sprites.empty()
    stars.empty()
    for _ in range(STAR_COUNT):
        star = Star()
        all_sprites.add(star)
        stars.add(star)
    platform = Platform()
    all_sprites.add(platform)
    stars_for_win += 4  # Увеличиваем количество звезд для победы

# Переменные для управления основным игровым циклом
running = True
clock = pygame.time.Clock()
intro = True
game_over = False
result = None
level = 1
missed_stars_for_lose = 13

# Основной игровой цикл
while running:
    if intro:
        show_intro_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                intro = False
    elif game_over:
        show_menu(result)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                    restart_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Управление платформой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            platform.move("left")
        if keys[pygame.K_RIGHT]:
            platform.move("right")
        # Обновление положения всех спрайтов
        all_sprites.update()
        # Проверка столкновений звезды с платформой
        hits = pygame.sprite.spritecollide(platform, stars, False)
        for hit in hits:
            hit.rect.y = random.randint(-SCREEN_HEIGHT, 0)
            hit.rect.x = random.randint(0, SCREEN_WIDTH - STAR_SIZE)
            caught_stars += 1
        # Проверка условий победы и поражения
        if missed_stars >= missed_stars_for_lose:
            game_over = True
            result = "lose"
        elif caught_stars >= stars_for_win:
            game_over = True
            result = "win"
            level += 1
            missed_stars_for_lose -= 1
        # Отображение всех спрайтов и текста на экране
        SCREEN.blit(background_image, [0, 0])
        all_sprites.draw(SCREEN)
        draw_text(SCREEN, f"Пойманные: {caught_stars}", 30, 75, 20, (255, 255, 255))
        draw_text(SCREEN, f"Упавшие: {missed_stars}", 30, 65, 50, (255, 255, 255))
        draw_text(SCREEN, f"Уровень: {level}", 30, SCREEN_WIDTH - 100, 20, (255, 255, 255))
        pygame.display.flip()
        clock.tick(60)

# Завершение работы Pygame
pygame.quit()
