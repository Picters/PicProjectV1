import pygame
import sys
import subprocess

# Инициализация Pygame
pygame.init()

# Параметры экрана для полноэкранного режима
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("История Кирилла")
screen_width, screen_height = screen.get_size()

# Цвета и шрифт
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.SysFont('Arial', 36, bold=False)

# Загрузка и настройка музыки
ambience_sound = pygame.mixer.Sound('./assets/sfx/scary_ambience.mp3')
ambience_sound.set_volume(0.3)
ambience_sound.play(-1)  # Циклическое воспроизведение

# Текст истории Кирилла
story_text = (
    "Кирилл - умный мальчик. Он учился в школе и любил помогать своей маме. "
    "Кирилл обожает заброшенные места. И поэтому он решил пойти на заброшенную фабрику PicProject. "
    "На этой фабрике разрабатывали программы PicLab, но что-то пошло не по плану и одного ребенка намертво зажевало в механизмы. "
    "Ходят слухи, что душа этого ребенка бродит по фабрике и ищет новых друзей...."
)

# Функция для разделения текста на строки
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)  # Добавить оставшийся текст
    return lines

# Функция для плавного появления текста
def fade_in_effect(lines, x, y):
    for alpha in range(0, 256, 5):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)
        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, WHITE)
            rendered_text.set_alpha(alpha)
            screen.blit(rendered_text, (x, y + i * font.get_height()))
        
        pygame.display.flip()
        pygame.time.delay(50)

# Функция для плавного исчезновения текста и музыки
def fade_out_effect(lines, x, y):
    initial_volume = ambience_sound.get_volume()
    for alpha in range(255, -1, -5):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Уменьшение громкости звука
        new_volume = initial_volume * (alpha / 255)
        ambience_sound.set_volume(new_volume)
        
        screen.fill(BLACK)
        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, WHITE)
            rendered_text.set_alpha(alpha)
            screen.blit(rendered_text, (x, y + i * font.get_height()))
        
        pygame.display.flip()
        pygame.time.delay(50)

# Подготовка текста для отображения
wrapped_lines = wrap_text(story_text, font, screen_width - 100)  # Оставляем отступ от краев

# Основной цикл для отображения истории
running = True
while running:
    # Плавное появление текста
    fade_in_effect(wrapped_lines, 50, screen_height // 2 - len(wrapped_lines) * font.get_height() // 2)

    # Задержка на экране 10 секунд с обработкой событий
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 10000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Плавное исчезновение текста и звука
    fade_out_effect(wrapped_lines, 50, screen_height // 2 - len(wrapped_lines) * font.get_height() // 2)

    running = False  # Завершение цикла после отображения истории

# Остановка звука
ambience_sound.stop()

# Показ черного экрана на 3 секунды перед переходом к part1.py
screen.fill(BLACK)
pygame.display.flip()
pygame.time.delay(5000)

# Запуск part1.py
subprocess.Popen(['python', 'part1.py'])
pygame.quit()
sys.exit()
