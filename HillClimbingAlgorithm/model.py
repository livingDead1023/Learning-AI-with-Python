import random as rd
from map import generate_map, save_map_to_file, draw_map
import sys
import os

class HillClimbingProject():
    def __init__(self, map_grid, height, width, num_houses, num_hospitals):
        self.map_grid = map_grid
        self.height = height
        self.width = width
        self.num_houses = num_houses
        self.num_hospitals = num_hospitals
        self.houses = set()
        self.hospitals = set()

        # Initialize houses and hospitals sets
        for y in range(height):
            for x in range(width):
                if map_grid[y][x] == 'H':
                    self.houses.add((y, x))
                elif map_grid[y][x] == '+':
                    self.hospitals.add((y, x))


    def available_spaces(self):
        candidates = set()
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if self.map_grid[y][x] == ' ' or self.map_grid[y][x] == '+':
                    candidates.add((y, x))

        # Remove houses from available spaces
        for house in self.houses:
            if house in candidates:
                candidates.remove(house)
        return candidates
    

    def get_cost(self):
        total_cost = 0
        for house_y, house_x in self.houses:
            min_distance = float('inf')
            for hospital_y, hospital_x in self.hospitals:
                distance = abs(house_y - hospital_y) + abs(house_x - hospital_x)
                min_distance = min(min_distance, distance)
            total_cost += min_distance
        return total_cost
    
    def get_neighbours(self, y, x):
        neighbours = []
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_y, new_x = y + dy, x + dx
            if 0 < new_y < self.height and 0 < new_x < self.width and (new_y, new_x) in self.available_spaces():
                neighbours.append((new_y, new_x))
        return neighbours

    def steepest_ascent(self, maximum = None, image_prefix = None, log = False ):
        
        count = 0
        initial_cost = self.get_cost()
        if log:
            print(f"Initial state: {initial_cost}")
        
        while maximum is None or count < maximum:
            count += 1
            best_neighbours = []
            best_neighbours_cost = float('inf')  # Initialize with infinity

            for hospital_y, hospital_x in list(self.hospitals):  # Iterate over a copy
                for replacement_y, replacement_x in self.get_neighbours(hospital_y, hospital_x):
                    # Create a potential new state
                    temp_hospitals = self.hospitals.copy()
                    temp_hospitals.remove((hospital_y, hospital_x))
                    temp_hospitals.add((replacement_y, replacement_x))

                    # Calculate the cost of the new state
                    # Temporarily update the map grid
                    original_hospital_value = self.map_grid[hospital_y][hospital_x]
                    original_replacement_value = self.map_grid[replacement_y][replacement_x]

                    self.map_grid[hospital_y][hospital_x] = ' '
                    self.map_grid[replacement_y][replacement_x] = '+'
                    
                    # Update hospitals set
                    original_hospitals = self.hospitals.copy()
                    self.hospitals.remove((hospital_y, hospital_x))
                    self.hospitals.add((replacement_y, replacement_x))
                    
                    neighbour_cost = self.get_cost()

                    # Revert the map grid and hospitals set
                    self.map_grid[hospital_y][hospital_x] = original_hospital_value
                    self.map_grid[replacement_y][replacement_x] = original_replacement_value
                    self.hospitals = original_hospitals

                    # Update best neighbor if needed
                    if neighbour_cost < best_neighbours_cost:
                        best_neighbours = [(temp_hospitals, (hospital_y, hospital_x), (replacement_y, replacement_x))]
                        best_neighbours_cost = neighbour_cost
                    elif neighbour_cost == best_neighbours_cost:
                        best_neighbours.append((temp_hospitals, (hospital_y, hospital_x), (replacement_y, replacement_x)))

            # Check if we improved
            if best_neighbours_cost >= self.get_cost():
                print("No improvement found. Returning current state.")
                break
            else:
                # Update hospitals with the best neighbor
                best_neighbour, old_hospital, new_hospital = rd.choice(best_neighbours)
                print(f"Found Better Neighbour: Cost: {best_neighbours_cost}")
                
                # Update the map grid
                self.map_grid[old_hospital[0]][old_hospital[1]] = ' '
                self.map_grid[new_hospital[0]][new_hospital[1]] = '+'

                self.hospitals = best_neighbour
                
                if log:
                    print(f"Found Better Neighbour: Cost: {best_neighbours_cost}")

                if image_prefix:
                    draw_map(self.map_grid, f"{image_prefix}_{count}.png")
        
        final_cost = self.get_cost()
        print(f"Final Cost: {final_cost}")
        print("Maximum iterations reached. Returning current state.")
        return self.hospitals

def load_map_from_file(filename):
    with open(filename, 'r') as f:
        map_grid = [list(line.strip()) for line in f]
    height = len(map_grid)
    width = len(map_grid[0]) if height > 0 else 0
    num_houses = sum(row.count('H') for row in map_grid)
    num_hospitals = sum(row.count('+') for row in map_grid)
    return map_grid, height, width, num_houses, num_hospitals

if __name__ == '__main__':
    # Define directory paths
    text_dir = "text_output"
    image_dir = "image_output"

    # Create directories if they don't exist
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

    # Load map from file
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "map.txt"  # Default filename

    try:
        map_grid, height, width, num_houses, num_hospitals = load_map_from_file(filename)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading map from file: {e}")
        sys.exit(1)

    # Create and run the hill climbing project
    project = HillClimbingProject(map_grid, height, width, num_houses, num_hospitals)
    project.steepest_ascent(image_prefix=os.path.join(image_dir, "hill_climbing"), log=True, maximum=10000000000)
    print("Done!")

    # Save output to separate directories
    save_map_to_file(project.map_grid, os.path.join(text_dir, "optimized_map.txt"))
    draw_map(project.map_grid, os.path.join(image_dir, "optimized_map.png"))