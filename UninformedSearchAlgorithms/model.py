import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.action = action 
        self.parent = parent

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("Maze must have exactly one start point 'A' and one goal point 'B'")
        
        self.contents = contents.splitlines()
        self.height = len(self.contents)
        self.width = max(len(line) for line in self.contents)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if self.contents[i][j] == "A":
                    self.start = (i, j)
                    row.append(False)
                elif self.contents[i][j] == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif self.contents[i][j] == "#":
                    row.append(True)
                else:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
        
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.contents):
            for j, col in enumerate(row):
                if col == "A":
                    print(col, end="")
                elif col == "B":
                    print(col, end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
        
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
        
    def solve(self):
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier() # Change to StackFrontier for DFS
        frontier.add(start)
        self.explored = set()
        while True:
            if frontier.empty():
                raise Exception("No solution")
            node = frontier.remove()
            self.num_explored += 1
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.explored.add(node.state)
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python model.py maze.txt")
        sys.exit(1)
    
    maze = Maze(sys.argv[1])
    print("Maze:")
    maze.print()
    print("Solving...")
    maze.solve()
    print("States Explored:", maze.num_explored)
    print("Solution:")
    maze.print()
