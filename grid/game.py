from rich.console import Console
from jinja2 import Environment, FileSystemLoader
import numpy as np

# project imports
from grid.environment import Grid
from grid.agent import Agent


def main():
    e = Environment(loader=FileSystemLoader('templates'))
    template = e.get_template('grid.template')
    env = Grid()
    agent = Agent(env)
    for eps in range(8):
        agent.run_episode()

    values = {}
    for x in range(env.height):
        for y in range(env.width):
            tmp = [agent.action_value(x, y, a) for a in range(4)]
            v = np.sum(tmp) / 4
            values[(x, y)] = v

    hsep = env.width * 3 * '-' + (env.width+1) * '-'
    output = template.render(hsep=hsep, width=env.width, height=env.height,
                             grid=values)
    console = Console()
    console.print(output, style='cyan')
