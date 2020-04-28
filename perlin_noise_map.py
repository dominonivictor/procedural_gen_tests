import random
import arcade
from noise import pnoise1 as noise

import pyglet

import logging as log

log.basicConfig(level=log.DEBUG)



GRID_SIZE = 25
N_GRIDS_PER_ROW = 2
N_ROWS = 2
BASE_XOFF = 0

def update(dt):
	global BASE_XOFF
	BASE_XOFF += dt
    

pyglet.clock.schedule_interval(update, 1.0/30.0)


SQUARE_SIZE = 4
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

X_SPACING = (SCREEN_WIDTH - GRID_SIZE*SQUARE_SIZE*N_GRIDS_PER_ROW)//(N_GRIDS_PER_ROW + 1) 
Y_SPACING = (SCREEN_HEIGHT - GRID_SIZE*SQUARE_SIZE*N_ROWS)//(N_ROWS + 1)



def generate_noise(width, height):
    noise_map = []

    points = 256
    span = 5.0
    speed = 1.0

    botom_range = 0
    top_range = 0

    xoff = BASE_XOFF
    for _x in range(width):
        new_row = []
        xoff = float(_x) * span / points - 0.5 * span
        for _y in range(height):
            noise_value = noise(xoff + BASE_XOFF)
            new_row.append(noise_value)
            xoff += random.random()

            if noise_value < botom_range:
                botom_range = noise_value
            elif noise_value > top_range:
                top_range = noise_value
        noise_map.append(new_row)
    
    difference = float(top_range - botom_range)
    for x in range(width):
        for y in range(height):
            noise_map[x][y] = (noise_map[x][y] - botom_range)/difference

    return noise_map
    

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.grid = generate_noise(GRID_SIZE, GRID_SIZE)

        arcade.set_background_color(arcade.color.BLACK)

    # def on_draw(self):
    #     arcade.start_render()

    #     for x in [200, 600]:
    #         for y in [200, 600]:
    #             arcade.draw_rectangle_filled(x, y, 100, 100, arcade.color.GREEN)


        
    #     arcade.finish_render()

    def on_draw(self):
        arcade.start_render()
        done_rows = 0
        for _col in range(N_GRIDS_PER_ROW):
            done_grids_in_row = 0
            
            for _row in range(N_ROWS):

                for row in range(GRID_SIZE):
                    for col in range(GRID_SIZE):
                        if self.grid[row][col] < 0.333: color = arcade.color.BLUE
                        elif self.grid[row][col] < 0.666: color = arcade.color.GREEN 
                        else: color = arcade.color.SANDY_BROWN
                        # if done_rows: color = arcade.color.SANDY_BROWN
                        # else: color = arcade.color.GREEN

                        

                        x = X_SPACING + row * SQUARE_SIZE + (X_SPACING + GRID_SIZE*SQUARE_SIZE)*done_grids_in_row
                        y = (Y_SPACING + GRID_SIZE *SQUARE_SIZE)*(done_rows + 1) - col * SQUARE_SIZE 
                        
                        # if row == 0  and col == 0: log.debug(f"x,y: {x}, {y}, done_rows: {done_rows}, done_grids: {done_grids_in_row}")


                        arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, color)
                        self.grid = generate_noise(GRID_SIZE, GRID_SIZE)

                
                done_grids_in_row += 1

            done_rows += 1
        
        arcade.finish_render()


def main():
    Game(SCREEN_WIDTH, SCREEN_HEIGHT, "WAZZUUP?")
    arcade.run()

if __name__ == "__main__":
    main()