from pygame import *  # Импортируем все модули из библиотеки Pygame

# Маштабируем картинку под размер окна
background = transform.scale(image.load('winXP.png'),(600,500))

# Определяем класс GameSprite (игровой спрайт - базовый объект)
class GameSprite(sprite.Sprite):
    # Конструктор класса, вызывается при создании объекта
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()  # Вызываем конструктор родительского класса sprite.Sprite
        # Загружаем изображение, масштабируем его до нужных размеров и сохраняем
        self.image = transform.scale(image.load(player_image), (wight, height)) 
        self.speed = player_speed  # Сохраняем скорость объекта
        self.rect = self.image.get_rect()  # Получаем прямоугольную область спрайта для коллизий
        self.rect.x = player_x  # Устанавливаем начальную X-координату
        self.rect.y = player_y  # Устанавливаем начальную Y-координату
    
    # Метод для отрисовки спрайта на экране
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Рисуем изображение в позиции rect

# Определяем класс Player (игрок), наследующий от GameSprite
class Player(GameSprite):
    # Метод для управления правым игроком (клавиши стрелок)
    def update_r(self):
        keys = key.get_pressed()  # Получаем список нажатых клавиш
        # Если нажата стрелка вверх и игрок не упёрся в верхнюю границу
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed  # Двигаем игрока вверх
        # Если нажата стрелка вниз и игрок не упёрся в нижнюю границу
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed  # Двигаем игрока вниз
    
    # Метод для управления левым игроком (клавиши W и S)
    def update_l(self):
        keys = key.get_pressed()  # Получаем список нажатых клавиш
        # Если нажата W и игрок не упёрся в верхнюю границу
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed  # Двигаем игрока вверх
        # Если нажата S и игрок не упёрся в нижнюю границу
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed  # Двигаем игрока вниз

# Настройки окна
back = (200, 255, 255)  # Цвет фона (голубоватый)
win_width = 600  # Ширина окна
win_height = 500  # Высота окна
window = display.set_mode((win_width, win_height))  # Создаём окно игры

# Основные переменные игры
game = True  # Переменная для главного цикла игры
finish = False  # Флаг окончания игры (раунда)
clock = time.Clock()  # Объект для управления частотой кадров
FPS = 60  # Количество кадров в секунду

# Создаём объекты игроков (ракетки)
racket1 = Player('roketka.png', 30, 200, 4, 50, 150)  # Левый игрок
racket2 = Player('roketka.png', 520, 200, 4, 50, 150)  # Правый игрок
ball = GameSprite('ballPP.png', 200, 200, 4, 50, 50)  # Мяч

# Настройка шрифта для вывода текста
font.init()  # Инициализируем модуль шрифтов
font = font.Font(None, 35)  # Создаём шрифт размера 35
lose1 = font.render('Игрок 1 проиграл!', True, (180, 0, 0))  # Текст при поражении 1 игрока
lose2 = font.render('Игрок 2 проиграл!', True, (180, 0, 0))  # Текст при поражении 2 игрока

# Начальная скорость мяча
speed_x = 3  # Скорость по горизонтали
speed_y = 3  # Скорость по вертикали

# Основной игровой цикл
while game:
    # Выявляем изображение заднего фона
    window.blit(background, (0, 0))
    # Обрабатываем все события (нажатия клавиш, закрытие окна)
    for e in event.get():
        if e.type == QUIT:  # Если нажата кнопка закрытия окна
            game = False  # Завершаем игру
    
    # Если игра не закончена (финиш не наступил)
    if finish != True:
        racket1.update_l()  # Обновляем позицию левой ракетки
        racket2.update_r()  # Обновляем позицию правой ракетки
        ball.rect.x += speed_x  # Двигаем мяч по горизонтали
        ball.rect.y += speed_y  # Двигаем мяч по вертикали

        # Проверяем столкновение мяча с ракетками
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1  # Меняем направление по горизонтали на противоположное
            speed_y *= 1  # Скорость по вертикали не меняется

        # Проверяем столкновение мяча с верхней и нижней стеной
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1  # Меняем направление по вертикали

        # Проверяем, не вышел ли мяч за левую границу (гол правому игроку)
        if ball.rect.x < 0:
            finish = True  # Устанавливаем флаг окончания игры
            window.blit(lose1, (200, 200))  # Показываем поражение игрока 1
            game_over = True  # Устанавливаем флаг окончания раунда

        # Проверяем, не вышел ли мяч за правую границу (гол левому игроку)
        if ball.rect.x > win_width:
            finish = True  # Устанавливаем флаг окончания игры
            window.blit(lose2, (200, 200))  # Показываем поражение игрока 2
            game_over = True  # Устанавливаем флаг окончания раунда

        # Отрисовываем все объекты на экране
        racket1.reset()  # Рисуем левую ракетку
        racket2.reset()  # Рисуем правую ракетку
        ball.reset()  # Рисуем мяч

    display.update()  # Обновляем экран (показываем все изменения)
    clock.tick(FPS)  # Ждём, чтобы игра шла с частотой 60 кадров в секунду
