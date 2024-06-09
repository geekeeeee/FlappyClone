import pygame , sys
from random import randint

class FLOOR: 
    def __init__(self):
        self.floor_surface = pygame.image.load('assets/sprites/base.png')
        self.floor_surface = pygame.transform.scale(self.floor_surface, (SCREEN_WIDTH, floor_height))
        
        self.height = 0
        self.floor_x = 0
    
    def set_height (self, x) :
        self.height = x
    
    def set_x (self, x) :
        self.floor_x = x
    
    def draw_floor(self, screen, speed) : 
        self.floor_x -= speed
        if (self.floor_x <= -1 * SCREEN_WIDTH) : self.floor_x = 0
        screen.blit(self.floor_surface, (self.floor_x , SCREEN_HEIGHT - self.height))
        screen.blit(self.floor_surface, (self.floor_x + SCREEN_WIDTH , SCREEN_HEIGHT - self.height))

class BACKGROUND : 
    def __init__(self) -> None:
        self.bg_screen = pygame.image.load('assets/sprites/background-night.png').convert()
        self.bg_screen = pygame.transform.scale(self.bg_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def draw_bg(self, screen) :
        screen.blit(self.bg_screen, (0, 0))

class BIRD : 
    def __init__(self) -> None:
        upflap = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        upflap = pygame.transform.scale(upflap, (25, 20))
        
        midflap = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
        midflap = pygame.transform.scale(midflap, (25, 20))

        downflap = pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
        downflap = pygame.transform.scale(downflap, (25, 20))
        self.frames = [downflap, midflap, upflap]
        self.frameidx = 0
        self.bird_rect = self.frames[self.frameidx].get_rect(center = (SCREEN_WIDTH/3, 150)) 
        self.bird_mov = 0

    def set_bird_mov (self, x) :
        self.bird_mov = x

    def movebird(self, gravity, pipe, score) :
        self.bird_mov += gravity
        self.bird_rect.centery += self.bird_mov
        for pipe in pipe.pipe_list:
            if(pipe.right >= self.bird_rect.left  and pipe.right - 1 <= self.bird_rect.left) : 
                score.inc_score()

    def inc_idx(self) : 
        self.frameidx = (self.frameidx+1) % 3
        # self.bird_rect = self.frames[self.frameidx].get_rect(center = (SCREEN_WIDTH/3, 150)) 

    def resetbird(self) : 
        self.bird_rect = self.frames[self.frameidx].get_rect(center = (SCREEN_WIDTH/3, 150)) 
        self.set_bird_mov(0)
        
    def draw_bird(self, screen) :
        rotated_bird = pygame.transform.rotozoom(self.frames[self.frameidx], self.bird_mov * -5, 1)
        screen.blit(rotated_bird, self.bird_rect)

class PIPES : 
    def __init__(self, pipe_width, window) -> None:
        self.window = window
        self.pipe_list = []
        self.pipe_surface = pygame.image.load('assets/sprites/pipe-green.png')
        self.pipe_surface = pygame.transform.scale(self.pipe_surface, (pipe_width, SCREEN_HEIGHT - floor_height))

    def create_pipe(self, pipe_width, floor_height):
        randm = randint(self.window + 10, SCREEN_HEIGHT - floor_height - 10)

        new_pipe = self.pipe_surface.get_rect(midtop=(SCREEN_WIDTH + pipe_width, randm))
        self.pipe_list.append(new_pipe)

        inv_new_pipe = self.pipe_surface.get_rect(midbottom=(SCREEN_WIDTH + pipe_width, randm - self.window))
        self.pipe_list.append(inv_new_pipe)

    def dec_window(self, window_rate) : 
        print(self.window)
        self.window -= window_rate
        if(self.window < 40) : self.window = 40

    def move_pipes(self) : 
        for pipe in self.pipe_list :
            pipe.centerx -= speed
        
        while (len(self.pipe_list)!=0 and self.pipe_list[0].right<0) :
            self.pipe_list.pop(0)
    
    def draw_pipes(self, screen) : 
        for pipe in self.pipe_list : 
            if pipe.bottom >= SCREEN_HEIGHT - floor_height :
                screen.blit(self.pipe_surface, pipe)
            else :
                inv_pipe_surface = pygame.transform.flip(self.pipe_surface, False, True)
                screen.blit(inv_pipe_surface, pipe)

    def resetpipes (self, window) : 
        self.pipe_list = []
        self.window = window

class SCORE : 
    def __init__(self, game_font) -> None:
        self.currscore = 0
        self.score_surface = game_font.render('Score'+ ' ' + str(self.currscore), True, pygame.Color('white'))
        self.score_rect = self.score_surface.get_rect(topleft = (10,10))
        self.highscore = 0
        self.hs_surface = game_font.render('HighScore'+ ' ' + str(self.highscore), True, pygame.Color('white'))
        self.hs_rect = self.hs_surface.get_rect(topleft = (10,23))

    def show_score(self, screen):
        self.score_surface = game_font.render('Score ' + str(self.currscore), True, pygame.Color('white'))
        self.score_rect = self.score_surface.get_rect(topleft = (10,10))
        self.hs_surface = game_font.render('HighScore'+ ' ' + str(self.highscore), True, pygame.Color('white'))
        self.hs_rect = self.hs_surface.get_rect(topleft = (10,23))
        screen.blit(self.score_surface, self.score_rect)
        screen.blit(self.hs_surface, self.hs_rect)

    def inc_score(self) : 
        self.currscore += 1
        self.show_score(screen)
        
    def reset_score(self) : 
        if(self.currscore > self.highscore) : self.highscore = self.currscore 
        self.currscore = 0
        self.show_score(screen)
    
def check_collision(pipes, birdrect, floor_height) -> bool: 
    if(birdrect.bottom >= SCREEN_HEIGHT-floor_height or birdrect.top <=0) :
        return True
    for pipe in pipes:
        if (birdrect.colliderect(pipe)) : 
            return True
    
    return False
    
pygame.init()
pygame.display.set_caption('FlappyBirb')
SCREEN_WIDTH = 402
SCREEN_HEIGHT = 300
floor_height = 40
fps = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# game variables
game_active = False
gravity = 0.18
jump = 4
speed = 0
speed_val = 2
pipe_rate = 2000
pipe_width = 50
window = 200
window_shortening_rate = 20
window_updation_rate = 2000
flap_speed = 200
game_font = pygame.font.Font('assets/fonts/pixel.ttf', 20)

bg = BACKGROUND()

floor = FLOOR()
floor.set_height(floor_height)

bird = BIRD()
pipe = PIPES(pipe_width, window)

score = SCORE(game_font)

PIPEEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PIPEEVENT, pipe_rate)

