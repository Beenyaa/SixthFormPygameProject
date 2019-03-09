
# IMPORTS:

import pygame
import constants

# IN-GAME OBJECTS:


class Ball:

    def __init__(self):
        self.object_type = "Ball"  # string type identifier to distinguish object type
        self.lives = 3  # amount of lives when beginning the game
        self.collected_scores = 0  # temporary stores the scores until the game finishes

        self.x = constants.INITIAL_BALL_RENDER_X  # initial x position
        self.y = constants.INITIAL_BALL_RENDER_Y  # initial y position

        self.x_speed = 0.0  # initial speed on x axis
        self.y_speed = 0.0  # initial speed on y axis

        self.gravity = 0.980665  # the constant gravity that is applied on the speed of the y axis of the ball
        self.max_speed = 30.0  # maximum value the speed can reach on each axis
        self.ball = pygame.image.load(constants.BALL).convert_alpha()  # load graphics
        self.ball = pygame.transform.smoothscale(self.ball, (constants.BALL_SIZE, constants.BALL_SIZE))
        # resize graphics
        self.mask = pygame.mask.from_surface(self.ball)  # get mask of graphics
        self.rect = self.ball.get_rect()  # get ball dimensions (x,y,width,height)

    def get_lives(self):  # getter
        return int(self.lives)

    def get_score(self):  # getter
        return int(self.collected_scores)

    def draw(self, screen):
        # method draws ball graphics on the screen from origin of x and y positions
        screen.blit(self.ball, (self.x, self.y))

    def set_speed(self, speed):
        self.x_speed = speed

    def update(self, objects_list):
        # method handles interactions between the in-game objects and the Ball

        if self.max_speed <= self.x_speed:
            self.x_speed = self.max_speed
            # this makes sure that if the x speed of the ball surpasses its defined limit then the
            # x speed gets reset, making the x speed equal the maximum speed limit.

        # changes ball x position
        self.x += self.x_speed

        # interactions on x-axis:
        for in_game_object in objects_list:
            object_x = in_game_object.get_x()
            object_y = in_game_object.get_y()

            # finds offset between Ball and current in-game object
            offset = (int(self.x - object_x), int(self.y - object_y))

            # check if ball has collided with anything
            has_collided = in_game_object.mask.overlap(self.mask, offset)

            if in_game_object.object_type == "Paddle":
                # if current object is of Paddle type
                if has_collided:
                    # and if Ball and object collided THEN:
                    # dampen x speed and repel ball the opposite direction by the new speed.
                    self.x_speed *= -in_game_object.bounce_factor
                    self.x -= self.x_speed
                    break

            elif in_game_object.object_type == "Playfield":
                # if current object is of Playfield type
                if has_collided:
                    # if current object and Ball has collided THEN:
                    # repel Ball opposite direction and dampen the x speed by bounce factor
                    self.x -= self.x_speed
                    self.x_speed *= -in_game_object.bounce_factor
                    break

            elif in_game_object.object_type == "Spring":
                # if current object is of Spring type
                if has_collided:
                    # if current object and Ball has collided THEN:
                    # repel Ball opposite direction and dampen the x speed by bounce factor
                    self.x -= self.x_speed
                    self.x_speed *= -in_game_object.bounce_factor
                    break

            elif in_game_object.object_type == "Deadzone":
                # if current object is of Deadzone type
                if has_collided:
                    # if current object and Ball has collided THEN:
                    # x_speed is reset to 0 and its position is reset to its original position
                    self.x_speed = 0.0
                    self.x = constants.INITIAL_BALL_RENDER_X
                    break

            elif in_game_object.object_type == "Point":
                # if current object is of Point type
                if has_collided:
                    self.collected_scores += in_game_object.score_worth
                    break

        # interactions on the y axis:
        if self.max_speed <= self.y_speed:
            self.y_speed = self.max_speed
            # this makes sure that if the y speed of the ball surpasses its defined limit then the
            # y speed gets reset, making the y speed equal the maximum speed limit.

        self.y_speed += self.gravity  # gravity constantly accelerates the y speed
        self.y += self.y_speed  # the y speed changes the y position of the Ball

        for in_game_object in objects_list:
            object_x = in_game_object.get_x()
            object_y = in_game_object.get_y()
            # find offset between ball and object
            offset = (int(self.x - object_x), int(self.y - object_y))

            # check if ball has collided with anything
            has_collided = in_game_object.mask.overlap(self.mask, offset)

            if in_game_object.object_type == "Paddle":
                # if current object is of Paddle type
                if has_collided:
                    # if current object and Ball has collided THEN:
                    # repel Ball opposite direction and dampen the x speed by bounce factor
                    self.y -= self.y_speed
                    self.y_speed *= -in_game_object.bounce_factor
                    break

            elif in_game_object.object_type == "Playfield":
                # if current object is of Playfield type
                if has_collided:
                    # if current object and Ball has collided THEN:
                    # repel Ball opposite direction and dampen the x speed by bounce factor
                    self.y -= self.y_speed
                    self.y_speed *= -in_game_object.bounce_factor
                    break

            elif in_game_object.object_type == "Spring":
                # if current object is of Spring type
                if has_collided:
                    # if current object and Ball has collided THEN:
                    # repel Ball opposite direction and dampen the x speed by bounce factor
                    self.y -= self.y_speed
                    self.y_speed *= -in_game_object.bounce_factor
                    break

            elif in_game_object.object_type == "Deadzone":
                # if current object is of Deadzone type
                if has_collided:
                    self.lives -= 1
                    self.y_speed = 0.0
                    self.y = constants.INITIAL_BALL_RENDER_Y
                    break

            elif in_game_object.object_type == "Point":
                # if current object is of Point type
                if has_collided:
                    # if current object and Ball has collided THEN:
                    # the score worth of the Point object gets added
                    self.collected_scores += in_game_object.score_worth
                    break


