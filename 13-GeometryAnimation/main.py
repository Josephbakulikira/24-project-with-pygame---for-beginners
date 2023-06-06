import pygame
from constants import *
import math

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Basic Trigonometric functions")
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

    pygame.quit()

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fps = 60
        self.running = True
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)
        self.circle = Circle()
        self.cosWave = Wave()
        self.sinWave = Wave()
        self.showText = False

        self.angle = 0
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()
            
            x = self.circle.radius * math.cos(self.angle)+ self.circle.x 
            y = self.circle.radius * -math.sin(self.angle)+ self.circle.y

            pygame.draw.line(self.screen, GRAY, (self.circle.x, self.circle.y), (x, y), 2)
            # HORIZONTAL line x-axis
            pygame.draw.line(self.screen, GRAY2, 
                            (self.circle.x - self.circle.radius - LINE_EXTENSION, self.circle.y), 
                            (self.circle.x + self.circle.radius + LINE_EXTENSION, self.circle.y),
                             2)
            # VERTICAL line y-axis
            pygame.draw.line(self.screen, GRAY2, 
                            (self.circle.x , self.circle.y + self.circle.radius + LINE_EXTENSION), 
                            (self.circle.x , self.circle.y - self.circle.radius - LINE_EXTENSION),
                             2)
            # SIN LINE AND TEXT
            sin_text = self.font.render("Sinθ", True, SIN_COLOR)
            pygame.draw.line(self.screen, SIN_COLOR,
                            (x, y),
                            (x, self.circle.y),
                            2
            )
            self.sinWave.points.insert(0, (x, y))

            if len(self.sinWave.points) > WAVE_LENGTH:
                self.sinWave.points.pop()
                self.cosWave.points.pop()
            
            # COSIN LINE AND TEXT
            cos_text = self.font.render("Cosθ", True, COS_COLOR)
            pygame.draw.line(self.screen, COS_COLOR,
                            (x, y),
                            (self.circle.x, y),
                            2
            )
            self.cosWave.points.insert(0, (x, y))

            # Angle value
            convertToDegree = int(math.degrees(self.angle))
            angle_text = self.font.render(f"{convertToDegree}°", True, WHITE)

            # calculate values 
            if self.angle > 0:
                sec = self.circle.radius / math.cos(self.angle)
                cosec = self.circle.radius / math.sin(self.angle)
                tan = self.circle.radius * (math.sin(self.angle) / math.cos(self.angle))
                cotan = self.circle.radius * (math.cos(self.angle) / math.sin(self.angle))

                # Draw Sec line
                pygame.draw.line(self.screen, SEC_COLOR, 
                                    (self.circle.x, self.circle.y),
                                    (self.circle.x + sec, self.circle.y),
                                    2)
                sec_text = self.font.render("secθ", True, SEC_COLOR)

                # Draw Cosec line
                pygame.draw.line(self.screen, COSEC_COLOR, 
                                    (self.circle.x, self.circle.y),
                                    (self.circle.x , self.circle.y - cosec),
                                    2)
                cosec_text = self.font.render("cosecθ", True, COSEC_COLOR)

                # Tan line
                pygame.draw.line(self.screen, TAN_COLOR,
                                    (x, y),
                                    (self.circle.x + int(sec), self.circle.y), 2)
                tan_text = self.font.render("tanθ", True, TAN_COLOR)
                
                # CoTan line
                pygame.draw.line(self.screen, COTAN_COLOR,
                                    (x, y),
                                    (self.circle.x, self.circle.y - + int(cosec)), 2)
                cotan_text = self.font.render("cotanθ", True, COTAN_COLOR)

                if self.showText:
                    self.screen.blit(sin_text, (x, y - (y - self.circle.y)//2))
                    self.screen.blit(cos_text, ( x  - (x - self.circle.x)//2, y))
                    self.screen.blit(sec_text, (self.circle.x + sec//2, self.circle.y))
                    self.screen.blit(cosec_text, (self.circle.x, self.circle.y - cosec//2))
                    self.screen.blit(tan_text, (self.circle.x + sec//2, self.circle.y + (y - self.circle.y)//2 ))
                    self.screen.blit(cotan_text, (self.circle.x - (self.circle.x - x)//2 , self.circle.y - cosec//2))
                    self.screen.blit(angle_text, (self.circle.x + 20, self.circle.y + 20))

            self.circle.Draw(self.screen)
            self.cosWave.Draw(self.screen, self.circle, False)
            self.sinWave.Draw(self.screen, self.circle, True)

            pygame.draw.circle(self.screen, GREEN, (x, y), 10)

            pygame.display.update()
            self.angle += ROTATING_SPEED
            if self.angle > math.pi * 2:
                self.angle = 0
            self.clock.tick(self.fps)

    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.showText = not self.showText

class Circle:
    def __init__(self, x=WIDTH//2, y=HEIGHT//2, radius=CIRCLE_RADIUS):
        self.x = x
        self.y = y
        self.radius = radius
        self.thickness = 3
        self.color = WHITE
    
    def Draw(self, screen):
        # origin point
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.thickness)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.thickness)

class Wave:
    def __init__(self):
        self.points = []
        self.thickness = 4
        self.color = WAVE_COLOR
    
    def Draw(self, screen,circle, horizontal=True):
        offset = 1
        
        for i in range(1, len(self.points)):
            x1, y1 = self.points[i][0], self.points[i][1]
            x2, y2 = self.points[i][0], self.points[i][1]

            if horizontal:
                # add offsets
                x1 = circle.x + i * offset
                x2 = circle.x + i * offset
            else:
                y1 = circle.y + i * offset
                y2 = circle.y + i * offset
            pygame.draw.line(screen, self.color, (x1, y1), (x2, y2), self.thickness)

if __name__ == "__main__":
    main()