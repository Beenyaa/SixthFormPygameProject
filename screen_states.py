# IMPORTS
import constants
import pygame
import objects
import user
import scores_handler

# GRAPHICS LOADER FUNCTION:


class LoadInGraphics:
    def __init__(self, image_file, location):
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.left, self.rect.top = location

    def get_collide_coords(self, coordinates):
        return self.rect.collidepoint(coordinates[0], coordinates[1])


# SCREEN STATES:


class Menu:
    def __init__(self, game):
        self.game = game

        # INITIALISE GRAPHICS:
        self.background = LoadInGraphics(constants.BACKGROUND_MENU, [0, 0])
        self.title = LoadInGraphics(constants.LOGO, [-3, 30])
        self.play_button = LoadInGraphics(constants.PLAY_BUTTON, [140, 250])
        self.highscore_button = LoadInGraphics(constants.HIGHSCORE_BUTTON, [67, 350])
        self.help_button = LoadInGraphics(constants.HELP_BUTTON, [140, 450])
        self.quit_button = LoadInGraphics(constants.QUIT_BUTTON, [140, 550])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.play_button.get_collide_coords(event.pos):
                    self.game.add_state(Gameplay(self.game))
                elif self.highscore_button.get_collide_coords(event.pos):
                    self.game.add_state(Highscore(self.game))
                elif self.help_button.get_collide_coords(event.pos):
                    self.game.add_state(Help(self.game))
                elif self.quit_button.get_collide_coords(event.pos):
                    self.game.done = True

    def update(self):
        pass

    def draw(self):
        self.game.screen.blit(self.background.image, self.background.rect)
        self.game.screen.blit(self.title.image, self.title.rect)
        self.game.screen.blit(self.play_button.image, self.play_button.rect)
        self.game.screen.blit(self.highscore_button.image, self.highscore_button.rect)
        self.game.screen.blit(self.help_button.image, self.help_button.rect)
        self.game.screen.blit(self.quit_button.image, self.quit_button.rect)


class Highscore:
    def __init__(self, game):
        self.game = game
        self.scoreboard = scores_handler.Scoreboard()

        # INITIALISE GRAPHICS:
        self.background = LoadInGraphics(constants.BACKGROUND_MENU, [0, 0])
        self.back_button = LoadInGraphics(constants.BACK_BUTTON, [110, 600])

        self.font = pygame.font.Font(constants.FONT_TYPE, constants.FONT_SIZE_FOR_DISPLAY)
        self.scoreboard_info = self.scoreboard.display()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.back_button.get_collide_coords(event.pos):
                    self.game.remove_last_state()

    def draw(self):
        text = self.font.render(self.scoreboard_info, True, constants.WHITE)
        rect = text.get_rect()

        rect.center = (self.game.screen.get_rect().center[0] - rect.width / 2,
                       self.game.screen.get_rect().center[1] - rect.height / 2)

        self.game.screen.blit(self.background.image, self.background.rect)
        self.game.screen.blit(self.back_button.image, self.back_button.rect)
        self.game.screen.blit(text, rect.center)

    def update(self):
        pass


class Help:
    def __init__(self, game):
        self.game = game

        # INITIALISE GRAPHICS:
        self.background = LoadInGraphics(constants.BACKGROUND_MENU, [0, 0])
        self.info1 = LoadInGraphics(constants.CONTROLS1, [70, 100])
        self.info2 = LoadInGraphics(constants.CONTROLS2, [50, 146])
        self.sound_button = LoadInGraphics(constants.SOUND_BUTTON, [120, 200])
        self.off_signal = LoadInGraphics(constants.OFF_SIGNAL, [154, 235])
        self.back_button = LoadInGraphics(constants.BACK_BUTTON, [110, 600])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.back_button.get_collide_coords(event.pos):
                    self.game.remove_last_state()

    def draw(self):
        self.game.screen.blit(self.background.image, self.background.rect)
        self.game.screen.blit(self.info1.image, self.info1.rect)
        self.game.screen.blit(self.info2.image, self.info2.rect)
        self.game.screen.blit(self.sound_button.image, self.sound_button.rect)
        self.game.screen.blit(self.off_signal.image, self.off_signal.rect)
        self.game.screen.blit(self.back_button.image, self.back_button.rect)

    def update(self):
        pass


