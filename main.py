import pygame
import os
import random

pygame.font.init()

#Window setting
WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

#Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#Load Images
ENEMY1_IMG = pygame.image.load(os.path.join("assets","enemy1.png"))
ENEMY2_IMG = pygame.image.load(os.path.join("assets","enemy2.png"))
ENEMY3_IMG = pygame.image.load(os.path.join("assets","enemy1.png"))

PLAYER_IMG = pygame.image.load(os.path.join("assets","spacecraft.png"))

LASER1_IMG = pygame.image.load(os.path.join("assets","laser1.png"))
LASER2_IMG = pygame.image.load(os.path.join("assets","laser2.png"))
LASER3_IMG = pygame.image.load(os.path.join("assets","laser3.png"))
LASER4_IMG = pygame.image.load(os.path.join("assets","laser4.png"))

HEART_IMG = pygame.image.load(os.path.join("assets","heart.png"))

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))
BG_START = pygame.transform.scale(pygame.image.load(os.path.join("assets","bg-start.png")),(WIDTH,HEIGHT))
BG_COMMAND = pygame.transform.scale(pygame.image.load(os.path.join("assets","bg-command-menu.png")),(WIDTH,HEIGHT))

class Spacecraft:

    COOLDOWN = 30

    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.spacecraft_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self,window):
        window.blit(self.spacecraft_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.spacecraft_img.get_width()

    def get_height(self):
        return self.spacecraft_img.get_height()

class Player(Spacecraft):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.spacecraft_img = PLAYER_IMG
        self.laser_img = LASER1_IMG
        self.mask = pygame.mask.from_surface(self.spacecraft_img)
        self.max_health = health

    def move_lasers(self, vel, objs, score):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs[:]:
                    if laser.collision(obj):
                        score += 100
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        return score


    def draw(self,window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self,window):
        pygame.draw.rect(window, RED, (self.x, self.y + self.spacecraft_img.get_height() + 10, self.spacecraft_img.get_width(), 10))
        pygame.draw.rect(window, GREEN, (self.x, self.y + self.spacecraft_img.get_height() + 10, self.spacecraft_img.get_width() * (1 - (self.max_health - self.health)/self.max_health), 10))

class Enemy(Spacecraft):
    BULLETS_TYPE = {
                "bullet1": (ENEMY1_IMG, LASER3_IMG),
                "bullet2": (ENEMY2_IMG, LASER4_IMG),
                "bullet3": (ENEMY3_IMG, LASER2_IMG)
                }

    def __init__(self,x,y,type,health=100):
        super().__init__(x,y,health)
        self.spacecraft_img, self.laser_img = self.BULLETS_TYPE[type]
        self.mask = pygame.mask.from_surface(self.spacecraft_img)

    def move(self,vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-21, self.y+50, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser:
    def __init__(self,x,y,img):
        self.x = x + 50
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img, (self.x, self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self,height):
        return not (height >= self.y >= 0)

    def collision(self,obj):
        return collide(obj, self)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def pause_menu():
    paused = True
    pause_font = pygame.font.SysFont("Verdana", 50)
    resume_font = pygame.font.SysFont("Verdana", 30)

    while paused:
        screen.blit(BG_IMG, (0, 0))

        pause_label = pause_font.render("Juego Pausado", True, WHITE)
        screen.blit(pause_label, (WIDTH//2 - pause_label.get_width()//2, HEIGHT//2 - 50))

        resume_label = resume_font.render("Presiona 'P' para reanudar", True, WHITE)
        screen.blit(resume_label, (WIDTH//2 - resume_label.get_width()//2, HEIGHT//2 + 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

def commands_menu():
    run = True

    while run:
        screen.blit(BG_COMMAND, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

def main():
    run = True
    paused = False
    fps = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("Verdana",35)
    score_font = pygame.font.SysFont("Verdana",20)
    lost_font = pygame.font.SysFont("Verdana",50)
    clock = pygame.time.Clock()
    player_vel = 5
    player = Player(300, 620)
    score = 0
    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 5

    lost = False
    lost_count = 0

    def redraw_window():
        screen.blit(BG_IMG,(0,0))

        for i in range(lives):
            screen.blit(HEART_IMG, (20 + i * (HEART_IMG.get_width() + 5), 20))

        level_label = main_font.render(f"Nivel: {level}", 1, WHITE)
        screen.blit(level_label, (WIDTH - level_label.get_width() - 20, 10))

        score_label = score_font.render(f"Puntos: {score}", 1, WHITE)
        screen.blit(score_label, (20, 60))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        if lost:
            lost_label = lost_font.render("Perdiste!!", 1, WHITE)
            screen.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            score_game = score_font.render(f"Puntos: {score}", 1, WHITE)
            screen.blit(score_game, (WIDTH/2 - score_game.get_width()/2, 450))

        pygame.display.update()

    while run:
        clock.tick(fps)

        redraw_window()

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 5:
                run = False
            else:
                continue

        if player.health <= 0:
            if lives > 1:
                lives -= 1
                player.health = player.max_health
            else:
                lives = 0
                lost = True
                lost_count = 1


        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["bullet1","bullet2","bullet3"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y + player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        score = player.move_lasers(-laser_vel, enemies, score)



def main_menu():
    title_font = pygame.font.SysFont("Verdana",30)
    run = True
    while run:
        screen.blit(BG_START,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    commands_menu()
    pygame.quit()

if __name__ == "__main__":
    main_menu()