import seaborn as sns

# project imports
from frozenlake.utils.helpers import get_params, get_env
from frozenlake.rmc import Agent


def main():
    sns.set_theme()

    params = get_params()
    env = get_env(params)

    agent = Agent(env, params)
    agent.run()
    agent.pprint_q_table()


if __name__ == '__main__':
    main()