class Gameplay:
    def __init__(self, game):
        self.game = game

        # INITIALISE GRAPHICS:
        self.background = LoadInGraphics(constants.BACKGROUND_MENU, [0, 0])

        # INITIALISE IN-GAME OBJECTS:
        self.ball = objects.Ball()
        self.right_paddle = objects.Paddle(265, 598, False)
        self.left_paddle = objects.Paddle(105, 598, True)
        self.playfield = objects.Playfield()
        self.spring = objects.Spring()
        self.deadzone = objects.Deadzone()
        self.point1 = objects.Point(50, 200)
        self.point2 = objects.Point(200, 230)
        self.point3 = objects.Point(190, 320)
        self.point4 = objects.Point(320, 450)
        self.point5 = objects.Point(238, 100)

        # list of object that feeds into the Ball's update method. Every object in this list is checked for collision
        # with the Ball.

        self.objects_list = [self.playfield,
                             self.right_paddle,
                             self.left_paddle,
                             self.spring,
                             self.deadzone,
                             self.point1,
                             self.point2,
                             self.point3,
                             self.point4,
                             self.point5]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.done = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.game.add_state(Pause(self.game))
                if event.key == pygame.K_d:
                    self.right_paddle.stop_rotate()
                if event.key == pygame.K_a:
                    self.left_paddle.stop_rotate()
                if event.key == pygame.K_SPACE:
                    self.spring.stop_charging()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.right_paddle.rotate_paddle()
                if event.key == pygame.K_a:
                    self.left_paddle.rotate_paddle()
                if event.key == pygame.K_SPACE:
                    self.spring.start_charging()

    def draw(self):
        # RENDER GRAPHICS:
        self.game.screen.blit(self.background.image, self.background.rect)
        self.spring.draw(self.game.screen)
        self.playfield.draw(self.game.screen)
        self.ball.draw(self.game.screen)
        self.right_paddle.draw(self.game.screen)
        self.left_paddle.draw(self.game.screen)
        self.point1.draw(self.game.screen)
        self.point2.draw(self.game.screen)
        self.point3.draw(self.game.screen)
        self.point4.draw(self.game.screen)
        self.point5.draw(self.game.screen)
        self.deadzone.draw(self.game.screen)

    def update(self):
        self.spring.update()
        self.right_paddle.update()
        self.left_paddle.update()
        self.ball.update(list(self.objects_list))
        score = self.ball.get_score()  # gets the number of scores that the is collected by the Ball

        if self.ball.get_lives() <= 0:
            self.game.add_state(SubmitScore(self.game, int(score)))


class Pause:
    def __init__(self, game):
        self.game = game

        # INITIALISE GRAPHICS:
        self.pause_background = LoadInGraphics(constants.PAUSE_BACKGROUND, (0, 0))
        self.pause_button = LoadInGraphics(constants.PAUSE_BUTTON, (119, 323))

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.done = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.game.remove_last_state()

    def draw(self):
        self.game.screen.blit(self.pause_background.image, self.pause_background.rect, )
        self.game.screen.blit(self.pause_button.image, self.pause_button.rect)

    def update(self):
        pass


class SubmitScore:
    def __init__(self, game, passed_score):
        self.game = game
        self.score = passed_score

        self.player = user.Player()

        # INITIALISE GRAPHICS:
        self.background = LoadInGraphics(constants.BACKGROUND_MENU, [0, 0])
        self.submit_score_text = LoadInGraphics(constants.SUBMIT_TEXT, [23, 50])
        self.name_text = LoadInGraphics(constants.NAME_TEXT, [125, 100])
        self.back_button = LoadInGraphics(constants.BACK_BUTTON, [110, 600])

        self.max_reached = False
        self.max_name_characters = 7
        self.name = ""
        self.font = pygame.font.Font(constants.FONT_TYPE, constants.FONT_SIZE_FOR_SUBMIT)

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.done = True

            elif event.type == pygame.MOUSEBUTTONUP:

                if self.back_button.get_collide_coords(event.pos):
                    # remove two screen states to take the user back to the Main Menu
                    # amd pass user's name and score to user.py file
                    self.player.save_playtime_info(self.name, self.score)
                    self.game.remove_last_state()
                    self.game.remove_last_state()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(self.name) > 0:
                    self.name = self.name[:-1]

                if event.key == pygame.K_RETURN:
                    # remove two screen states to take the user back to the Main Menu
                    # and pass user's name and score to user.py file
                    self.player.save_playtime_info(self.name, self.score)
                    self.game.remove_last_state()
                    self.game.remove_last_state()

                if self.max_reached == False:
                    if event.unicode.isalpha() or event.unicode.isnumeric():
                        self.name += event.unicode

    def update(self):
        if len(self.name) >= self.max_name_characters:
            self.max_reached = True

        else:
            self.max_reached = False

    def draw(self):
        text = self.font.render(self.name, True, constants.WHITE)
        rect = text.get_rect()

        rect.center = (self.game.screen.get_rect().center[0] - rect.width / 2,
                       self.game.screen.get_rect().center[1] - rect.height / 2)

        self.game.screen.blit(self.background.image, self.background.rect, )
        self.game.screen.blit(self.back_button.image, self.back_button.rect)
        self.game.screen.blit(self.submit_score_text.image, self.submit_score_text.rect)
        self.game.screen.blit(self.name_text.image, self.name_text.rect)
        self.game.screen.blit(text, rect.center)