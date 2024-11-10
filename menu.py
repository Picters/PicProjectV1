import pygame
import sys
import subprocess
import random

# Инициализация Pygame
pygame.init()

# Полный экран
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PicProjectV1")
screen_width, screen_height = screen.get_size()

# Цвета
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)

# Загрузка и настройка музыки
pygame.mixer.music.load('./assets/sfx/scary_ambience.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # Циклическое воспроизведение

# Шрифты
font = pygame.font.SysFont('Arial', 74, bold=False)
small_font = pygame.font.SysFont('Arial', 36, bold=False)
warning_font = pygame.font.SysFont('Arial', 48, bold=False)

# Текст
title_text = font.render("PicProjectV1", True, DARK_RED)
play_text = small_font.render("Играть", True, DARK_RED)
exit_text = small_font.render("Выйти", True, DARK_RED)
warning_text = warning_font.render("ВНИМАНИЕ! Экраны могут вызвать эпилептические приступы.", True, WHITE)
headphones_text = warning_font.render("Рекомендуем играть в наушниках", True, WHITE)

# Позиции текста
title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
exit_rect = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))
warning_rect = warning_text.get_rect(center=(screen_width // 2, screen_height // 2))
headphones_rect = headphones_text.get_rect(center=(screen_width // 2, screen_height // 2))

# Флаги для показа предупреждений
show_warning = True
show_headphones_warning = False
menu_active = False  # Блокировка кнопок до появления меню

# Функция для плавного появления и исчезновения текста с обработкой событий
def fade_in_out_text(text_surface, rect, fade_in=True, fade_out=True, delay=50):
    if fade_in:
        for alpha in range(0, 256, 5):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            text_surface.set_alpha(alpha)
            screen.fill(BLACK)
            screen.blit(text_surface, rect)
            pygame.display.flip()
            pygame.time.delay(delay)
    if fade_out:
        for alpha in range(255, -1, -5):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            text_surface.set_alpha(alpha)
            screen.fill(BLACK)
            screen.blit(text_surface, rect)
            pygame.display.flip()
            pygame.time.delay(delay)

# Основной цикл
running = True
while running:
    screen.fill(BLACK)  # Устанавливаем черный фон
    
    if show_warning:
        # Плавное появление и исчезновение предупреждения об эпилепсии
        fade_in_out_text(warning_text, warning_rect, fade_in=True, fade_out=True)
        show_warning = False
        show_headphones_warning = True
        pygame.time.delay(1000)  # Пауза 1 секунда перед вторым предупреждением
        continue

    if show_headphones_warning:
        # Плавное появление и исчезновение предупреждения о наушниках
        fade_in_out_text(headphones_text, headphones_rect, fade_in=True, fade_out=True)
        show_headphones_warning = False
        menu_active = True  # Включение основного меню
        continue

    if menu_active:
        # Эффект мигающего и искажающегося текста заголовка
        if random.randint(0, 1):
            title_font_size = random.randint(70, 80)
            dynamic_font = pygame.font.SysFont('Arial', title_font_size, bold=False)
            title_surf = dynamic_font.render("PicProjectV1", True, DARK_RED if random.randint(0, 1) else RED)
            title_rect = title_surf.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
            screen.blit(title_surf, title_rect)

        # Отображение кнопок
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)

        # Обработка событий, активных только после появления меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and menu_active:
                if play_rect.collidepoint(event.pos):
                    # Переход к черному экрану и параллельный запуск history.py
                    pygame.mixer.music.stop()  # Остановка музыки
                    screen.fill(BLACK)  # Отображение черного экрана
                    pygame.display.flip()
                    
                    # Запуск history.py в параллельном процессе
                    subprocess.Popen(['python', 'history.py'])
                    
                    # Задержка на черном экране 3 секунды
                    pygame.time.delay(5000)

                    pygame.quit()
                    sys.exit()  # Закрытие menu.py после черного экрана
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # Обновление экрана
    pygame.display.flip()
    pygame.time.delay(100)
