from torpedo import *
from asteroid import *
from spaceship import *
from gameMaster import *
import math


class GameRunner:

    def __init__(self, amnt = 3):
        self.game = GameMaster()
        self.screenMaxX = self.game.get_screen_max_x()
        self.screenMaxY = self.game.get_screen_max_y()
        self.screenMinX = self.game.get_screen_min_x()
        self.screenMinY = self.game.get_screen_min_y()
        shipStartX = (self.screenMaxX-self.screenMinX)/2 + self.screenMinX
        shipStartY = (self.screenMaxY-self.screenMinY)/2 + self.screenMinY
        self.game.set_initial_ship_cords( shipStartX, shipStartY )
        self.game.add_initial_astroids(amnt)

    def run(self):
        self._do_loop()
        self.game.start_game()

    def _do_loop(self):
        self.game.update_screen()
        self.game_loop()
        # Set the timer to go off again
        self.game.ontimer(self._do_loop,5)

    def move_object(self,object):
        """
        function that receives an object(ship,asteroid,torpedo)
        and moves it on the screen
        """
        x = object.get_x_cor()
        y = object.get_y_cor()
        x_s = object.get_speed_x()
        y_s = object.get_speed_y()
        min_x = self.game.get_screen_min_x()
        max_x = self.game.get_screen_max_x()
        min_y = self.game.get_screen_min_y()
        max_y = self.game.get_screen_max_y()
        delta_x = max_x - min_x
        delta_y = max_y - min_y
        x = (x_s + x - min_x) % delta_x + min_x
        y = (y_s + y - min_y) % delta_y + min_y
        object.move(x,y)

    def move_asteroids(self):
        """
        function that's in charge of moving all of the current asteroids
        """
        list = self.game.get_asteroids()
        for i in range(len(list)):
            x = list[i].get_x_cor()
            y = list[i].get_y_cor()
            self.move_object(list[i])

    def move_ship(self):
        """
        function that's in charge of the acceleration of the ship when the
        key up is pressed on the keyboard
        and turning it left\ right when the key left or right is pressed
        also the function moves the ship across the screen
        """
        ship = self.game.get_ship()
        angle = ship.get_angle()
        speed_x = ship.get_speed_x()
        speed_y = ship.get_speed_y()
        if(self.game.is_up_pressed()):
            new_speed_x = speed_x + math.cos(angle * math.pi / 180)
            new_speed_y = speed_y + math.sin(angle * math.pi / 180)
            ship.set_speed_x(new_speed_x)
            ship.set_speed_y(new_speed_y)
        elif(self.game.is_right_pressed()):
            ship.increase_angle()
        elif(self.game.is_left_pressed()):
            ship.decrease_angle()
        self.move_object(ship)

    def ship_slow_down(self):
        """
        function that insures that the speed of the ship will by decrease 0.1%
        each iteration on the game loop
        """
        ship = self.game.get_ship()
        speed_x = ship.get_speed_x()
        speed_y = ship.get_speed_y()
        if (speed_x != 0):
            # if  the speed is zero in the x axis there is no point trying to
            #decrease its speed
            ship.set_speed_x(speed_x*0.999)
        if (speed_y !=0):
            # if  the speed is zero in the y axis there is no point trying to
            #decrease its speed
            ship.set_speed_y(speed_y*0.999)

    def torpedo_fire(self):
        """
        function that creates a torpedo on the screen each time the key
        space is pressed, and moves it across the screen
        """
        ship = self.game.get_ship()
        x = ship.get_x_cor()
        y = ship.get_y_cor()
        x_s = ship.get_speed_x()
        y_s = ship.get_speed_y()
        angle = ship.get_angle()
        torpedo_speed_x = x_s + math.cos(angle * math.pi / 180)
        torpedo_speed_y = y_s + math.sin(angle * math.pi / 180)
        torpedo_list = self.game.get_torpedos()
        if(self.game.is_fire_pressed() and (len(torpedo_list) < 20)):
            # the max amount of the torpedoes at any given time is 20
            self.game.add_torpedo(x,y,torpedo_speed_x,torpedo_speed_y,angle)
        for i in torpedo_list:
            # moving each torpedo that's in the list of the torpedoes
            self.move_object(i)

    def check_torpedo(self):
        """
        function that removes torpedoes from the screen that have
        # outlived their life span
        """
        dead_torpedo = []
        # the built in function that removes torpedoes gets a list of
        # torpedoes
        torpedo_list = self.game.get_torpedos()
        for i in torpedo_list:
            life = i.get_life_span()
            if (life <= 0):
                dead_torpedo.append(i)
        self.game.remove_torpedos(dead_torpedo)

    def collision(self,torpedo,asteroid):
        """
        function that receives an asteroid and a torpedo that collided
        removes the torpedo from the game, and splits the asteroid into
        two smaller one if possible if not removes it.
        also the function add score for each asteroid that was destroyed
        based on its size
        """
        dead_torpedo = []
        dead_torpedo.append(torpedo)
        asteroid_x = asteroid.get_x_cor()
        asteroid_y = asteroid.get_y_cor()
        torpedo_speed_x = torpedo.get_speed_x()
        torpedo_speed_y = torpedo.get_speed_y()
        asteroid_speed_x = asteroid.get_speed_x()
        asteroid_speed_y = asteroid.get_speed_y()
        asteroid_speed_xy = math.pow(asteroid_speed_x,2) + math.pow\
            (asteroid_speed_y,2)
        asteroid_size = asteroid.get_size()
        low_points = 20
        med_points = 50
        hi_points = 100
        self.game.remove_asteroid(asteroid)
        self.game.remove_torpedos(dead_torpedo)
        if (asteroid_size > 1):
            # the only way that a given asteroid will split will be when it's
            # size is bigger  than 1
            new_speed_x = (torpedo_speed_x + asteroid_speed_x)\
                          /math.sqrt((asteroid_speed_xy))
            new_speed_y = (torpedo_speed_y + asteroid_speed_y)\
                          /math.sqrt((asteroid_speed_xy))
            self.game.add_asteroid(asteroid_x,asteroid_y,new_speed_x,
                                   new_speed_y,asteroid_size - 1)
            self.game.add_asteroid(asteroid_x,asteroid_y,-new_speed_x,
                                   -new_speed_y,asteroid_size - 1)
            # the speed of both asteroids is the same the only difference is
            # their direction
        if (asteroid_size == 1):
            self.game.add_to_score(hi_points)
        if (asteroid_size == 2):
            self.game.add_to_score(med_points)
        if (asteroid_size == 3):
            self.game.add_to_score(low_points)

    def check_for_collision(self):
        """
        function that runs in all of the indexes of the torpedoes list
        and asteroids list and sends each possible combo of torpedo
        and an asteroid to a function if there was a collision between
        the given two objects
        """
        torpedo_list = self.game.get_torpedos()
        asteroid_list = self.game.get_asteroids()
        for asteroid in asteroid_list:
            for torpedo in torpedo_list:
                if (self.game.intersect(torpedo,asteroid)):
                    self.collision(torpedo,asteroid)

    def ship_destruction(self):
        """
        function that determines whether the ship collided with an asteroid
        if it did then the player will lose one life, and the asteroid will
        be destroyed, and the player will receive a message, also if the
        player has only one life left, the next collision with an asteroid
        will result in a message to the player saying that he has lost
         and the game will end
        """
        ship = self.game.get_ship()
        life = self.game.get_num_lives()
        asteroid_list = self.game.get_asteroids()
        for asteroid in asteroid_list:
            if(self.game.intersect(ship,asteroid)):
                life -= 1
                self.game.ship_down()
                self.game.remove_asteroid(asteroid)
                if (life < 1):
                    self.game.show_message("Loser!!!","You are out of lives")
                    self.game.end_game()
                else:
                    self.game.show_message("Collision","You've lost one life,"
                                                   " be careful next time")

    def is_win(self):
        """
        function that determines whether the winning criteria has been met
        which is the destruction of all of the asteroids and, the amount
        of remaining lives is greater than 0
        """
        asteroid_list = self.game.get_asteroids()
        life = self.game.get_num_lives()
        if (not len(asteroid_list) and (life > 0)):
            self.game.show_message("Win!","Congratulations you've won")
            self.game.end_game()

    def game_loop(self):
        #This is where your code goes!
        self.move_asteroids()
        self.move_ship()
        self.ship_slow_down()
        self.torpedo_fire()
        self.check_torpedo()
        self.check_for_collision()
        self.ship_destruction()
        self.is_win()
        if self.game.should_end():
            # if the player pressed "q" the game will end and the player
            # receive a message
            self.game.show_message("Exit","Come back soon")
            self.game.end_game()


def main():
    runner = GameRunner()
    runner.run()

if __name__ == "__main__":
    main()
