import csv
from sklearn.model_selection import train_test_split

import torch as t

import torch.nn as nn
import torch.optim as optim

# Read the train data from the file and divide it into X(evidence) and y(label)
with open('/Users/ritayanbanerjee/Desktop/SearchAlgorithms/NeuralNetwork/data.csv') as f:
    reader = csv.reader(f)
    next(reader)
    data_train = []
    for row in reader:
        data_train.append({"evidence": [float(cell) for cell in row[:4]], "label": 0 if row[4] == '0' else 1})
X_train = [row["evidence"] for row in data_train]
y_train = [row["label"] for row in data_train]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.4)

# Convert data to tensors
X_train = t.tensor(X_train, dtype=t.float32)
X_test = t.tensor(X_test, dtype=t.float32)
y_train = t.tensor(y_train, dtype=t.float32).view(-1, 1)
y_test = t.tensor(y_test, dtype=t.float32).view(-1, 1)

# Define the neural network class
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Example usage
if __name__ == "__main__":
    # Hyperparameters
    input_size = 4
    hidden_size = 5
    output_size = 1
    learning_rate = 0.001
    num_epochs = 10000000000

    # Create the model
    model = SimpleNN(input_size, hidden_size, output_size)

    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Dummy data
    X = t.randn(100, input_size)
    y = t.randn(100, output_size)

    # Train the model
    for epoch in range(num_epochs):
        # Forward pass
        outputs = model(X)
        loss = criterion(outputs, y)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch+1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
            print('Finished Training')
    model.eval()
    with t.no_grad():
        test_outputs = model(X_test)
        test_loss = criterion(test_outputs, y_test)
        accuracy = ((test_outputs.round() == y_test).sum().item() / y_test.size(0)) * 100
        print(f'Test Loss: {test_loss.item():.4f}, Accuracy: {accuracy:.2f}%')
        #print(f'Test Loss: {test_loss.item():.4f}, Accuracy: {accuracy:.2f}%')
