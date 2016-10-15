import pygame
from app.game_of_life import GameOfLife

class Screen:

    def __init__(self):
        self.height    = 704  # Set screen height
        self.width     = 1024 # Set screen width
        self.cell_size = 32   # Determine the size of a cell on screen

        self.title = "Conway's Game of Life"

        # Create a new game of life that will fit inside our window
        self.gol = GameOfLife(
            self.width//self.cell_size,
            self.height//self.cell_size
        )

        # Set up a few state variables
        self.animating = False
        self.step      = False
        self.mouse_effect = self.gol.ALIVE

    def update(self):
        # If we're animating or stepping, then advance the game
        if self.animating or self.step:
            self.gol.update()
            # If we stepped, cease all animation after the step
            if self.step:
                self.animating = False
                self.step      = False

        if self.animating:
            pygame.display.set_caption(self.title + " - Animating")
        else:
            pygame.display.set_caption(self.title)

    def render(self):
        # Create blank surface and fill with white
        surface = pygame.Surface((self.width, self.height))
        surface.fill((255,255,255))

        # Draw Horizontal Grid lines
        for y in range(self.gol.get_height()):
            pygame.draw.line(
                surface,
                (0,0,0),
                (0,y*self.cell_size),
                (self.width,y*self.cell_size)
            )

        # Draw Vertical Grid lines
        for x in range(self.gol.get_width()):
            pygame.draw.line(
                surface,
                (0,0,0),
                (x*self.cell_size,0),
                (x*self.cell_size,self.height)
            )

        for y in range(self.gol.get_height()):
            for x in range(self.gol.get_width()):
                # Draw live cells in blue colour
                if self.gol.get_cell(x,y) == self.gol.ALIVE:
                    pygame.draw.rect(
                        surface,
                        (0,0,255),
                        (
                            self.cell_size*x,
                            self.cell_size*y,
                            self.cell_size,
                            self.cell_size
                        ))
        return surface

    def __game_loop(self):
        clock = pygame.time.Clock()
        frame_count = 0   # We'll update the game every 15 fames. Keep track of
        update_frame = 15 # what frame we're on

        while True:
            # Regulate framerate
            clock.tick(60)

            # Check for any useful events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit() # player has quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == event.key == pygame.K_SPACE:
                        # Player hit spacebar. Either start or stop animating
                        self.animating = not self.animating
                    elif (event.key == pygame.K_UP or
                        event.key == pygame.K_DOWN or
                        event.key == pygame.K_RIGHT or
                        event.key == pygame.K_LEFT):
                        # Player pressed an arrow key. Advance the state of the
                        # game by one
                        self.step = True
                    elif event.key == pygame.K_c:
                        # Player pressed an arrow key. Advance the state of the
                        # game by one
                        self.gol.reset()
                        self.step = False
                        self.animating=False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Player clicked on a square. Flip it's state and store
                    # the action in case they start dragging
                    pos = pygame.mouse.get_pos()
                    x = pos[0]//self.cell_size
                    y = pos[1]//self.cell_size
                    self.mouse_effect = 1-self.gol.get_cell(x,y)
                    self.gol.set_cell(x,y, self.mouse_effect)
                elif event.type == pygame.MOUSEMOTION:
                    # Check to see if user is dragging their mouse across
                    # The screen. If so, set the states of any cells they move
                    # over as appropriate
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        x = pos[0]//self.cell_size
                        y = pos[1]//self.cell_size
                        self.gol.set_cell(x,y, self.mouse_effect)

            # Keep track of elapsed frames
            frame_count = frame_count+1

            # Update game if frame is multiple of 15
            if frame_count % update_frame == 0:
                self.update()

            # Display the game state
            render = self.render()
            self.screen.blit(render, (0,0))
            pygame.display.flip()

    def __initialize_display(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def run(self):
        self.__initialize_display()
        self.__game_loop()

    def quit(self):
        exit()
