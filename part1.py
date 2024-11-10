import pygame
import sys
import subprocess
import os

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
final_size = 100    # Минимальный размер, к которому уменьшается Кирилл
character_size = initial_size
character = pygame.transform.scale(character_image, (character_size, character_size))

# Позиция персонажа — немного вправо и вверх от центра
character_rect = character.get_rect(midbottom=(screen_width // 2 + 50, screen_height - 100))

# Загрузка и настройка фонового звука улицы
try:
    pygame.mixer.music.load('./assets/sfx/out.mp3')
    pygame.mixer.music.set_volume(0.3)  # Установка громкости
    pygame.mixer.music.play(-1)  # Циклическое воспроизведение
except pygame.error as e:
    print(f"Не удалось загрузить или воспроизвести фоновый звук улицы: {e}")

# Звук шагов Кирилла
try:
    walk_sound = pygame.mixer.Sound('./assets/sfx/walk_out.mp3')
    walk_sound.set_volume(0.5)  # Установка громкости для шагов
except pygame.error as e:
    print(f"Не удалось загрузить звук шагов: {e}")

# Скорость изменения размера
shrink_rate = 3  # Увеличенная скорость уменьшения при движении вперед
grow_rate = 5    # Нормальная скорость увеличения при движении назад

# Основной игровой цикл
running = True
reached_min_size = False  # Флаг для проверки достижения минимального размера

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

    # Проверка, двигается ли персонаж
    is_moving = False

    # Уменьшение при нажатии W
    if keys[pygame.K_w] and character_size > final_size and not reached_min_size:
        character_size -= shrink_rate  # Увеличенная скорость уменьшения
        character = pygame.transform.scale(character_image, (character_size, character_size))
        character_rect = character.get_rect(center=character_rect.center)
        is_moving = True

    # Увеличение при нажатии S
    if keys[pygame.K_s] and character_size < initial_size:
        character_size += grow_rate
        character = pygame.transform.scale(character_image, (character_size, character_size))
        character_rect = character.get_rect(center=character_rect.center)
        is_moving = True

    # Управление звуком шагов
    if is_moving:
        if not pygame.mixer.Sound.get_num_channels(walk_sound):
            walk_sound.play(-1)  # Воспроизведение звука шагов в цикле
    else:
        walk_sound.stop()  # Остановить звук шагов, когда движение прекращается

    # Проверка на достижение минимального размера и запуск плавного исчезновения
    if character_size <= final_size and not reached_min_size:
        reached_min_size = True
        pygame.mixer.music.stop()  # Остановить фоновый звук улицы
        walk_sound.stop()  # Остановить звук шагов

    # Плавное исчезновение персонажа с увеличенной скоростью
    if reached_min_size:
        for alpha in range(255, -1, -15):  # Увеличение шага до 15 для более быстрого исчезновения
            screen.fill((0, 0, 0))  # Черный экран
            screen.blit(background, (0, 0))
            character.set_alpha(alpha)
            screen.blit(character, character_rect)
            pygame.display.flip()
            pygame.time.delay(30)  # Уменьшение задержки для ускорения
        reached_min_size = False  # Остановка дальнейшего уменьшения после исчезновения
        running = False  # Завершение цикла

    # Прорисовка персонажа
    if not reached_min_size:
        screen.blit(character, character_rect)

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Ограничение FPS

# Черный экран на 3 секунды перед переходом к part2.py
screen.fill((0, 0, 0))
pygame.display.flip()
pygame.time.delay(5000)
python_path = sys.executable

# Переход на part2.py
subprocess.Popen([python_path, os.path.join(os.getcwd(), 'part2.py')])
pygame.quit()
sys.exit()
