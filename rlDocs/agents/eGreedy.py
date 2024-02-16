import numpy as np

class EpsilonGreedy:
    """Epsilon Greedy Exploration Strategy."""

    def __init__(self, initial_epsilon=1.0, min_epsilon=0.0, decay=0.99):
        """
        Initialize Epsilon Greedy Exploration Strategy.

        Parameters:
            initial_epsilon (float): The initial value of epsilon (default is 1.0).
            min_epsilon (float): The minimum value of epsilon (default is 0.0).
            decay (float): The decay rate for epsilon (default is 0.99).
        """
        self.initial_epsilon = initial_epsilon
        self.epsilon = initial_epsilon
        self.min_epsilon = min_epsilon
        self.decay = decay

    def choose(self, q_table, state, action_space):
        """
        Choose action based on epsilon greedy strategy.

        Parameters:
            q_table (dict): The Q-table containing state-action values.
            state (object): The current state of the agent.
            action_space (object): The space of possible actions.

        Returns:
            int: The chosen action.
        """
        if np.random.rand() < self.epsilon:
            action = int(action_space.sample())
        else:
            action = np.argmax(q_table[state])

        self.epsilon = max(self.epsilon * self.decay, self.min_epsilon)
        return action

    def reset(self):
        """Reset epsilon to initial value."""
        self.epsilon = self.initial_epsilon
