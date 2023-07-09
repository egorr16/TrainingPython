from pygame import *
from map import *
init()
mixer.init()
mixer_music.load('res/jungles.ogg')
mixer_music.set_volume(0.04)
mixer_music.play()
kick = mixer.Sound('res/kick.ogg')
window = display.set_mode((795, 795))
BACKGROUND_COLOR = (255, 0, 100)
window.fill(BACKGROUND_COLOR)
clock = time.Clock()
game = True

# transform.scale - змінити розмір
background_image = transform.scale(
    image.load('res/fon.jpg'), (800, 800))


# image.load - заваниажити картинку

class Sprite:

    def __init__(self, image_name, x, y, width, height):
        self.image = transform.scale(
            image.load(image_name), (width, height))
        # автоматично створює хітбокс розмірами з картинку
        self.rect = self.image.get_rect()
        # встановимо кординати!
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        # функція яка за потреби буде рухати персонажа

    def move(self):
        # функція яка перевіряє чи натиснуто зараз якусь кнопку
        pressed_keys = key.get_pressed()  # отримати всі клавіші які натиснуто
        if pressed_keys[K_w]:
            self.rect.y -= 5
        if pressed_keys[K_s]:
            self.rect.y += 5
        if pressed_keys[K_a]:
            self.rect.x -= 5
        if pressed_keys[K_d]:
            self.rect.x += 5

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def auto_move(self, x1, x2):
        if self.rect.x <= x1 or self.rect.x + self.rect.width > x2:
            self.speed *= -1
        self.rect.x += self.speed

    def is_collide(self, cyborg):
        return self.rect.colliderect(cyborg.rect)

    def wall_collide(self, walls):
        pressed_keys = key.get_pressed()  # отримати всі клавіші які натиснуто
        for wall in walls:
            if self.is_collide(wall):
                if pressed_keys[K_w]:
                    self.rect.y += 5
                if pressed_keys[K_s]:
                    self.rect.y -= 5
                if pressed_keys[K_a]:
                    self.rect.x += 5
                if pressed_keys[K_d]:
                    self.rect.x -= 5


player1 = Sprite('res/fortnite.jpg', 100, 60, 40, 40)
enemy = Sprite('res/cyborg.png', 680, 680, 40, 40)
treasure = Sprite('res/treasure.png', 680, 680, 40, 40)
game_map = make_map()
while game:
    player1.move()
    player1.wall_collide(game_map)
    window.blit(background_image, (0, 0))

    enemy.draw()
    player1.draw()
    treasure.draw()
    enemy.auto_move(580, 740)

    for e in event.get():
        if e.type == QUIT:
            game = False
    for block in game_map:
        block.draw(window)
    if player1.is_collide(enemy):
        player1.rect.x = 55
        player1.rect.y = 55

    if player1.is_collide(treasure):  # якщо герой торкнувся спрайту
        # font.SysFont(Назва шрифта, розмір) - створити об'єкт шрифт певного розміру
        # .render(text, True, color) - на основі шрифта створити текст певного кольору
        # вікно.blit(text, (x, y)) - показати у вікні певне зображення в певних кординатах
        # щоб шрифти працювали, треба на початку написати init()
        text = font.SysFont('Algerian', 150).render("You Win", True, (50, 150, 100))
        window.blit(text, (100, 300))
        game = False
        display.update()
        time.wait(5000)  # почекати 5 секунд
    display.update()
    clock.tick(60)


