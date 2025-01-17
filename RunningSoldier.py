# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading


from pygame import mixer

import pygame

pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Running Soldier")

Ico = pygame.image.load("assets/Soldier/r_run/tile008.png")
pygame.display.set_icon(Ico)


RUNNING = [
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile008.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile009.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile010.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile011.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile012.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile013.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile014.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile015.png")),
]
DEAD = [pygame.image.load(os.path.join("assets/Soldier/r_dead", "tile007.png"))]
JUMPING = [pygame.image.load(os.path.join("assets/Soldier/r_run", "tile012.png"))]
DUCKING = [
    pygame.image.load(os.path.join("assets/Soldier/r_duck", "tile004.png"))
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Other", "desert_rock1.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Other", "middle_lane_rock1_1.png")),
    pygame.image.load(os.path.join("assets/Other", "middle_lane_rock1_2.png")),
    pygame.image.load(os.path.join("assets/Other", "middle_lane_rock1_3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "tile000.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile001.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile002.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile003.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile004.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile005.png")),
]

SHOOT = pygame.image.load(os.path.join("assets/Soldier/r_shoot", "tile007.png"))

CLOUD = pygame.image.load(os.path.join("assets/Other", "cloud_shape3_1.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

BULLET = pygame.image.load(os.path.join("assets/Other", "bullet_image.png"))

BOMB = pygame.image.load(os.path.join("assets/Other","Bomb_03.png"))

SLOWMO = pygame.image.load(os.path.join("assets/Other","Hero_Speed_Debuff.png"))

scaled_image = pygame.transform.scale(BOMB, (64, 64))

scaled_image_sm = pygame.transform.scale(SLOWMO, (64, 64))

FONT_COLOR=(0,0,0)

fireballs=[]
bullet_items = []
fireball_count = 3
bomb_items=[]
slowmo_items=[]

class Background():
    def __init__(self):
        self.bg_images = [pygame.image.load(os.path.join("assets/Other", "Background.png")) for _ in range(4)]
        #self.bg_image2 =  [pygame.image.load(os.path.join("assets/Other", "Background.png")) for _ in range(4)]
        self.rectBGimg = self.bg_images[0].get_rect()

        self.bgY = 0
        self.bgX = [i * self.rectBGimg.width for i in range(4)]
        
        self.bgY2 = self.rectBGimg.height

    def update(self):
        for i in range(4):
            self.bgX[i] -= game_speed
            if self.bgX[i] <= -self.rectBGimg.width:
                self.bgX[i] = (3 * self.rectBGimg.width) + self.bgX[i]

    def render(self):
        for i in range(4):
            SCREEN.blit(self.bg_images[i], (self.bgX[i], self.bgY))
            SCREEN.blit(self.bg_images[i], (self.bgX[i], self.bgY2))


class Fireball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = BULLET
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 20

    def move(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def collides_with(self, obstacle):
        # Use the rect attribute for collision detection
        return self.rect.colliderect(obstacle.rect)

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = scaled_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 20

    def move(self):
        self.rect.x += self.speed

    def draw(self, screen):
        scaled_image = pygame.transform.scale(BOMB, (64, 64))
        screen.blit(scaled_image, self.rect)
    
    def collides_with(self, obstacle):
        # Use the rect attribute for collision detection
        return self.rect.colliderect(obstacle.rect)

class SlowMo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = scaled_image_sm
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 20

    def move(self):
        self.rect.x += self.speed

    def draw(self, screen):
        scaled_image_sm = pygame.transform.scale(SLOWMO, (64, 64))
        screen.blit(scaled_image_sm, self.rect)
    
    def collides_with(self, obstacle):
        # Use the rect attribute for collision detection
        return self.rect.colliderect(obstacle.rect)

class soldier:

    X_POS = 80
    Y_POS = 330
    Y_POS_DUCK = 370
    JUMP_VEL = 8.5
    MAX_Y_POS = 500  # Change as per your screen size and game design
    MIN_Y_POS = 100  # Change as per your screen size and game design
    VERTICAL_MOVE_SPEED = 10  # Speed of vertical movement

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD
        self.shoot_img = SHOOT

        self.soldier_duck = False
        # self.soldier_run = True
        self.soldier_jump = False
        self.soldier_dead = False
        self.soldier_shoot = False

        self.step_index = 0
        self.jump_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.soldier_rect = self.image.get_rect()
        self.soldier_rect.x = self.X_POS
        self.soldier_rect.y = self.Y_POS
        self.hitbox = self.soldier_rect.inflate(-20, -10)
        
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)

        self.sounds_list = {
            'item_collect': mixer.Sound('sounds/item_collect.wav'),
            'bomb': mixer.Sound('sounds/bomb.wav'),
            'Hit': mixer.Sound('sounds/Hit.wav'),
            'jump': mixer.Sound('sounds/jump.wav'),
            'next_level': mixer.Sound('sounds/next_level.wav'),
            'shot': mixer.Sound('sounds/shot.wav'),
            'slow': mixer.Sound('sounds/slow.wav')
        }
        
        self.hit=False


    def update(self, userInput):

        self.hitbox = self.soldier_rect.inflate(-100, 0)

        if self.soldier_duck:
            self.duck()
        # if self.soldier_run:
        #     self.run()
        if self.soldier_jump:
            self.jump()
        if self.soldier_dead:
            if self.hit==False:
                self.music_channel.play(self.sounds_list['Hit'])
                self.hit=True
            self.dead()
        
        if userInput[pygame.K_UP] and self.soldier_rect.y > self.MIN_Y_POS:
            self.soldier_rect.y -= self.VERTICAL_MOVE_SPEED
        elif userInput[pygame.K_DOWN] and self.soldier_rect.y < self.MAX_Y_POS:
            self.soldier_rect.y += self.VERTICAL_MOVE_SPEED
        
        if self.soldier_shoot:
            self.shoot()

        if self.step_index >= 8:
            self.step_index = 0

        # if (userInput[pygame.K_UP]) and not self.soldier_jump:
        #     self.soldier_rect.y -=10
        # elif userInput[pygame.K_DOWN] and not self.soldier_jump:
        #     self.soldier_rect.y +=10
        # elif not (self.soldier_jump or userInput[pygame.K_DOWN]):
        #     self.soldier_duck = False
        #     self.soldier_run = True
        #     self.soldier_jump = False

        if self.soldier_dead:
            self.soldier_run = False
            self.soldier_duck = False
            self.soldier_jump = False
            self.soldier_dead = True
            
    def duck(self):
        self.image = self.duck_img[0]
        self.soldier_rect = self.image.get_rect()
        self.soldier_rect.x = self.X_POS
        self.soldier_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    # def run(self):
    #     self.image = self.run_img[self.step_index]
    #     self.soldier_rect = self.image.get_rect()
    #     self.soldier_rect.x = self.X_POS
    #     self.soldier_rect.y = self.Y_POS
    #     self.step_index += 1

    def jump(self):
        self.image = self.jump_img[self.jump_index]
        if self.soldier_jump:
            self.soldier_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.soldier_jump = False
            self.jump_vel = self.JUMP_VEL
        
    
    def dead(self):
        self.image = self.dead_img[0]
    
    def shoot(self):
        self.image = self.shoot_img
        self.music_channel.play(self.sounds_list['shot'])


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.soldier_rect.x, self.soldier_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 270, 300]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class BulletItem:
    def __init__(self):
        self.image = pygame.image.load(os.path.join("assets/Other", "bullet_image.png"))  # Replace with your item image path
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 350)  # Random height
        
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)

        self.sounds_list = {
            'item_collect': mixer.Sound('sounds/item_collect.wav'),
            'bomb': mixer.Sound('sounds/bomb.wav'),
        }

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # Remove the item if it goes off the screen
            bullet_items.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BombItem:
    def __init__(self):
        self.image = scaled_image  # Replace with your item image path
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 350)  # Random height
        
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)

        self.sounds_list = {
            'bomb': mixer.Sound('sounds/bomb.wav')
        }

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # Remove the item if it goes off the screen
            bomb_items.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class SlowMoItem:
    def __init__(self):
        self.image = scaled_image_sm  # Replace with your item image path
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 350)  # Random height
        
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)

        self.sounds_list = {
            'slow': mixer.Sound('sounds/slow.wav'),
        }

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # Remove the item if it goes off the screen
            slowmo_items.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    global fireballs, fireball_count, death_count
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = soldier()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False
    fireball_count = 3
    back_ground = Background()

    pygame.key.set_repeat(50, 50)

    def display_bullet_count():
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(f'Bullets: {fireball_count}', True, FONT_COLOR)
        text_rect = text.get_rect(topleft=(10, 10))  # Position at top-left corner
        SCREEN.blit(text, text_rect)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 2
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    # def background():
    #     global x_pos_bg, y_pos_bg
    #     image_width = BG.get_width()
    #     SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    #     SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    #     if x_pos_bg <= -image_width:
    #         SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    #         x_pos_bg = 0
    #     x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    run = False
                    paused()
                if event.key == pygame.K_SPACE and fireball_count > 0:
                    player.shoot()
                    fireballs.append(Fireball(player.soldier_rect.x, player.soldier_rect.y))
                    fireball_count -= 1
                if event.key == pygame.K_UP:
                    print("up")
                    player.soldier_rect.y = max(player.MIN_Y_POS, player.soldier_rect.y - player.VERTICAL_MOVE_SPEED)
                if event.key == pygame.K_DOWN:
                    print("down")
                    player.soldier_rect.y = min(player.MAX_Y_POS, player.soldier_rect.y + player.VERTICAL_MOVE_SPEED)
        
            # Add bullet items to the game
        if random.randint(0, 60) == 5:  # Adjust the frequency as needed
            bullet_items.append(BulletItem())
        
        if random.randint(0, 200) == 5:  # Adjust the frequency as needed
            bomb_items.append(BombItem())
        
        if random.randint(0, 200) == 5:  # Adjust the frequency as needed
            if game_speed>10:
                slowmo_items.append(SlowMoItem())

        # Update and draw bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.update()
            item.draw(SCREEN)
        
        for item in bomb_items[:]:
            item.update()
            item.draw(SCREEN)
        
        for item in slowmo_items[:]:
            item.update()
            item.draw(SCREEN)

        # Check for collisions with bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.soldier_rect.colliderect(item.rect):
                player.music_channel.play(player.sounds_list['item_collect'])
                fireball_count += 1  # Increase bullet count
                bullet_items.remove(item)  # Remove the collected item
        
        for item in bomb_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.soldier_rect.colliderect(item.rect):
                player.music_channel.play(player.sounds_list['bomb'])
                obstacles.clear()
                bomb_items.remove(item)  # Remove the collected item
        
        for item in slowmo_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.soldier_rect.colliderect(item.rect):
                player.music_channel.play(player.sounds_list['slow'])
                game_speed -= 2
                if game_speed == 0 or game_speed<0:
                    game_speed = 1
                slowmo_items.remove(item)
        
        
        # for obstacle in obstacles:
        #     obstacle.draw(SCREEN)
        #     obstacle.update()
        #     if player.hitbox.colliderect(obstacle.rect) and not player.soldier_dead:
        #         death_count += 1
        #         player.soldier_dead = True  # Set the soldier as dead
        #         player.dead()  # Call the dead method to handle the death event
        #         break 
        #     for fireball in fireballs:
        #         if fireball.collides_with(obstacle):  # You'll need to implement this method
        #             obstacles.remove(obstacle)
        #             fireballs.remove(fireball)
        #             break
        
        fireballs = [fireball for fireball in fireballs if fireball.x < SCREEN_WIDTH]

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        
        # background()
        back_ground.update()
        back_ground.render()


        player.draw(SCREEN)
        player.update(userInput)
        

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.hitbox.colliderect(obstacle.rect):
                player.dead()
                pygame.time.delay(1000)
                menu(death_count)
            for fireball in fireballs:
                if fireball.collides_with(obstacle):
                    points += 50
                    obstacles.remove(obstacle)
                    fireballs.remove(fireball)
                    break


        for fireball in fireballs:
            fireball.move()
            fireball.draw(SCREEN)
        
        for item in bomb_items[:]:
            item.draw(SCREEN)
        
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.draw(SCREEN)
        
        for item in slowmo_items[:]:  # Use a slice copy to iterate safely when removing items
            item.draw(SCREEN)
        
        cloud.draw(SCREEN)
        cloud.update()
        
        display_bullet_count()

        score()

        clock.tick(60)
        pygame.display.update()
        


def menu(death_count):
    global points
    global FONT_COLOR
    run = True
    while run:
        FONT_COLOR=(0,0,0)
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Space War, Press enter to play", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )  # Read all file in case values are not on a single line
                score_ints = [int(x) for x in score.split()]  # Convert strings to ints
            highscore = max(score_ints)  # sum all elements of the list
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
