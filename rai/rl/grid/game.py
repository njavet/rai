from rich.console import Console
from jinja2 import Environment, FileSystemLoader
import numpy as np

# project imports
from rai.rl.grid.environment import Grid
from rai.rl.grid.agent import Agent


def main():
    e = Environment(loader=FileSystemLoader('templates'))
    template = e.get_template('grid.template')
    env = Grid()
    agent = Agent(env)
    for eps in range(2048):
        agent.run_episode()

    values = np.zeros((env.height, env.width))
    actions = np.zeros((env.height, env.width))
    for x in range(env.height):
        for y in range(env.width):
            tmp = [agent.action_value(x, y, a) for a in range(4)]
            v = np.sum(tmp) / 4
            values[x, y] = v
            ind = np.argmax(tmp)
            actions[x, y] = agent.action_space[ind].value

    hsep = env.width * 10 * '-'
    output = template.render(height=env.height,
                             width=env.width,
                             grid=values,
                             hsep=hsep)
    console = Console()
    console.print('value function:')
    console.print(output, style='cyan')
    output = template.render(height=env.height,
                             width=env.width,
                             grid=actions,
                             hsep=hsep)
    console.print('action function:')
    console.print(output, style='cyan')

    trajectory = agent.run()
    for t in trajectory:
        print(t.state, t.action, t.reward)