class Playfield:

    def __init__(self):
        self.object_type = "Playfield"  # string type identifier to distinguish object type

        self.playfield = pygame.image.load(constants.PLAYFIELD).convert_alpha()  # load graphics
        self.playfield = pygame.transform.smoothscale(self.playfield, (400, 680))
        self.mask = pygame.mask.from_surface(self.playfield)  # get mask of graphics
        self.rect = self.playfield.get_rect()  # gets playfield dimensions (x,y,width,height)

        self.bounce_factor = 0.8  # float type identifier for the bounce interaction of the ball with this object type

    def get_x(self):  # getter
        # method gets the x value of the playfield
        return int(self.rect.x)

    def get_y(self):  # getter
        # method gets the y value of the playfield
        return int(self.rect.y)

    def draw(self, screen):
        # method draws playfield from the origin of x and y values
        screen.blit(self.playfield, (self.rect.x, self.rect.y))


class Paddle(object):

    def __init__(self, x, y, left):
        self.object_type = "Paddle"  # string type identifier to distinguish object type
        self.rotating = False   #
        self.left = left        # instance of "left" parameter boolean value (either True or False)
        self.degrees = 0        # original starting point for the paddle

        if left:            # if the Paddle object is the left Paddle, the equalizer variable is set to -1
            equalizer = -1  # to deal with the calculations respectively opposite to the right Paddle.

        else:               # else the Paddle object is the right Paddle, the equalizer variable is set to 1
            equalizer = 1   # to deal with the calculations respectively opposite to the left Paddle

        self.rot_acc = 3.25 * equalizer        # rotation acceleration
        self.rot_speed = 1 * equalizer      # rotation speed
        self.max_rotate = 80 * equalizer    # maximum rotation by angle
        self.return_speed = -8 * equalizer  # speed of rotation to return paddle

        self.og_rot_speed = self.rot_speed  # save the original rotation speed for later use
        self.bounce_factor = 1.25  # float type identifier for the bounce interaction of the ball with this object type

        self.original_paddle = pygame.image.load(constants.PADDLE_SPRITE).convert_alpha()      # load in graphics
        self.original_paddle = pygame.transform.smoothscale(self.original_paddle, (120, 105))  # rescale graphics

        if left:
            # reflect graphics on y axis
            self.original_paddle = pygame.transform.flip(self.original_paddle, self.left, False)

        self.rotated_paddle = pygame.transform.rotozoom(self.original_paddle, 0, 1)   # rotate graphics
        self.mask = pygame.mask.from_surface(self.rotated_paddle)                # get mask of graphics
        self.rect = self.original_paddle.get_rect()       # get dimensions of paddle (x,y,width,height)
        self.rect.center = (x, y)     # set the centre x y points of the graphics as the x and y inputs

    def get_x(self):  # getter
        return int(self.rect.x)

    def get_y(self):  # getter
        return int(self.rect.y)

    def draw(self, screen):
        # method draws the rotated paddle from the origin of x and y values
        screen.blit(self.rotated_paddle, self.rect)

    def rotate_paddle(self):  # setter
        self.rotating = True

    def stop_rotate(self):  # setter
        self.rotating = False

    def update(self):
        
        if self.rotating:
            # If the instance is rotating THEN:

            # rotation speed is increased by the rotation acceleration and
            #  the degrees are increase by the rotation speed
            self.rot_speed += self.rot_acc
            self.degrees += self.rot_speed

            if (not self.left and self.degrees >= self.max_rotate) or (self.left and self.degrees <= self.max_rotate):
                # This comparison checks whether the instance of the paddle is: NOT reflected AND its degrees are higher
                # or equal to the maximum limit OR the instance IS reflected AND its degrees are less or equal to the
                # maximum limit.

                # If so:

                # reset rotation speed to original value of the instance to avoid the "jumping" of the paddle
                # and make the degrees equal the maximum limit to avoid over turning
                self.rot_speed = self.og_rot_speed
                self.degrees = self.max_rotate

            # instance of paddle is being rotated and the rect and mask is updated for accurate collision detection
            self.rotated_paddle = pygame.transform.rotozoom(self.original_paddle, -self.degrees, 1)
            self.rect = self.rotated_paddle.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.rotated_paddle)

        else:
            # If the instance is not rotating THEN:

            # reduce degrees by the return speed
            self.degrees += self.return_speed

            if (not self.left and self.degrees <= 0) or (self.left and self.degrees >= 0):
                # This comparison checks whether the instance of the paddle is: NOT reflected AND its degrees are less
                # than or equal to 0 OR the instance IS reflected AND its degrees are higher or equal to 0.

                # If so:

                # make the instance's degrees equal 0
                self.degrees = 0

            # instance of paddle is being rotated and the rect and mask is updated for accurate collision detection
            self.rotated_paddle = pygame.transform.rotozoom(self.original_paddle, -self.degrees, 1)
            self.rect = self.rotated_paddle.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.rotated_paddle)


