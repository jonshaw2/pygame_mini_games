import pygame
import math
import time
import random

KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275
KEY_ENTER = 13
KEY_SPACE = 32
KEY_LeftCLICK = 1

KEY_Q = 113
KEY_W = 119
KEY_E = 101
KEY_A = 97
KEY_S = 115
KEY_D = 100
KEY_Z = 122
KEY_X = 120
KEY_C = 99

#initiate background
background_width = 1024
background_height = 960
background_line_thickness = 6
blue_color = (97, 159, 182)
screen = pygame.display.set_mode((background_width, background_height))
screen.fill(blue_color)
pygame.draw.lines(screen, (000,000,000), False, [(background_width/2,0),(background_width/2,background_height)],background_line_thickness)
pygame.draw.lines(screen, (000,000,000), False, [(0,background_height/2),(background_width, background_height/2)],background_line_thickness)

#initiate end condition
stop_game = False

class Square_jump_game(object):
    def __init__(self):

        self.dead = False
        self.dead_timer = 0

        #rectangle info
        self.x = 102
        self.y = 343

        self.rectangle_height = 60
        self.rectangle_width = 60
        self.rectangle_speed = 0

        self.mario_die = pygame.image.load("mario_die.png").convert_alpha()
        self.mario_die = pygame.transform.scale(self.mario_die, (self.rectangle_width, self.rectangle_height))

        #mario background
        self.mario_background = pygame.image.load("overworld_bg.png").convert_alpha()
        self.mario_background = pygame.transform.scale(self.mario_background, (512-3, 480-3))

        #mario info (standing)
        self.mario_standing = pygame.image.load("mario_standing.png").convert_alpha()
        self.mario_standing = pygame.transform.scale(self.mario_standing, (self.rectangle_width,self.rectangle_height))

        #mario info (jumping)
        self.mario_jumping = pygame.image.load("mario_jump.png").convert_alpha()
        self.mario_jumping = pygame.transform.scale(self.mario_jumping, (self.rectangle_width, self.rectangle_height))
        self.jump_condition = False

        #enemy info
        self.mario_enemy = pygame.image.load("mario_enemy.png").convert_alpha()
        self.mario_enemy = pygame.transform.scale(self.mario_enemy, (60,90))

        #wall info
        self.wall_x = (background_width / 10) + ((background_width/2 - background_width/10) * .8)
        self.wall_y = (background_height / 3) - 30 + 23
        self.wall_speed = 6

        #ground
        self.ground_height = (background_height/2)-(self.y+self.rectangle_height+background_line_thickness/2)
        self.ground_width = background_width/2-(background_line_thickness/2)
        self.ground_x = 100
        self.ground_y = self.y + self.rectangle_height + 50

        self.ground_limit = 343
        #keep score
        self.score_milisecond = time.time()
        self.score_second = 0
        self.score_minute = 0
        self.score = "00:00:00"
        #score text
        self.score_font = pygame.font.Font(None, 50)
        self.score_text = self.score_font.render(self.score, True, (0, 0, 0))
        screen.blit(self.score_text, (80, 100))
        #text
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render('Press SPACE to jump.', True, (255,0,0))
        screen.blit(self.text, (80, 415))

        pygame.draw.rect(screen, (0,0,255), (self.x,self.y,self.rectangle_width,self.rectangle_height), 0)
        pygame.draw.rect(screen, (139,69,19),(self.ground_x,self.ground_y,self.ground_width, self.ground_height),0)
        pygame.draw.rect(screen, (255,0,0), (self.wall_x, self.wall_y, 60,90), 0)

    def jump(self):
        self.jump_condition = True
        self.rectangle_speed = 10

    def render(self):
        screen.blit((self.mario_background),(0, 0))
        # pygame.draw.rect(screen, (0,0,255), (self.x,self.y,self.rectangle_width,self.rectangle_height), 0)
        pygame.draw.rect(screen, (139,69,19),(60,420,370, 40),0)
        # pygame.draw.rect(screen, (255,0,0), (self.wall_x, self.wall_y, 60,90), 0)
        screen.blit(self.text, (70, 425))
        self.score_text = self.score_font.render(self.score, True, (0, 0, 0))
        screen.blit(self.score_text, (180, 0))

        #mario standing
        if self.jump_condition == False and self.dead == False:
            screen.blit((self.mario_standing),(self.x, self.y))
        elif self.jump_condition == True and self.dead == False:
            screen.blit((self.mario_jumping), (self.x, self.y))
        elif self.dead == True:
            screen.blit((self.mario_die),(self.x, self.y))

        screen.blit((self.mario_enemy),(self.wall_x, self.wall_y))

    def jumping(self):
        self.y -= self.rectangle_speed
        if self.rectangle_speed >0 and self.y < 93:
            self.rectangle_speed = -10
        if self.rectangle_speed <0 and self.y >= self.ground_limit:
            self.rectangle_speed = 0
            self.jump_condition = False

    def wall_movement(self):
        self.wall_x -= self.wall_speed

        if self.wall_x <= 0 - 60:
            self.wall_x = (background_width / 10) + ((background_width/2 - background_width/10) * .8)

    def collision(self):
            if self.x+25 > self.wall_x-25 and self.x-25 < self.wall_x+25 and self.y-25 > self.wall_y-35 and self.dead == False:
                self.dead = True
                self.dead_timer = time.time()
                self.ground_limit = 2000
                game1_lose_sound.play()
                self.jump()
                #time.sleep(1)

            if self.x+25 > self.wall_x-25 and self.x-25 < self.wall_x+25 and self.y+25 > self.wall_y-35 and self.dead == False:
                self.dead = True
                self.dead_timer = time.time()
                self.ground_limit = 2000
                game1_lose_sound.play()
                self.jump()

            if self.dead == True and time.time() - self.dead_timer >= 3:
                self.__init__()

    def keep_score(self):
        if time.time() - self.score_milisecond > 1:
            self.score_second += 1
            self.score_milisecond = time.time()
        if self.score_second >= 60:
            self.score_minute += 1
            self.score_second = 0

        self.score = "%02.f:%02.f:%02.f" % (self.score_minute, self.score_second, (time.time() - self.score_milisecond)*100)

