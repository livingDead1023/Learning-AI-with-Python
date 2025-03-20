# Description: A simple implementation of a numeric Markov model in Python.
import random

class NumericMarkovModel:
        def __init__(self):
            self.model = {}

        def train(self, data):
            for i in range(len(data) - 1):
                if data[i] not in self.model:
                    self.model[data[i]] = []
                self.model[data[i]].append(data[i + 1])

        def generate(self, start_state, length):
            if start_state not in self.model:
                return []
            result = [start_state]
            current_state = start_state
            for _ in range(length - 1):
                next_states = self.model.get(current_state, [])
                if not next_states:
                    break
                next_state = random.choice(next_states)
                result.append(next_state)
                current_state = next_state
            return result

    # Example usage
if __name__ == "__main__":
        data = [1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 4, 5]
        numeric_model = NumericMarkovModel()
        numeric_model.train(data)
        generated_sequence = numeric_model.generate(1, 10)
        print("Generated sequence:", generated_sequence)