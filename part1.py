import pygame
import sys
import subprocess

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
    print(f"Не удалось загрузить или воспроизвести звук: {e}")

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

    # Уменьшение при нажатии W
    if keys[pygame.K_w] and character_size > final_size and not reached_min_size:
        character_size -= shrink_rate  # Увеличенная скорость уменьшения
        character = pygame.transform.scale(character_image, (character_size, character_size))
        character_rect = character.get_rect(center=character_rect.center)

    # Увеличение при нажатии S
    if keys[pygame.K_s] and character_size < initial_size:
        character_size += grow_rate
        character = pygame.transform.scale(character_image, (character_size, character_size))
        character_rect = character.get_rect(center=character_rect.center)

    # Проверка на достижение минимального размера и запуск плавного исчезновения
    if character_size <= final_size and not reached_min_size:
        reached_min_size = True
        pygame.mixer.music.stop()  # Остановить фоновый звук

    # Плавное исчезновение персонажа
    if reached_min_size:
        for alpha in range(255, -1, -5):
            screen.fill((0, 0, 0))  # Черный экран
            screen.blit(background, (0, 0))
            character.set_alpha(alpha)
            screen.blit(character, character_rect)
            pygame.display.flip()
            pygame.time.delay(50)
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
pygame.time.delay(3000)

# Переход на part2.py
subprocess.Popen(['python', 'part2.py'])
pygame.quit()
sys.exit()
