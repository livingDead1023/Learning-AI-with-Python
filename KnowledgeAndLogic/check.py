from logic import*
# Define symbols
A = Symbol("A")
B = Symbol("B")

# Define knowledge base
knowledge = And(A, Not(B))

# Define query
query = A

# Check if knowledge base entails query
result = model_check(knowledge, query)
print(result)  # Output: True or False