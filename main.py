# IMPORTS:
import pygame
import constants
import screen_states


class Game:

    # This class is responsible for handling different
    # game states and keeping them updated.

    def __init__(self):
        pygame.init()

        self.size = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.done = False
        self.clock = pygame.time.Clock()
        self.screensStack = []

    def get_current_state(self):
        return self.screensStack[len(self.screensStack)-1]

    def add_state(self, state):
        self.screensStack.append(state)

    def remove_last_state(self):
        self.screensStack.pop()

    # MAIN GAME LOOP: most of the game will
    # take place within this "while" loop.

    def run(self):
        self.add_state(screen_states.Menu(self))
        while not self.done:
            caption = "{} - FPS: {:.2f}".format(constants.GAME_WINDOW_CAPTION, self.clock.get_fps())
            pygame.display.set_caption(caption)
            self.clock.tick(constants.FPS)
            self.get_current_state().handle_events()
            self.get_current_state().update()
            self.get_current_state().draw()
            pygame.display.flip()

        pygame.quit()

# main_loop.Run method is the game loop.


if __name__ == "__main__":
    main_loop = Game()
    main_loop.run()
