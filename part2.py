import pygame
import sys
import time

# Инициализация Pygame
pygame.init()

# Параметры экрана для полноэкранного режима
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Part 2: Внутри фабрики")
screen_width, screen_height = screen.get_size()

# Загрузка фона и персонажей
background = pygame.image.load('./assets/images/in_fabric.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Загрузка персонажа Кирилла
character_image = pygame.image.load('./assets/characters/kira.png')
character_size = 250
character = pygame.transform.scale(character_image, (character_size, character_size))
character_rect = character.get_rect(midleft=(50, screen_height - 150))

# Загрузка проклятого персонажа kiraX
kiraX_image = pygame.image.load('./assets/characters/kiraX.png')
kiraX_size = 400
kiraX = pygame.transform.scale(kiraX_image, (kiraX_size, kiraX_size))
kiraX_rect = kiraX.get_rect(midright=(screen_width - 100, screen_height - 150))

# Загрузка изображения крови
blood_image = pygame.image.load('./assets/effects/blood.png')
blood = pygame.transform.scale(blood_image, (character_size + 100, character_size + 100))

# Звуковые эффекты
try:
    walk_sound = pygame.mixer.Sound('./assets/sfx/walk_in.mp3')
    kiraX_walk_sound = pygame.mixer.Sound('./assets/sfx/kiraX_walk.mp3')
    grab_sound = pygame.mixer.Sound('./assets/sfx/grab.mp3')
    scream_sound = pygame.mixer.Sound('./assets/sfx/scream.mp3')
    pygame.mixer.music.load('./assets/sfx/in_PicX.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Циклическое воспроизведение фоновой музыки
except pygame.error as e:
    print(f"Не удалось загрузить один из звуков: {e}")

# Скорость передвижения
move_speed = 5
kiraX_move_speed = 3
center_reached = False
kiraX_approaching = False
show_blood = False

# Основной игровой цикл
running = True
while running:
    screen.blit(background, (0, 0))  # Прорисовка фона
    screen.blit(kiraX, kiraX_rect)  # Прорисовка kiraX

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Движение Кирилла до центра экрана
    keys = pygame.key.get_pressed()
    if not center_reached:
        if keys[pygame.K_d] and character_rect.centerx < screen_width // 2:
            character_rect.x += move_speed
            if not pygame.mixer.get_busy():
                walk_sound.play(-1)
        else:
            walk_sound.stop()
            if character_rect.centerx >= screen_width // 2:
                center_reached = True
                kiraX_approaching = True

    # Движение kiraX к Кириллу
    if kiraX_approaching and kiraX_rect.left > character_rect.right:
        kiraX_rect.x -= kiraX_move_speed
        if not pygame.mixer.get_busy():
            kiraX_walk_sound.play(-1)
    else:
        kiraX_walk_sound.stop()
        if kiraX_approaching and kiraX_rect.left <= character_rect.right:
            kiraX_approaching = False
            pygame.mixer.music.stop()
            grab_sound.play(-1)  # Проигрывание grab.mp3 циклично

            # Задержка для grab.mp3 перед scream.mp3
            pygame.time.delay(2000)
            grab_sound.stop()
            scream_sound.play()

            # Показ изображения крови и проигрывание scream.mp3 на 1 секунду
            show_blood = True
            blood_rect = blood.get_rect(center=character_rect.center)
            pygame.time.delay(1000)  # Кровь и крик на экране на 1 секунду

            # Черный экран и завершение
            screen.fill((0, 0, 0))
            pygame.display.flip()
            pygame.mixer.stop()
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit()

    # Прорисовка персонажей
    screen.blit(character, character_rect)
    if show_blood:
        screen.blit(blood, blood_rect)

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(60)
