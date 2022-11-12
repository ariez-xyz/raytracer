import sys
import pygame

class Canvas:
    def __init__(self, realtime_update=False) -> None:
        pygame.init()

        self.width = 300
        self.height = 300
        self.canvas = pygame.display.set_mode((self.width, self.height))

        # Draw the canvas to screen after each set_color. 
        # Pygame docs say Surface.set_at is slow, but this is a software renderer, soo...
        self.realtime_update = realtime_update

    def set_color(self, x, y, color):
        # Translate from center-origin coordinate system to top-left origin.
        x = self.width // 2 + x
        y = self.height // 2 - y

        # Clamp values to [0, 255]
        color = [val if 0 <= val <= 255 else max(0,min(255,val)) for val in color]

        self.canvas.set_at((x, y), color)

        if self.realtime_update:
            self.draw()

    def draw(self):
        pygame.display.flip()
    
    def block_till_exit(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


if __name__ == "__main__":
    canvas = Canvas(realtime_update=True)
    canvas.set_color(0,0,(256,0,0))
    canvas.block_till_exit()

