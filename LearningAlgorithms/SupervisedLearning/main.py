import csv
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import log_loss

# Define models to try
models = {
    "Perceptron": Perceptron(),
    "GaussianNB": GaussianNB(),
    "SVC": make_pipeline(StandardScaler(), SVC(probability=True)),
    "KNN": make_pipeline(StandardScaler(), knn(n_neighbors=300))
}

# Read the train data from the file and divide it into X(evidence) and y(label)
with open('/SearchAlgorithms/LearningAlgorithms/SupervisedLearning/train.csv') as f:
    reader = csv.reader(f)
    next(reader)
    data_train = []
    for row in reader:
        data_train.append({"evidence": [float(cell) for cell in row[:4]], "label": 0 if row[4] == '0' else 1})
X_train = [row["evidence"] for row in data_train]
y_train = [row["label"] for row in data_train]

# Read the test data from the file and divide it into X(evidence) and y(label)
with open('/SearchAlgorithms/LearningAlgorithms/SupervisedLearning/test.csv') as f:
    reader = csv.reader(f)
    next(reader)
    data_test = []
    for row in reader:
        if len(row) >= 5:
            data_test.append({"evidence": [float(cell) for cell in row[:4]], "label": 0 if row[4] == '0' else 1})
X_test = [row["evidence"] for row in data_test]
y_test = [row["label"] for row in data_test]

# Evaluate each model
results = {}
for model_name, model in models.items():
    print(f"Evaluating {model_name}...")
    model.fit(X_train, y_train)
    try:
        predictions = model.predict(X_test)
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X_test)
        else:
            probabilities = [[1-p, p] for p in predictions]
    except ValueError as e:
        print(f"Error during prediction with {model_name}: {e}")
        predictions = []
        probabilities = []
        if not predictions:
            print("No predictions were made.")
            predictions = [0] * len(y_test)
            probabilities = [[1, 0]] * len(y_test)
    
    total = 0
    correct = 0
    incorrect = 0
    for actual, predicted in zip(y_test, predictions):
        total += 1
        if actual == predicted:
            correct += 1
        else:
            incorrect += 1

    accuracy = 100 * correct / total if total > 0 else 0
    if len(probabilities) > 0 and len(probabilities) == len(y_test):
        loss = log_loss(y_test, probabilities)
    else:
        loss = float('inf')
    
    results[model_name] = {"accuracy": accuracy, "loss": loss}
    print(f"Total: {total}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Results: {correct}/{total} correct")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Loss: {loss:.4f}")

# Plot the results
model_names = list(results.keys())
accuracies = [results[model]["accuracy"] for model in model_names]
losses = [results[model]["loss"] for model in model_names]

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Model')
ax1.set_ylabel('Accuracy (%)', color=color)
ax1.bar(model_names, accuracies, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Loss', color=color)
ax2.plot(model_names, losses, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Model Performance')
plt.show()
