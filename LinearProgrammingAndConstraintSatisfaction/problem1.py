import scipy as sp

# PROBLEM:
# Cost Function: 50x + 80y
# Constraints:
# C1: 5x + 2y <= 20
# C2: 10x + 12y >= 90 <=> -10x - 12y <= -90

result = sp.optimize.linprog(
    c=[50, 80],
    A_ub=[[5, 2], [-10, -12]],
    b_ub=[20,-90],
)

if result.success:
    print("X:", result.x[0])
    print("Y:", result.x[1])
else:
    print("No solution found")