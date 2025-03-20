import random

import matplotlib.pyplot as plt

def generate_map(width, height, num_houses):
    # Create an empty map
    map_grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Place the boundary
    for i in range(width):
        map_grid[0][i] = map_grid[height-1][i] = '#'
    for i in range(height):
        map_grid[i][0] = map_grid[i][width-1] = '#'

    # Randomly place houses
    for _ in range(num_houses):
        while True:
            x = random.randint(1, width-2)
            y = random.randint(1, height-2)
            if map_grid[y][x] == ' ':
                map_grid[y][x] = 'H'
                break

    # Calculate the number of hospitals required based on the size of the map
    num_hospitals = (width * height) // 1000  # Example formula: 1 hospital per 50 units of area

    # Randomly place hospitals
    for _ in range(num_hospitals):
        while True:
            x = random.randint(1, width-2)
            y = random.randint(1, height-2)
            if map_grid[y][x] == ' ':
                map_grid[y][x] = '+'
                break
    while True:
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if map_grid[y][x] == ' ':
            map_grid[y][x] = '+'
            break

    return map_grid

def save_map_to_file(map_grid, filename):
    with open(filename, 'w') as f:
        for row in map_grid:
            f.write(''.join(row) + '\n')

def draw_map(map_grid, image_filename):
    fig, ax = plt.subplots()
    ax.set_xticks(range(len(map_grid[0])))
    ax.set_yticks(range(len(map_grid)))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)

    for y, row in enumerate(map_grid):
        for x, cell in enumerate(row):
            if cell == '#':
                ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='black'))
            elif cell == 'H':
                ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='blue'))
            elif cell == '+':
                ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='red'))

    plt.gca().invert_yaxis()
    plt.savefig(image_filename)

if __name__ == "__main__":
    width = 60
    height = 80
    num_houses = 15

    map_grid = generate_map(width, height, num_houses)
    save_map_to_file(map_grid, 'maps/map.txt')
    draw_map(map_grid, 'maps/map.png')