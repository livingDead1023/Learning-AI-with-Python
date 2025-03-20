<p class ='i'>

import random as rd
from map import generate_map, save_map_to_file, draw_map
import sys
import os
import numpy as np  # Import NumPy

class HillClimbingProject():
    def __init__(self, map_grid, height, width, num_houses, num_hospitals):
        # Initialize the HillClimbingProject with the map grid and its properties
        self.map_grid = map_grid  # The 2D grid representing the map
        self.height = height  # The height of the map
        self.width = width  # The width of the map
        self.num_houses = num_houses  # The number of houses on the map
        self.num_hospitals = num_hospitals  # The number of hospitals on the map
        self.houses = set()  # A set to store the coordinates of houses
        self.hospitals = set()  # A set to store the coordinates of hospitals

        # Initialize houses and hospitals sets by iterating through the map
        for y in range(height):
            for x in range(width):
                if map_grid[y][x] == 'H':
                    self.houses.add((y, x))  # Add house coordinates to the houses set
                elif map_grid[y][x] == '+':
                    self.hospitals.add((y, x))  # Add hospital coordinates to the hospitals set


    def available_spaces(self):
        # Determine available spaces where a hospital can be placed
        candidates = set()  # Initialize a set to store candidate coordinates
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if self.map_grid[y][x] == ' ' or self.map_grid[y][x] == '+':
                    candidates.add((y, x))  # Add empty or hospital-occupied coordinates to candidates

        # Remove houses from available spaces to prevent hospital placement on house locations
        for house in self.houses:
            if house in candidates:
                candidates.remove(house)  # Remove house coordinates from the candidates set
        return candidates  # Return the set of available spaces
    

    def get_cost(self):
        # Calculate the total cost based on Manhattan distances from houses to nearest hospitals
        houses_array = np.array(list(self.houses))  # Convert houses set to NumPy array
        hospitals_array = np.array(list(self.hospitals))  # Convert hospitals set to NumPy array
        
        if len(self.houses) == 0 or len(self.hospitals) == 0:
            return 0  # Handle edge case where there are no houses or hospitals
        
        # Calculate Manhattan distances using NumPy
        distances = np.abs(houses_array[:, np.newaxis, :] - hospitals_array[np.newaxis, :, :])
        min_distances = np.sum(distances, axis=2).min(axis=1)
        total_cost = np.sum(min_distances)
        
        return total_cost  # Return the total cost
    
    def get_neighbours(self, y, x):
        # Get neighboring coordinates for a given cell
        neighbours = []  # Initialize a list to store neighboring coordinates
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Define possible movements (up, down, left, right)
            new_y, new_x = y + dy, x + dx  # Calculate new coordinates
            if 0 < new_y < self.height and 0 < new_x < self.width and (new_y, new_x) in self.available_spaces():
                neighbours.append((new_y, new_x))  # Add valid neighboring coordinates to the list
        return neighbours  # Return the list of neighboring coordinates

    def steepest_ascent(self, maximum = None, image_prefix = None, log = False ):
        # Implement the steepest ascent hill climbing algorithm
        
        count = 0  # Initialize iteration counter
        initial_cost = self.get_cost()  # Calculate initial cost
        if log:
            print(f"Initial state: {initial_cost}")  # Print initial cost if logging is enabled
        
        # Loop until maximum iterations are reached or no improvement is found
        while maximum is None or count < maximum:
            count += 1  # Increment iteration counter
            best_neighbours = []  # Initialize list to store best neighbors
            best_neighbours_cost = float('inf')  # Initialize best neighbor cost to infinity

            # Iterate through each hospital
            for hospital_y, hospital_x in list(self.hospitals):  # Iterate over a copy
                # Iterate through each possible replacement location
                for replacement_y, replacement_x in self.get_neighbours(hospital_y, hospital_x):
                    # Create a potential new state
                    temp_hospitals = self.hospitals.copy()  # Copy the current hospitals set
                    temp_hospitals.remove((hospital_y, hospital_x))  # Remove the current hospital
                    temp_hospitals.add((replacement_y, replacement_x))  # Add the replacement location

                    # Calculate the cost of the new state
                    # Temporarily update the map grid
                    original_hospital_value = self.map_grid[hospital_y][hospital_x]  # Store original value
                    original_replacement_value = self.map_grid[replacement_y][replacement_x]  # Store original value

                    self.map_grid[hospital_y][hospital_x] = ' '  # Set current hospital location to empty
                    self.map_grid[replacement_y][replacement_x] = '+'  # Set replacement location to hospital
                    
                    # Update hospitals set
                    original_hospitals = self.hospitals.copy()
                    self.hospitals.remove((hospital_y, hospital_x))
                    self.hospitals.add((replacement_y, replacement_x))
                    
                    neighbour_cost = self.get_cost()  # Calculate the cost of the new state

                    # Revert the map grid and hospitals set
                    self.map_grid[hospital_y][hospital_x] = original_hospital_value  # Restore original value
                    self.map_grid[replacement_y][replacement_x] = original_replacement_value  # Restore original value
                    self.hospitals = original_hospitals

                    # Update best neighbor if needed
                    if neighbour_cost < best_neighbours_cost:  # If the new cost is better
                        best_neighbours = [(temp_hospitals, (hospital_y, hospital_x), (replacement_y, replacement_x))]  # Store the new neighbor
                        best_neighbours_cost = neighbour_cost  # Update the best cost
                    elif neighbour_cost == best_neighbours_cost:  # If the new cost is equal to the best cost
                        best_neighbours.append((temp_hospitals, (hospital_y, hospital_x), (replacement_y, replacement_x)))  # Add the new neighbor

            # Check if we improved
            if best_neighbours_cost >= self.get_cost():  # If no improvement was found
                print("No improvement found. Returning current state.")
                break  # Exit the loop
            else:
                # Update hospitals with the best neighbor
                best_neighbour, old_hospital, new_hospital = rd.choice(best_neighbours)  # Choose a random best neighbor
                print(f"Found Better Neighbour: Cost: {best_neighbours_cost}")  # Print the new cost
                
                # Update the map grid
                self.map_grid[old_hospital[0]][old_hospital[1]] = ' '  # Set the old hospital location to empty
                self.map_grid[new_hospital[0]][new_hospital[1]] = '+'  # Set the new hospital location to hospital

                self.hospitals = best_neighbour  # Update the hospitals set
                
                if log:
                    print(f"Found Better Neighbour: Cost: {best_neighbours_cost}")  # Print the new cost if logging is enabled

                if image_prefix:
                    draw_map(self.map_grid, f"{image_prefix}_{count}.png")  # Draw the map if image prefix is provided
        
        final_cost = self.get_cost()  # Calculate the final cost
        print(f"Final Cost: {final_cost}")  # Print the final cost
        print("Maximum iterations reached. Returning current state.")
        return self.hospitals  # Return the final hospitals set

