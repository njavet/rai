


    @staticmethod
    def random_argmax(arr: np.ndarray) -> int:
        arr_max = np.max(arr)
        arr_maxes = np.where(arr == arr_max)[0]
        action = int(np.random.choice(arr_maxes))
        return action

    def generate_trajectory(self, action_selector: Callable) -> list[GymTrajectory]:
        trajectory = []
        state, info = self.env.reset()
        done = False
        while not done:
            action = action_selector(state)
            next_state, ts, done = self.make_step(state, action)
            state = next_state
            trajectory.append(ts)
        return trajectory

    def evaluate_trajectories(self):
        raise NotImplementedError

    @staticmethod
    def convert_trajectory(trajectory: list[GymTrajectory]) -> np.ndarray:
        np_traj = np.array([[t.state, t.action, t.reward] for t in trajectory])
        return np_traj

    def run(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.reset_tables()
            for episode in range(self.params.total_episodes):
                trajectory = self.generate_trajectory(self.get_action)
                self.trajectories[episode].append(trajectory)
            qtables[n, :, :] = self.qtable
        self.qtable = qtables.mean(axis=0)
