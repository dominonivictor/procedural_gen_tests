import random
import arcade

GRID_SIZE = 70
SQUARE_SIZE = 4
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

X_SPACING = (SCREEN_WIDTH - GRID_SIZE)//2 
Y_SPACING = (SCREEN_HEIGHT - GRID_SIZE)//2

def generate_noise(width, height):
    noise_map = []
    # Populate a noise map with 0s
    for _y in range(height):
        new_row = []
        for _x in range(width):
            new_row.append(0)
        noise_map.append(new_row)

    # Progressively apply variation to the noise map but changing values + or -
    # 5 from the previous entry in the same list, or the average of the
    # previous entry and the entry directly above
    new_value = 0
    top_of_range = 0
    bottom_of_range = 0
    for y in range(height):
        for x in range(width):
            if x == 0 and y == 0:
                continue
            if y == 0:  # If the current position is in the first row
                new_value = noise_map[y][x - 1] + random.randint(-1000, +1000)
            elif x == 0:  # If the current position is in the first column
                new_value = noise_map[y - 1][x] + random.randint(-1000, +1000)
            else:
                minimum = min(noise_map[y - 1][x], noise_map[y][x - 1])
                maximum = max(noise_map[y - 1][x], noise_map[y][x - 1])
                average_value = minimum + ((maximum-minimum)/2.0)
                new_value = average_value + random.randint(-1000, +1000)
            noise_map[y][x] = new_value
            # check whether value of current position is new top or bottom
            # of range
            if new_value < bottom_of_range:
                bottom_of_range = new_value
            elif new_value > top_of_range:
                top_of_range = new_value
    # Normalises the range, making minimum = 0 and maximum = 1
    difference = float(top_of_range - bottom_of_range)
    for y in range(height):
        for x in range(width):
            noise_map[y][x] = (noise_map[y][x] - bottom_of_range)/difference
    
    return noise_map

def get_neighbours(x, y):
    i = -1
    j = -1
    i_end = 2
    j_end = 2
    if x == 0:
        i = 0
    elif y == 0:
        j = 0
    elif x == width - 1:
        i_end = 1
    elif y == height - 1:
        j_end = 1

    pass
    

def cellular_automata(grid):


# gmap = generate_noise(GRID_SIZE, GRID_SIZE)
# res = "00"
# for x in range(GRID_SIZE):
#     for y in range(GRID_SIZE):          
#         if gmap[x][y] < 0.3: res = "00"
#         elif gmap[x][y] < 0.7: res = "77"
#         else: res = "99"
#         print(res, end=" ")

#     print("")

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.grid = generate_noise(GRID_SIZE, GRID_SIZE)

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] < 0.333: color = arcade.color.BLUE
                elif self.grid[row][col] < 0.666: color = arcade.color.GREEN 
                else: color = arcade.color.SANDY_BROWN

                x = X_SPACING + row * SQUARE_SIZE
                y = Y_SPACING + col * SQUARE_SIZE

                arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, color)

        arcade.finish_render()
        self.grid = generate_noise(GRID_SIZE, GRID_SIZE)

def main():
    Game(SCREEN_WIDTH, SCREEN_HEIGHT, "WAZZUUP?")
    arcade.run()

if __name__ == "__main__":
    main()