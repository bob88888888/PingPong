import pygame, sys
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
pygame.init()

ball_speed = 3
slider_speed = 15

class Slider:
    def __init__(self, x, y, window_height):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 250
        self.window_height = window_height

    def move(self, dy):
        if 0 <= self.y + dy <= self.window_height - self.h:
            self.y += dy 

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y, self.w, self.h))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 25
        self.h = 25
        self.ball_dx = ball_speed
        self.ball_dy = ball_speed

    def move(self, dx, dy):
        self.x += self.ball_dx
        self.y += self.ball_dy

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 0), (self.x, self.y, self.w, self.h))

class Game:
    def __init__(self):
        self.win_width = 1900
        self.win_height = 1000
        self.window = pygame.display.set_mode((self.win_width, self.win_height))

        self.ball = Ball(self.win_width // 2, self.win_height // 2)
        self.s1 = Slider(10, self.win_height // 2, self.win_height)
        self.s2 = Slider(self.win_width - 20, self.win_height // 2, self.win_height)
        self.clock = pygame.time.Clock()

                # Initialize variables to track key states
        self.key_states = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_w: False,
            pygame.K_s: False
        }

        # Change the font and size as needed
        self.font = pygame.font.Font(None, 36) 

        # Initialize scores
        self.score1 = 0
        self.score2 = 0 

    def collision(self):
        if self.ball.x <= self.s1.x + self.s1.w and self.s1.y <= self.ball.y <= self.s1.y + self.s1.h:
            self.ball.ball_dx *= -1
        elif self.ball.x + self.ball.w >= self.s2.x and self.s2.y <= self.ball.y <= self.s2.y + self.s2.h:
            self.ball.ball_dx *= -1
        elif self.ball.y <= 0 or self.ball.y + self.ball.h >= self.win_height:
            self.ball.ball_dy *= -1

    def game_reset(self):
        # Reset ball position
        self.ball = Ball(self.win_width // 2, self.win_height // 2)

        # Reset slider positions
        self.s1 = Slider(10, self.win_height // 2, self.win_height)
        self.s2 = Slider(self.win_width - 20, self.win_height // 2, self.win_height)

    def end(self, winner):
        self.window.fill((0, 0, 0))

        self.font = pygame.font.Font(None, 50) 
      
        text_surface = self.font.render(f"Game ended, {winner} is the winner!!! \n Do you want to play again? Press Enter to play again or press Escape to quit.", True, (255, 255, 255))  
        text_rect = text_surface.get_rect(center=(self.win_width // 2, self.win_height // 2))
        self.window.blit(text_surface, text_rect)

    def main_reset(self):
        # Reset ball position
        self.ball = Ball(self.win_width // 2, self.win_height // 2)

        # Reset slider positions
        self.s1 = Slider(10, self.win_height // 2, self.win_height)
        self.s2 = Slider(self.win_width - 20, self.win_height // 2, self.win_height)

        # Reset scores
        self.score1 = 0
        self.score2 = 0

    def score(self):
        if self.ball.x <= 0 :
            self.score2 += 1
            self.game_reset()

        elif self.ball.x + self.ball.w >= self.win_width:
            self.score1 += 1
            self.game_reset()
        
    def play(self):
        pygame.display.set_caption("Ping Pong")
        self.window.fill((0, 0, 0))

        for event in GAME_EVENTS.get():
            if event.type == GAME_GLOBALS.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    self.main_reset()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  

            if event.type == pygame.KEYDOWN:
                if event.key in self.key_states:
                    self.key_states[event.key] = True

            elif event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False

        # Update slider positions based on key states
        if self.key_states[pygame.K_UP]:
            self.s2.move(-slider_speed)
        if self.key_states[pygame.K_DOWN]:
            self.s2.move(slider_speed)
        if self.key_states[pygame.K_w]:
            self.s1.move(-slider_speed)
        if self.key_states[pygame.K_s]:
            self.s1.move(slider_speed)

        # Adjust ball movement speed
        self.ball.move(self.ball.ball_dx * 1, self.ball.ball_dy * 1)
        self.collision()
        self.score()

        # Draw the ball
        self.ball.draw(self.window)

        # Render text
        text_surface = self.font.render(f"{self.score1} : {self.score2}", True, (255, 255, 255))  
        text_rect = text_surface.get_rect(center=(self.win_width // 2, self.win_height // 2))

        # Draw Sliders
        self.s1.draw(self.window)
        self.s2.draw(self.window)

        self.window.blit(text_surface, text_rect)

        if self.score1 > self.score2 and self.score1 >= 10:
            winner = "slider2"
            self.end(winner)

        elif self.score1 < self.score2 and self.score2 >= 10:
            winner = "slider1"
            self.end(winner)
        
        pygame.display.update()
        self.clock.tick(100)

if __name__ == "__main__":
    game = Game()

    while True:
        game.play()


            

