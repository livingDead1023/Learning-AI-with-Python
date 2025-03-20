# PROBLEM:
'''
    A
   / \
  B --C
/ |   |
D |   F
\ | /   \
  E --- G

Each node has Domain {a,b,c}; solve the CSP such that all nodes connected by an edge have different values.
Ensure that the solution is optimal, and that all nodes are node consistent and arc consistent.
'''

# SOLUTION 1:
def S1():
    # Define Constants
    VARIABLES = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] # Nodes
    CONSTRAINTS = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'F'), ('C', 'F'), ('D', 'E'), ('E', 'G'), ('F', 'G')] # Edges
    DOMAINS = ['a', 'b', 'c']  # Possible values for each node

    # Backtracking Search Function
    def backtrack(assignment):
        '''Backtracking algorithm to solve CSP, takes in assignment and returns a solution(if any)'''

        # Check if all variables have been assigned
        if len(assignment) == len(VARIABLES): return assignment

        # Else, select an unassigned variable
        var = select(assignment)

        # Loop for each value in the constant
        for value in DOMAINS:
            if consistent(assignment):

                # Copy and add new value to the assignment 
                new_assignment = assignment.copy()
                new_assignment[var] = value

                # Keep calling the function, until...
                result = backtrack(new_assignment)
                if result: return result # we reach result, return result
        return None # Else, return no solution

    # Selecting Unassigned Variable
    def select(assignment):
        '''Selects an Unassigned Variable, takes in assignment and returns var'''
        for var in VARIABLES:
            if var not in assignment:
                return var
        return None

    # Consistency Checking Function
    def consistent(assignment):
        '''Checks to see if assignment is consistent, takes in assignment and returns bool(True or False)'''

        # Iterates for every constraint in constant
        for (x,y) in CONSTRAINTS:

            # Checks arcs where both values are assigned
            if x not in assignment or y not in assignment: break

            # If both values are the same, not consistent
            if assignment[x] == assignment[y]: return False

        return True # All values are consistent

    # Evaluate solution
    solution = backtrack(dict())
    print(solution)

#SOLUTION 2:
from constraint import *

def S2():
    # Define the Problem
    problem = Problem()
    problem.addVariables(["A","B","C","D","E","F","G"],
                         ['a','b','c'])
    CONSTRAINTS = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'F'), ('C', 'F'), ('D', 'E'), ('E', 'G'), ('F', 'G')] # Edges
    for (x,y) in CONSTRAINTS: problem.addConstraint(lambda x,y: x!=y, [x,y])

    for solution in problem.getSolutions(): print(solution)

# Choose implementation
a = int(input("Check Solution No.[in int]: "))
S1() if a == 1 else S2()