




    def evaluate_trajectories(self, trajectories: list[Trajectory]):
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        for trajectory in trajectories:
            r, c = self.evaluate_trajectory(trajectory)
            returns += r
            counts += c
        return returns, counts
