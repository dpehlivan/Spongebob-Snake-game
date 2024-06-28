#Spongebob snake game project version 2.0

import pygame, sys, random,json
from pygame.math import Vector2

# Creates the square for fruit for the snake
class FRUIT:
    def __init__(self):
        self.suprise()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(fruit_scale,fruit_rect)
        #pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        #this is a test rectangle for fruit movement

    def suprise(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

#creates square spaces for the snake body and draws them
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1,0)
        self.new_tail = False


    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (92, 255, 110), block_rect)
    #this code makes the snake move forward on the board 
    def move_snake(self):
        if self.new_tail == True:
            body_double = self.body[:]
            body_double.insert(0, body_double[0] + self.direction)
            self.body = body_double [:]
            self.new_tail = False
        else:
            body_double = self.body[ :-1]
            body_double.insert(0, body_double[0] + self.direction)
            self.body = body_double [:]
        
    def tail (self):
        self.new_tail = True


class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.file_path = 'spongebob_scoreboard.json'
        self.player_name = 'Player'
#this calls the methods
    def refresh(self):
        self.snake.move_snake()
        self.check_snake_lick_fruit()
        self.check_snake_injury()

    def draw_objects(self):
        self.write_score()
        self.draw_sea()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    def check_snake_lick_fruit(self):
        if self.fruit.pos == self.snake.body[0]:
            #this print statement checks if function check_snake_lick_fruit works properly
            #print("I am Batman")
#this method places the fruit randomly after snake licks it
           self.fruit.suprise()    
           #this method adds a additional tail to snake after fruit lick
           self.snake.tail()
           self.update_scoreboard(self.file_path, self.player_name, 1)
    def check_snake_injury(self):
        #checks if snake head hits the walls or bites itself
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number :
            self.game_restart()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_restart()

    def game_restart(self):
         self.update_scoreboard(self.file_path, self.player_name, len(self.snake.body) - 3)
         self.__init__()

    def game_over(self):
        self.game_restart()
        
#this changes the background color variations(the checkerboard)
    def draw_sea(self):
        sea_color = (0, 112, 255)
        for row in range(cell_number):
           if row % 2 == 0:
              for col in range (cell_number):
                 if col % 2 == 0:
                    sea_rect = pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                    pygame.draw.rect(screen, sea_color, sea_rect)
           else:
               for col in range (cell_number):
                 if col % 2 != 0:
                    sea_rect = pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                    pygame.draw.rect(screen, sea_color, sea_rect)
    #this is the scoreboard, keeps track of score according to snake body length
    def write_score(self):
       # points = score_numbers
        score_numbers = str(len(self.snake.body) - 3)
        score_display = game_font.render(score_numbers,True,(42,45,52))
        score_x = int(cell_size*cell_number - 60)
        score_y = int(cell_size*cell_number - 40)
        #fruit_rect = fruit.get_rect(midright = (score_rect.left, score_rect.centery))
        score_rect = score_display.get_rect(center = (score_x, score_y))
        screen.blit(score_display,score_rect)

        #screen.blit(fruit_scale,fruit_rect)
    def read_scores(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def write_scores(self, file_path, scores):
        with open(file_path, 'w') as file:
            json.dump(scores, file, indent=4)

    def update_scoreboard(self, file_path, player_name, points):
        scores = self.read_scores(file_path)
        if player_name in scores:
            if points > scores[player_name]:
                scores[player_name] = points
        else:
            scores[player_name] = points
        self.write_scores(file_path, scores)



               




# This starts pygame
pygame.init()
cell_size = 40
cell_number = 24

# This is the display of game screen
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

# This helps keep track of running time during the game
timer = pygame.time.Clock()

size = (50, 50)

#this imports the image of the fruit
fruit = pygame.image.load("krabbypatty.png")
fruit_scale = pygame.transform.scale(fruit,size)
#fruit = FRUIT()
#snake = SNAKE()

#this is the font for the scoreboard
game_font = pygame.font.Font("Spongeboy Me Bob.ttf", 20)

#this is a custom event that will be initiated in the game every 140 miliseconds
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,140)

main_game = GAME()
game_running = False
#game_restart = False
def game_start():
    global game_running,main_game
    main_game = GAME()
    game_running = True
    #game_restart = True

# Loop in which all game elements are going to be displayed
while True:
    # This closes the screen window and whole code by pressing the X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE and game_running:
            main_game.refresh()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                 if main_game.snake.direction.y !=1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                 if main_game.snake.direction.y !=-1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                 if main_game.snake.direction.x !=1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                 if main_game.snake.direction.x !=-1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_r and not game_running:
                game_start()
            #if event.key == pygame.K_w:
                #main_game.snake.direction = Vector2(0, -1)
            #if event.key == pygame.K_s:
               # main_game.snake.direction = Vector2(0, 1)
            #if event.key == pygame.K_a:
              #  main_game.snake.direction = Vector2(-1, 0)
            #if event.key == pygame.K_d:
             #   main_game.snake.direction = Vector2(1,0)

    # This is the red, green, and blue coloring of display 
    screen.fill((48, 197, 255))

    if game_running:
        main_game.draw_objects()
    else:
        start_text = game_font.render('Welcome to Planktons KrabbyPatty Adventure, press R to start', True, (42, 45, 52))
        start_rect = start_text.get_rect(center=(cell_number * cell_size / 2, cell_number * cell_size / 2))
        screen.blit(start_text, start_rect)



    #fruit.draw_fruit()
    #snake.draw_snake()

    pygame.display.update()

    # Maximum speed of frames per second
    timer.tick(70)