class Defuse_bomb(object):
    def __init__(self):

        self.current_time2 = time.time()
        self.spawn_time = random.randint(1,3)
        self.x = random.randint(512,800)
        self.y = random.randint(50,280)
        self.curr_time = time.time()

        #score text

        self.bomb_count = 0
        self.score = "Bombs Defused: %03.f" % self.bomb_count
        self.score_font = pygame.font.Font(None, 50)
        #text
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render('CLICK to defuse!', True, (255, 0, 0))
        screen.blit(self.text, (620, 415))

        self.size = 150
        self.explosion = 6
        self.explosion_text = ""
        self.bomb_pic = pygame.image.load("Zeeky_H_Bomb.png").convert_alpha()
        self.bomb_pic = pygame.transform.scale(self.bomb_pic, (self.size,self.size))

        self.spawn = True

    def render(self):

        #update explosion time
        if self.spawn == False:
            if time.time() - self.curr_time > 1 and self.x:
                self.explosion -= 1
                self.curr_time = time.time()

            if self.explosion <= 0:
                self.bomb_exploded()

            #explosion text
            self.explosion_text = str(self.explosion)
            font = pygame.font.Font(None, 100)
            text = font.render(self.explosion_text, True, (255, 0, 0))
            screen.blit(text, (self.x + 70, self.y - 40))

            screen.blit((self.bomb_pic),(self.x, self.y))
            #pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.size,self.size), 1)

        screen.blit(self.text, (620, 415))

        self.score_font = pygame.font.Font(None, 50)
        self.score_text = self.score_font.render(self.score, True, (0,0,0))
        screen.blit(self.score_text, (580,0))


    def collision(self,x,y):
        if x < self.x+ self.size and x > self.x and y < self.y+self.size and y > self.y and self.spawn == False:
            print "collision on bomb"
            self.bomb_count += 1
            self.score = "Bombs Defused: %03.f" % self.bomb_count
            self.current_time2 = time.time()
            self.spawn = True
            return True

    def reposition(self):
        if time.time() - self.current_time2 >= self.spawn_time and self.spawn == True:
            self.x = random.randint(512,800)
            self.y = random.randint(50,280)
            self.size = 150
            self.explosion = 5
            self.spawn = False

    def bomb_exploded(self):
        print "boom!"
        self.__init__()
