import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана для полноэкранного режима
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Part 1: Улица фабрики")
screen_width, screen_height = screen.get_size()

# Загрузка фона и персонажа
background = pygame.image.load('./assets/images/out_fabric.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Загрузка персонажа Кирилла
character_image = pygame.image.load('./assets/characters/kira.png')
initial_size = 500  # Начальный размер персонажа
final_size = 300    # Размер, когда персонаж приближается к фабрике
character = pygame.transform.scale(character_image, (initial_size, initial_size))
character_rect = character.get_rect(midbottom=(screen_width // 2, screen_height - 50))  # Начальная позиция снизу по центру

# Скорость персонажа
speed = 5

# Основной игровой цикл
running = True
while running:
    screen.fill((0, 0, 0))  # Чёрный фон (если фон не будет прорисован)
    screen.blit(background, (0, 0))  # Прорисовка фона

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получение состояния нажатых клавиш
    keys = pygame.key.get_pressed()

    # Движение персонажа только вверх (уменьшение размера) и вниз (увеличение)
    if keys[pygame.K_w] and character_rect.height > final_size:  # W - Вверх (уменьшение размера)
        character_rect.y -= speed  # Перемещение персонажа вверх
        new_size = max(final_size, character_rect.height - 1)  # Уменьшение размера до final_size
        character = pygame.transform.scale(character_image, (new_size, new_size))
        character_rect = character.get_rect(center=character_rect.center)
    elif keys[pygame.K_s] and character_rect.height < initial_size:  # S - Вниз (увеличение размера)
        character_rect.y += speed  # Перемещение персонажа вниз
        new_size = min(initial_size, character_rect.height + 1)  # Увеличение размера до initial_size
        character = pygame.transform.scale(character_image, (new_size, new_size))
        character_rect = character.get_rect(center=character_rect.center)

    # Ограничение перемещения персонажа по вертикали экрана
    if character_rect.top < 0:
        character_rect.top = 0
    if character_rect.bottom > screen_height:
        character_rect.bottom = screen_height

    # Прорисовка персонажа
    screen.blit(character, character_rect)

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Ограничение FPS
