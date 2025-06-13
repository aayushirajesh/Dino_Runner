import pygame, random, os

HIGH_SCORE_FILE = "high_score.txt"

pygame.init()

# Creating Window
screen_width = 1100
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))   # WIDTH(X) and HEIGHT(Y)   // creates actual window where game runs
pygame.display.set_caption("Dino Runner")   # title of window
icon = pygame.image.load('assets/dino/DinoStart.png') # load image into icon variable
pygame.display.set_icon(icon)   # display image in icon variable as icon for game


DINO_RUNNING = [pygame.image.load('assets/dino/DinoRun1.png'),pygame.image.load('assets/dino/DinoRun2.png')]
DINO_DUCK = [pygame.image.load('assets/dino/DinoDuck1.png'),pygame.image.load('assets/dino/DinoDuck2.png')]
DINO_JUMP = pygame.image.load('assets/dino/DinoJump.png')
SMALL_TREE = [pygame.image.load('assets/tree/small1.png'),pygame.image.load('assets/tree/small2.png'),pygame.image.load('assets/tree/small3.png'),pygame.image.load('assets/tree/small4.png')]
LARGE_TREE = [pygame.image.load('assets/tree/large1.png'),pygame.image.load('assets/tree/large2.png'),pygame.image.load('assets/tree/large3.png'), pygame.image.load('assets/tree/large4.png')]
BIRD = [pygame.image.load('assets/bird/Bird1.png'), pygame.image.load('assets/bird/Bird2.png')]
CLOUD = pygame.image.load('assets/others/Cloud.png')
BG = pygame.image.load('assets/others/Track.png')
pygame.mixer.music.load('assets/music/dino_bg.mp3')  # Path to your music file
pygame.mixer.music.set_volume(0.5)  # Volume: 0.0 to 1.0
pygame.mixer.music.play(-1)  # -1 makes the music loop forever



class Dino:
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    jump_velocity = 8.5

    def __init__(self):
        self.duck_img = DINO_DUCK
        self.run_img = DINO_RUNNING
        self.jump_img = DINO_JUMP

        #by default dino is always running
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.jump_velocity
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos   #x coordinate of dino
        self.dino_rect.y = self.y_pos   #y coordinate of dino
        
    def update(self, userInput):   #updates dino at every iteration of while loop
        #check state of dino
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        
        if self.step_index >= 10:
            self.step_index = 0
        
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):   #same as run
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck   #y coordinate of dino while ducking
        self.step_index += 1
    
    def run(self):
        self.image = self.run_img[self.step_index // 5]   #step_index helps loop through run_img to show animation of running dino
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos   #x coordinate of dino
        self.dino_rect.y = self.y_pos   #y coordinate of dino
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        #jump physics
        if self.dino_jump:      #jump prompted
            self.dino_rect.y -= self.jump_vel * 4     # Move Dino up
            self.jump_vel -= 0.8      # Simulate gravity    // decelerate cuz at peak of jump, vel = 0
        if self.jump_vel < -self.jump_velocity:      #when jump at peak positon   
            self.dino_jump = False
            self.jump_vel = self.jump_velocity       #reset velocity


    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
    
class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.width = self.image.get_width()
    def update(self):
        self.x -= game_speed  #move cloud from right to left
        #when cloud goes off screen, reset its coordinates so it appears again
        if self.x < -self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type    # determine what type of cherry blossom to display(small or large)
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self, obstacles): #move obstacle across screen
        self.rect.x -= game_speed   #decrease x axis of img
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image[self.type], (self.rect.x, self.rect.y-50))

class SmallTrees(Obstacles):    #class smalltree inherits from class obstacles
    def __init__(self, image):
        self.type = random.randint(0,3)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeTrees(Obstacles):    #class smalltree inherits from class obstacles
    def __init__(self, image):
        self.type = random.randint(0,3)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0  #only one type of bird
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):    #overrides draw in parent class_obstacle
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index//5], self.rect)
        self.index += 1


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    else:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


high_score = load_high_score()

def main():
    global game_speed, x_pos_bg, y_pos_bg, score, high_score
    run = True
    clock = pygame.time.Clock()
    player = Dino()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    score = 0
    font = pygame.font.Font(None, 30)
    obstacles = []
    death_count = 0


    def display_score():
        global game_speed, score, high_score
        score += 1
        if score % 100 == 0:
            game_speed += 1
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        text = font.render("Score: " + str(score), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        screen.blit(text, text_rect)

        # Also display high score
        high_score_text = font.render("High Score: " + str(high_score), True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (900, 70)
        screen.blit(high_score_text, high_score_rect)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((204, 235, 255))   # pastel blue
        userInput = pygame.key.get_pressed()

    
        player.draw(screen)   #draw dino on screen
        player.update(userInput)    #dino logic

        if len(obstacles) ==0:
            choice = random.randint(0, 2)
            if choice == 0:
                obstacles.append(SmallTrees(SMALL_TREE))
            elif choice == 1:
                obstacles.append(LargeTrees(LARGE_TREE))
            else:
                obstacles.append(Bird(BIRD))


        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update(obstacles)

            # remove useless padding around dino so when it collide with obstacles, it doesn't look awkward(space btw dino and obstacle)
            # i.e, game over tho it looks like dino didnot touch obstacle
            adjusted_dino_rect = player.dino_rect.inflate(-20, -10)

            if adjusted_dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                run = False  # This ends the main loop and returns to outer menu

        background()
        cloud.draw(screen)   #draw cloud on screen
        cloud.update()    #cloud logic
        display_score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global score
    run = True
    while run:
        screen.fill((204, 235, 255))
        font = pygame.font.Font(None, 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0,0,0))
        elif death_count >0:
            text = font.render("Press any Key to Start", True, (0,0,0))
            score_text = font.render("Your Score: " + str(score), True, (0,0,0))
            score_rect = score_text.get_rect()
            score_rect.center = (screen_width//2, screen_height//2+50)
            screen.blit(score_text, score_rect)

            # High score
            high_score_text = font.render("High Score: " + str(high_score), True, (0,0,0))
            high_score_rect = high_score_text.get_rect()
            high_score_rect.center = (screen_width//2, screen_height//2 + 90)
            screen.blit(high_score_text, high_score_rect)


        text_rect = text.get_rect()
        text_rect.center = (screen_width//2, screen_height//2)
        screen.blit(text, text_rect)
        screen.blit(DINO_RUNNING[0], (screen_width//2-20, screen_height//2-140))
        #screen.blit(pygame.image.load('assets/others/GameOver.png'), (screen_width//2-20, screen_height//2-100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Cleanly exit the program
            if event.type == pygame.KEYDOWN:
                run = False  # Exit the menu loop

if __name__ == "__main__":
    death_count = 0
    while True:
        menu(death_count)
        main()
        death_count += 1