class Point:

    def __init__(self, x, y):
        self.object_type = "Point"  # string type identifier to distinguish object type
        self.x_pos = x  # x position is equal to the passed in integer
        self.y_pos = y  # y position is equal to the passed in integer
        self.score_worth = 5  # upon touching one total score is increased by 5
        self.point = pygame.image.load(constants.POINT_SPRITE).convert_alpha()  # load in graphics
        self.point = pygame.transform.smoothscale(self.point, (constants.POINT_SIZE, constants.POINT_SIZE))
        # resize graphics
        self.mask = pygame.mask.from_surface(self.point)  # get mask of graphics

    def draw(self, screen):
        # method draws point from the origin of x and y values
        screen.blit(self.point, (self.x_pos, self.y_pos))

    def get_x(self):  # getter
        return int(self.x_pos)

    def get_y(self):  # getter
        return int(self.y_pos)


class Spring:

    def __init__(self):
        self.object_type = "Spring"  # string type identifier to distinguish object type
        self.x = constants.INITIAL_SPRING_RENDER_X  # initial x position
        self.y = constants.INITIAL_SPRING_RENDER_Y  # initial y position

        self.spring = pygame.image.load(constants.SPRING_SPRITE).convert_alpha()  # load in graphics
        self.spring = pygame.transform.smoothscale(self.spring, (constants.SPRING_WIDTH, constants.SPRING_HEIGHT))
        # resize graphics
        self.mask = pygame.mask.from_surface(self.spring)  # get mask for graphics

        self.bounce_factor = 0.35  # initial bounce factor
        self.max_bounce_factor = 10.0  # maximum limit for bounce factor
        self.charging = False  # the initial boolean identifier for the two states that the spring has
        self.lowering_speed = 0.02  # the initial lowering speed
        self.lowering_acc = 0.02  # lowering acceleration that gets added to lowering speed
        self.return_speed = 3  # the initial return speed
        self.return_acc = 0.75  # returning acceleration that gets added to return speed
        self.max_lowering = 40  # maximum limit to how much the spring can be lowered
        self.bounce_factor_charger = 0.15  # bounce factor is increased by this amount
        self.ticks = 0  # initial ticks
        self.charger = 0.0  # initial charger

    def get_x(self):  # getter
        # returns current x position
        return int(self.x)

    def get_y(self):  # getter
        # returns current y position
        return int(self.y)

    def draw(self, screen):
        # method draws the moving spring from the origin of x and y values
        screen.blit(self.spring, (self.x, self.y))

    def start_charging(self):  # setter
        self.charging = True

    def stop_charging(self):  # setter
        self.charging = False

    def charging_charger(self, ticks_taken):
        # the amount of ticks taken for: while the spring was being charged gets multiplied by the bounce factor charger
        # which is a constant float number.
        charger = self.bounce_factor_charger * ticks_taken
        # the charger value gets returned as a float number
        return float(charger)

    def update(self):

        # local variables for later use are declared here:

        og_y_pos = constants.INITIAL_SPRING_RENDER_Y
        og_charger = 0.0
        og_bounce_factor = 0.55
        og_lowering_speed = 0.125

        if self.charger > self.max_bounce_factor and self.bounce_factor > self.max_bounce_factor:
            # if the charger is greater than or equal to the maximum limit for bounce factor
            # then bounce factor equals the maximum limit and charger is reset to 0.

            self.bounce_factor = self.max_bounce_factor
            self.charger = og_charger

        elif self.charging:

            # if self.charging is True, then Spring y position is continuously lowered by
            # the speed and added acceleration.

            self.lowering_speed += self.lowering_acc
            self.y += self.lowering_speed

            if self.y >= (self.max_lowering + og_y_pos):

                # if y position is greater or equal to the total of maximum lowering limit,
                # then lowering speed is reset and y position equalised to the maximum
                # lowering limit.

                self.lowering_speed = og_lowering_speed
                self.y = self.max_lowering + og_y_pos
                self.bounce_factor = og_bounce_factor

            if self.y <= (self.max_lowering + og_y_pos):

                # if y position is smaller or equal to the maximum lowering limit, then
                # the ticks are counted for every tick this condition is True.

                self.ticks += 1
                self.bounce_factor = og_bounce_factor

        else:

            # else self.charging is NOT True, then spring is returned to original position
            # and new bounce factor is applied if there is one to repel the Ball.

            self.return_speed += self.return_acc
            self.y -= self.return_speed
            self.charger += self.charging_charger(self.ticks)  # ticks are passed into the charging_charger method
            self.bounce_factor += self.charger  # the value received from the prior method charges the bounce factor
            self.charger = og_charger

            if self.y <= og_y_pos:

                # if the y position is   less  than or equal to the original
                # y position, then reset all attributes to original values.
                # Resetting spring takes place here.

                self.return_speed = 1
                self.y = og_y_pos
                self.charger = og_charger
                self.bounce_factor = og_bounce_factor
                self.ticks = 0
                self.lowering_speed = og_lowering_speed


class Deadzone:

    def __init__(self):
        self.object_type = "Deadzone"  # string type identifier to distinguish object type
        self.x = constants.INITIAL_DEADZONE_RENDER_X  # initial x position
        self.y = constants.INITIAL_DEADZONE_RENDER_y  # initial y position
        self.deadzone = pygame.image.load(constants.DEADZONE_SPRITE).convert_alpha()  # load in graphics
        self.mask = pygame.mask.from_surface(self.deadzone)  # get mask of graphics

    def draw(self, screen):
        # method draws deadzone from the origin of x and y values
        screen.blit(self.deadzone, (self.x, self.y))

    def get_x(self):  # getter
        return int(self.x)

    def get_y(self):  # getter
        return int(self.y)