FLAPEVENT = pygame.USEREVENT
pygame.time.set_timer(FLAPEVENT, flap_speed)

WINDOWEV = pygame.USEREVENT + 2
pygame.time.set_timer(WINDOWEV, window_updation_rate)

# ! game loop
while True :
    for event in pygame.event.get() : 
        if (event.type == pygame.QUIT) : 
            pygame.quit()
            sys.exit()
        if (event.type == pygame.KEYDOWN) :
            if (event.key == pygame.K_UP) :
                bird.set_bird_mov(-1 * jump)
            if (event.key == pygame.K_SPACE):
                game_active = True
        if (event.type == PIPEEVENT) :
            pipe.create_pipe(pipe_width, floor_height)
        if (event.type == FLAPEVENT) :
            bird.inc_idx()
        if (event.type == WINDOWEV) :
            pipe.dec_window(window_shortening_rate)
    
    bg.draw_bg(screen)
    floor.draw_floor(screen, speed)

    if(game_active) :    
        speed = speed_val
        bird.movebird(gravity, pipe, score)
        bird.draw_bird(screen)

        pipe.move_pipes()
        pipe.draw_pipes(screen)
    else :
        speed = 0
        bird.resetbird() 
        pipe.resetpipes(window)
        score.reset_score()

    if(check_collision(pipe.pipe_list ,bird.bird_rect, floor_height)) :
        game_active = False
    
    score.show_score(screen)
    pygame.display.update()
    clock.tick(fps)