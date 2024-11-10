import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Параметры экрана для полноэкранного режима
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PicProjectV1")

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
warning_font = pygame.font.Font(None, 48)

# Текст
title_text = font.render("PicProjectV1", True, RED)
play_text = small_font.render("Играть", True, RED)
exit_text = small_font.render("Выйти", True, RED)
warning_text = warning_font.render("ВНИМАНИЕ! Экраны могут вызвать эпилептические приступы.", True, WHITE)

# Позиции текста
title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
play_rect = play_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
exit_rect = exit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))
warning_rect = warning_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# Флаг для перехода к основному меню после предупреждения
show_warning = True

# Загрузка музыки
pygame.mixer.music.load('./assets/sfx/scary_ambience.mp3')  # Зловещая музыка
pygame.mixer.music.play(-1)

# Основной цикл
while True:
    screen.fill(BLACK)
    
    if show_warning:
        # Анимация предупреждения
        screen.blit(warning_text, warning_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Задержка 3 секунды на предупреждение
        show_warning = False  # Переход к основному меню
        continue

    # Мигающий текст в главном меню
    if random.randint(0, 1):
        screen.blit(title_text, title_rect)

    # Отображение кнопок
    screen.blit(play_text, play_rect)
    screen.blit(exit_text, exit_rect)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                # Запуск игры
                print("Игра началась!")  # Здесь будет переход в основной игровой цикл
            elif exit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    # Обновление экрана
    pygame.display.flip()
    pygame.time.delay(100)
