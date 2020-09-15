# Pong V2 has all attributes of the full version except the paddles do not move.

import pygame

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Pong')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.dot_center = [250, 200]
        self.dot_velocity = [5, 3]
        self.dot_radius = 10
        self.dot = Dot('white', self.dot_radius, self.dot_center, self.dot_velocity, self.surface)

        # rectangle values
        self.left_rectangle = pygame.Rect((50, 165), (10, 70))
        self.right_rectangle = pygame.Rect((440, 165), (10, 70))

        # initial score values
        self.left_score_num = 0
        self.right_score_num = 0
        
        self.continue_top_right = True
        self.continue_top_left = True
        self.continue_bottom_right = True
        self.continue_bottom_left = True
        pygame.key.set_repeat(20,20)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            self.collision()
            self.update_score()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.KEYDOWN and self.continue_game:
                self.handle_key_down(event)
         #   if event.type == pygame.KEYUP and self.continue_game:
           #     self.handle_key_up(event)

    def handle_key_down(self, event):
        size = self.surface.get_size()
        if event.key == pygame.K_q:
           self.left_rectangle.top = self.left_rectangle.top - 10
           if self.left_rectangle.top < 0:
               self.left_rectangle.top = 0
           
        if event.key == pygame.K_p:
           self.right_rectangle.top = self.right_rectangle.top - 10
           if self.right_rectangle.top < 0:
               self.right_rectangle.top = 0
           
        if event.key == pygame.K_a:
           self.left_rectangle.bottom = self.left_rectangle.bottom + 10
           if self.left_rectangle.bottom > size[1]:
               self.left_rectangle.bottom = size[1]
               
        if event.key == pygame.K_l:
           self.right_rectangle.bottom = self.right_rectangle.bottom + 10
           if self.right_rectangle.bottom > size [1]:
               self.right_rectangle.bottom = size[1]


    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        self.dot.draw()
        self.left_score()
        self.right_score()
        pygame.draw.rect(self.surface, pygame.Color('White'), self.left_rectangle)
        pygame.draw.rect(self.surface, pygame.Color('White'), self.right_rectangle)
        pygame.display.update()  # make the updated surface appear on the display

    def collision(self):
        # Detects any collision between dot and paddle and reverses x-velocity if one occurs
        # - self is the Game which detects collisions

        if self.dot_velocity[0] > 0:
            if self.right_rectangle.collidepoint(self.dot_center[0] + self.dot_radius, self.dot_center[1]):
                self.dot_velocity[0] = - self.dot_velocity[0]
        if self.dot_velocity[0] < 0:
            if self.left_rectangle.collidepoint(self.dot_center[0] - self.dot_radius, self.dot_center[1]):
                self.dot_velocity[0] = - self.dot_velocity[0]

    def left_score(self):
        # creates the left score
        # - self is the Game onto which the score is drawn

        fg_color = pygame.Color('white')
        font = pygame.font.SysFont('', 70)
        text_string = str(self.left_score_num)
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        location = (0, 0)
        self.surface.blit(text_box, location)

    def right_score(self):
        # creates the right score
        # - self is the Game onto which the score is drawn

        fg_color = pygame.Color('White')
        font = pygame.font.SysFont('', 70)
        text_string = str(self.right_score_num)
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        location = (self.surface.get_width()-text_box.get_width(), 0)
        self.surface.blit(text_box, location)

    def update_score(self):
        # updates the scores on the left and right
        # - self is the Game to update

        if self.dot_center[0] - self.dot_radius <= 0:  # left edge
            self.right_score_num += 1
        if self.dot_center[0] + self.dot_radius >= self.surface.get_width():  # right edge
            self.left_score_num += 1


    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.dot.move()

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if self.left_score_num == 11 or self.right_score_num == 11:
            self.continue_game = False


class Dot:
    # An object in this class represents a Dot that moves

    def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the pygame.Color of the dot
        # - center is a list containing the x and y int
        #   coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object

        self.color = pygame.Color(dot_color)
        self.radius = dot_radius
        self.center = dot_center
        self.velocity = dot_velocity
        self.surface = surface

    def move(self):
        # dictates the movement of the dot including how it bounces of window edges
        # - self is the Dot

        size = self.surface.get_size()
        for i in range(0, 2):
            self.center[i] = (self.center[i] + self.velocity[i])
            if self.center[i] <= self.radius:
                self.velocity[i] = - self.velocity[i]
            if self.center[i] + self.radius >= size[i]:
                self.velocity[i] = - self.velocity[i]

    def draw(self):
        # Draw the dot on the surface
        # - self is the Dot

        pygame.draw.circle(self.surface, self.color, self.center, self.radius)

main()
