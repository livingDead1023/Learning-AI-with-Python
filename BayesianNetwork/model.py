from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Define the network structure
model = BayesianNetwork([
    ('nodeA', 'nodeB'),
    ('nodeA', 'nodeC'),
    ('nodeB', 'nodeC'),
    ('nodeC', 'nodeD')
])

# Define the CPDs
cpd_nodeA = TabularCPD(variable='nodeA', variable_card=3, values=[[0.7], [0.2], [0.1]], state_names={'nodeA': ['a', 'b', 'c']})

cpd_nodeB = TabularCPD(variable='nodeB', variable_card=2, 
                       values=[[0.9, 0.8, 0.3], [0.1, 0.2, 0.7]], 
                       evidence=['nodeA'], evidence_card=[3], 
                       state_names={'nodeA': ['a', 'b', 'c'], 'nodeB': ['d', 'e']})

cpd_nodeC = TabularCPD(variable='nodeC', variable_card=2, 
                       values=[[0.8, 0.9, 0.6, 0.7, 0.4, 0.5], [0.2, 0.1, 0.4, 0.3, 0.6, 0.5]], 
                       evidence=['nodeA', 'nodeB'], evidence_card=[3, 2], 
                       state_names={'nodeA': ['a', 'b', 'c'], 'nodeB': ['d', 'e'], 'nodeC': ['f', 'g']})

cpd_nodeD = TabularCPD(variable='nodeD', variable_card=2, 
                       values=[[0.1, 0.4], [0.9, 0.6]], 
                       evidence=['nodeC'], evidence_card=[2], 
                       state_names={'nodeC': ['f', 'g'], 'nodeD': ['h', 'i']})

# Add CPDs to the model
model.add_cpds(cpd_nodeA, cpd_nodeB, cpd_nodeC, cpd_nodeD)

# Validate the model
model.check_model()

# Example usage
inference = VariableElimination(model)

# Get the distribution for each node
nodes = ['nodeA', 'nodeB', 'nodeC', 'nodeD']
for node in nodes:
    distribution = inference.query(variables=[node])
    print(f"Distribution for {node}:")
    print(distribution)

# Check the probability of a specific combination of states
# For example, the probability of nodeA being 'a', nodeB being 'd', nodeC being 'f', and nodeD being 'h'
evidence = {'nodeA': 'a', 'nodeB': 'd', 'nodeC': 'f'}
query_node = 'nodeD'
distribution = inference.query(variables=[query_node], evidence=evidence)
print(f"Distribution for {query_node} given {evidence}:")
print(distribution)

# Extract the probability of a specific state in nodeD
state = 'h'
state_index = distribution.state_names[query_node].index(state)
probability = distribution.values[state_index]
print(f"Probability of {query_node} being in state '{state}' given {evidence}: {probability}")
