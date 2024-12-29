from rich.console import Console
from jinja2 import Environment, FileSystemLoader

# project imports
from grid.environment import Grid
from grid.agent import Agent


def main():
    e = Environment(loader=FileSystemLoader('templates'))
    template = e.get_template('grid.template')
    env = Grid()
    hsep = env.width * 3 * '-' + (env.width+1) * '-'
    output = template.render(hsep=hsep, width=env.width, height=env.height,
                             grid=env.grid)
    console = Console()
    console.print(output, style='cyan')
    agent = Agent(env)
    trajectory = agent.generate_trajectory()

    return trajectory