class Drive(object):
    def __init__(self):
        #1024 960
        self.size_x = 80
        self.size_y = 120
        self.x = -100
        self.y = 760
        self.score = 0
        self.highscore = "%03.f Rabbit Doged!" %self.score
        self.curr_time = time.time()
        self.car_position = 2

        self.rabbit_x = -100
        self.rabbit_y = 545
        self.rabbit_position = random.randint(1,4)

        self.rabbit = pygame.image.load("rabbit.png").convert_alpha()
        self.rabbit = pygame.transform.scale(self.rabbit, (50,100))




        self.background = pygame.image.load("green-background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (512-3, 480-3))
        self.race_car = pygame.image.load("Pink_car.png").convert_alpha()
        self.race_car = pygame.transform.scale(self.race_car, (self.size_x,self.size_y))

        #text
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render('\"A\" \"D\" to drive!', True, (255, 0, 0))
        screen.blit(self.text, (100, 900))

        #highscore
        self.score_font = pygame.font.Font(None, 50)
        self.score_text = self.score_font.render(self.highscore, True, (0, 0, 0))
        screen.blit(self.score_text, (100, 500))

    def render(self):
        screen.blit((self.background),(0, 483))
        screen.blit((self.race_car),(self.x, self.y))
        screen.blit((self.rabbit),(self.rabbit_x,self.rabbit_y))

        screen.blit(self.text, (100, 900))

        self.highscore = "%03.f Rabbit Doged!" %self.score
        self.score_text = self.score_font.render(self.highscore, True, (0, 0, 0))
        screen.blit(self.score_text, (100, 500))


    def turn_left(self):
        if self.car_position <= 1:
            self.car_position = 1
        else:
            self.car_position -= 1

    def turn_right(self):
        if self.car_position >= 4:
            self.car_position = 4
        else:
            self.car_position += 1

    def check_car_position(self):
        if self.car_position == 1:
            self.x = 50
        elif self.car_position == 2:
            self.x = 150
        elif self.car_position == 3:
            self.x = 250
        elif self.car_position == 4:
            self.x = 350

        if self.car_position == self.rabbit_position and self.y - 200  < self.rabbit_y - 100:
            print "Rabbit Hitted"
            self.__init__()
    def obstacle_move(self):
        if self.rabbit_position == 1:
            self.rabbit_x = 65
        if self.rabbit_position == 2:
            self.rabbit_x = 165
        if self.rabbit_position == 3:
            self.rabbit_x = 265
        if self.rabbit_position == 4:
            self.rabbit_x = 365

        #if time.time() - self.curr_time >= 1:
        self.rabbit_y += 2
        #    self.curr_time = time.time()

    def new_rabbit(self):
        if self.rabbit_y > 900:
            self.rabbit_position = random.randint(1,4)
            self.rabbit_y = 545
            self.score += 1

#1024
#512
# class Mole(object, position):
#     def __init__(self):
#         self.mole_pic = pygame.image.load("mole.png").convert_alpha()
#         self.mole_background = pygame.transform.scale(self.mole_pic, (509, 477))
#         if position == 1:
#             print "hello 1"
#
#
#         elif position == 2:
#             print "hello 2"
#
#         else:
#             print "hello 3"
#         pass

class Whack_a_mole(object):
    def __init__(self):
        self.mole_counter = 0
        self.mole_miss = 0


        self.anger_movement = 5
        self.mole1_movement = 1
        self.mole2_movement = 1
        self.mole3_movement = 1
        self.mole4_movement = 1
        self.mole5_movement = 1
        self.mole6_movement = 1

        self.background_x = background_width/2+ 6
        self.background_y = 483

        self.score = ""
        self.score_font = pygame.font.Font(None, 50)
        self.score_text = self.score_font.render(self.score, True, (255, 0, 0))
        screen.blit(self.score_text, (500, 635))

        self.mole1_x = 535
        self.mole1_y = 545
        self.font1 = pygame.font.Font(None, 50)
        self.text1 = self.font1.render('\"Q\"', True, (255, 0, 0))
        screen.blit(self.text1, (577, 635))

        self.mole2_x = 700
        self.mole2_y = 545
        self.font2 = pygame.font.Font(None, 50)
        self.text2 = self.font2.render('\"W\"', True, (255, 0, 0))
        screen.blit(self.text2, (742, 635))

        self.mole3_x = 865
        self.mole3_y = 545
        self.font3 = pygame.font.Font(None, 50)
        self.text3 = self.font3.render('\"E\"', True, (255, 0, 0))
        screen.blit(self.text3, (907, 635))

        self.mole4_x = 535
        self.mole4_y = 755
        self.font4 = pygame.font.Font(None, 50)
        self.text4 = self.font4.render('\"Z\"', True, (255, 0, 0))
        screen.blit(self.text4, (577, 900))

        self.mole5_x = 700
        self.mole5_y = 755
        self.font5 = pygame.font.Font(None, 50)
        self.text5 = self.font5.render('\"X\"', True, (255, 0, 0))
        screen.blit(self.text5, (742, 845))

        self.mole6_x = 864
        self.mole6_y = 755
        self.font6 = pygame.font.Font(None, 50)
        self.text6 = self.font6.render('\"C\"', True, (255, 0, 0))
        screen.blit(self.text6, (907, 845))

        self.mole_pic = pygame.image.load("mole.png").convert_alpha()
        self.mole_pic = pygame.transform.scale(self.mole_pic, (150, 150))
        self.mole_background = pygame.image.load("whack_a_mole.png").convert_alpha()
        self.mole_background = pygame.transform.scale(self.mole_background, (512-3, 480-3))

        # self.mole [[Display Condition, Reset Spawn Timer Condition, Stored Time, Spawn Time, Anger Condition]]
        self.mole = [[True, True, time.time(),5,random.randint(4,10),False,time.time()],
                    [False, True, time.time(),5,random.randint(4,10),False,time.time()],
                    [False, True, time.time(),5,random.randint(4,10),False,time.time()],
                    [False, True, time.time(),5,random.randint(4,10),False,time.time()],
                    [False, True, time.time(),5,random.randint(4,10),False,time.time()],
                    [False, True, time.time(),5,random.randint(4,10),False,time.time()]]

    def spawn_mole(self):

        for i in range(len(self.mole)):

            if self.mole[i][0] == False:
                if self.mole[i][1] == True:
                    self.mole[i][2] = time.time()
                    self.mole[i][1] = False
                    self.mole[i][4] = random.randint(4,10)
                    self.mole[i][5] = False
                    self.mole[i][3] = 5
                    self.mole[i][6] = time.time()
                else:
                    if time.time() - self.mole[i][2] > self.mole[i][4]:
                        self.mole[i][0] = True
                        self.mole[i][2] = time.time()

            if time.time()-self.mole[i][6]>=1 and self.mole[i][0] == True:
                self.mole[i][3] -= 1
                self.mole[i][6] = time.time()

            if self.mole[i][3] <= 2:
                self.mole[i][5] = True

            if self.mole[i][3] == 0:
                self.mole_miss += 1
                self.mole[i][0] = False
                self.mole[i][1] = True

    def check_mole(self, input):
            if self.mole[input][0] == True:
                self.mole[input][0] = False
                self.mole[input][1] = True
                self.mole_counter += 1

    def render(self):
        screen.blit((self.mole_background),(self.background_x, self.background_y))

        screen.blit(self.text1, (577, 705))
        screen.blit(self.text2, (742, 705))
        screen.blit(self.text3, (907, 705))
        screen.blit(self.text4, (577, 915))
        screen.blit(self.text5, (742, 915))
        screen.blit(self.text6, (907, 915))

        if self.mole[0][0] == True and self.mole[0][5] == False:
            screen.blit((self.mole_pic),(self.mole1_x, self.mole1_y))
        elif self.mole[0][0] == True and self.mole1_movement == -1:
            screen.blit((self.mole_pic),(self.mole1_x+self.anger_movement, self.mole1_y))
            self.mole1_movement = 1
        elif self.mole[0][0] == True and self.mole1_movement == 1:
            screen.blit((self.mole_pic),(self.mole1_x-self.anger_movement, self.mole1_y))
            self.mole1_movement = -1

        if self.mole[1][0] == True and self.mole[1][5] == False:
            screen.blit((self.mole_pic),(self.mole2_x, self.mole2_y))
        elif self.mole[1][0] == True and self.mole2_movement == -1:
            screen.blit((self.mole_pic),(self.mole2_x+self.anger_movement, self.mole2_y))
            self.mole2_movement = 1
        elif self.mole[1][0] == True and self.mole2_movement == 1:
            screen.blit((self.mole_pic),(self.mole2_x-self.anger_movement, self.mole2_y))
            self.mole2_movement = -1

        if self.mole[2][0] == True and self.mole[2][5] == False:
            screen.blit((self.mole_pic),(self.mole3_x, self.mole3_y))
        elif self.mole[2][0] == True and self.mole3_movement == -1:
            screen.blit((self.mole_pic),(self.mole3_x+self.anger_movement, self.mole3_y))
            self.mole3_movement = 1
        elif self.mole[2][0] == True and self.mole3_movement == 1:
            screen.blit((self.mole_pic),(self.mole3_x-self.anger_movement, self.mole3_y))
            self.mole3_movement = -1

        if self.mole[3][0] == True and self.mole[3][5] == False:
            screen.blit((self.mole_pic),(self.mole4_x, self.mole4_y))
        elif self.mole[3][0] == True and self.mole4_movement == -1:
            screen.blit((self.mole_pic),(self.mole4_x+self.anger_movement, self.mole4_y))
            self.mole4_movement = 1
        elif self.mole[3][0] == True and self.mole4_movement == 1:
            screen.blit((self.mole_pic),(self.mole4_x-self.anger_movement, self.mole4_y))
            self.mole4_movement = -1

        if self.mole[4][0] == True and self.mole[4][5] == False:
            screen.blit((self.mole_pic),(self.mole5_x, self.mole5_y))
        elif self.mole[4][0] == True and self.mole5_movement == -1:
            screen.blit((self.mole_pic),(self.mole5_x+self.anger_movement, self.mole5_y))
            self.mole5_movement = 1
        elif self.mole[4][0] == True and self.mole5_movement == 1:
            screen.blit((self.mole_pic),(self.mole5_x-self.anger_movement, self.mole5_y))
            self.mole5_movement = -1

        if self.mole[5][0] == True and self.mole[5][5] == False:
            screen.blit((self.mole_pic),(self.mole6_x, self.mole6_y))
        elif self.mole[5][0] == True and self.mole6_movement == -1:
            screen.blit((self.mole_pic),(self.mole6_x+self.anger_movement, self.mole6_y))
            self.mole6_movement = 1
        elif self.mole[5][0] == True and self.mole6_movement == 1:
            screen.blit((self.mole_pic),(self.mole6_x-self.anger_movement, self.mole6_y))
            self.mole6_movement = -1


        self.score = "HIT:%03.f  MISS:%03.f" %(self.mole_counter, self.mole_miss)
        self.score_text = self.score_font.render(self.score, True, (255, 0, 0))
        screen.blit(self.score_text, (620, 505))

        # if self.mole[1][0] == True:
        #     screen.blit((self.mole_pic),(self.mole2_x, self.mole2_y))
        # if self.mole[2][0] == True:
        #     screen.blit((self.mole_pic),(self.mole3_x, self.mole3_y))
        # if self.mole[3][0] == True:
        #     screen.blit((self.mole_pic),(self.mole4_x, self.mole4_y))
        # if self.mole[4][0] == True:
        #     screen.blit((self.mole_pic),(self.mole5_x, self.mole5_y))
        # if self.mole[5][0] == True:
        #     screen.blit((self.mole_pic),(self.mole6_x, self.mole6_y))

def main():
    pygame.init()
    pygame.mixer.init()
    global game1_lose_sound
    #global background_music
    game1_lose_sound = pygame.mixer.Sound('Mario_Die.wav')
    pygame.mixer.music.load('Impossible_Quiz.mp3')
    pygame.mixer.music.play(1)

    clock = pygame.time.Clock()
    #initiate the games
    screen_1 = Square_jump_game()
    screen_2 = Defuse_bomb()
    screen_3 = Drive()
    screen_4 = Whack_a_mole()

    while not stop_game:
        screen_1.keep_score()
        screen_1.jumping()
        screen_1.wall_movement()
        screen_4.spawn_mole()

        for event in pygame.event.get():

            # Event handling
            if event.type == pygame.KEYDOWN:
                print event.key
                if event.key == KEY_SPACE:
                    if screen_1.y > (background_height / 3) - 50 :
                        screen_1.jump()
                if event.key == KEY_A:
                    screen_3.turn_left()
                if event.key == KEY_D:
                    screen_3.turn_right()

                if event.key == KEY_Q:
                    screen_4.check_mole(0)
                if event.key == KEY_W:
                    screen_4.check_mole(1)
                if event.key == KEY_E:
                    screen_4.check_mole(2)
                if event.key == KEY_Z:
                    screen_4.check_mole(3)
                if event.key == KEY_X:
                    screen_4.check_mole(4)
                if event.key == KEY_C:
                    screen_4.check_mole(5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    x, y = event.pos
                    if screen_2.collision(x,y):
                        screen_2.reposition()

        screen.fill(blue_color)
        pygame.draw.lines(screen, (255,255,255), True, [(background_width/2,0),(background_width/2,background_height)],background_line_thickness)
        pygame.draw.lines(screen, (255,255,255), False, [(0,background_height/2),(background_width, background_height/2)],background_line_thickness)
        screen_1.render()
        screen_2.render()
        screen_3.render()
        screen_4.render()

        if screen_2.spawn == True:
            screen_2.reposition()
        pygame.display.update()
        screen_1.collision()
        screen_3.obstacle_move()
        screen_3.check_car_position()
        screen_3.new_rabbit()

        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