def load_map_from_file(filename):
    # Load the map from a text file
    with open(filename, 'r') as f:  # Open the file for reading
        map_grid = [list(line.strip()) for line in f]  # Read each line and convert it to a list of characters
    height = len(map_grid)  # Determine the height of the map
    width = len(map_grid[0]) if height > 0 else 0  # Determine the width of the map
    num_houses = sum(row.count('H') for row in map_grid)  # Count the number of houses
    num_hospitals = sum(row.count('+') for row in map_grid)  # Count the number of hospitals
    return map_grid, height, width, num_houses, num_hospitals  # Return the map grid and its properties

if __name__ == '__main__':
    # Main execution block
    # Define directory paths
    text_dir = "text_output"  # Directory for text output
    image_dir = "image_output"  # Directory for image output

    # Create directories if they don't exist
    os.makedirs(text_dir, exist_ok=True)  # Create the text output directory if it doesn't exist
    os.makedirs(image_dir, exist_ok=True)  # Create the image output directory if it doesn't exist

    # Load map from file
    if len(sys.argv) > 1:
        filename = sys.argv[1]  # Get the filename from the command line argument
    else:
        filename = "map.txt"  # Default filename

    try:
        map_grid, height, width, num_houses, num_hospitals = load_map_from_file(filename)  # Load the map from the file
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")  # Print an error message if the file is not found
        sys.exit(1)  # Exit the program
    except Exception as e:
        print(f"Error loading map from file: {e}")  # Print an error message if there is an error loading the map
        sys.exit(1)  # Exit the program

    # Create and run the hill climbing project
    project = HillClimbingProject(map_grid, height, width, num_houses, num_hospitals)  # Create an instance of the HillClimbingProject
    project.steepest_ascent(image_prefix=os.path.join(image_dir, "hill_climbing"), log=True, maximum=10000000000)  # Run the steepest ascent algorithm
    print("Done!")  # Print a completion message

    # Save output to separate directories
    save_map_to_file(project.map_grid, os.path.join(text_dir, "optimized_map.txt"))  # Save the optimized map to a text file
    draw_map(project.map_grid, os.path.join(image_dir, "optimized_map.png"))  # Save the optimized map as an image
    
</p>