import os.path
import time

import click

from jeeves.cli.echo import info, error, title, success
from jeeves.core.parsers import FlowParser, ExecutionParser
from jeeves.core.executor import Executor
from jeeves.core.registry import ActionRegistry


@click.group()
def main():
    # TODO: Check if Jeevesfile in cwd, execute directly
    ActionRegistry.autodiscover()
    pass


@main.command()
@click.argument("defintinion_file", type=click.File())
@click.option(
    "--output",
    "print_output",
    is_flag=True,
    default=False,
    help="Display output for flow",
)
@click.option("--argument", "-a", "defined_arguments", multiple=True, default=[])
@click.option("--save-execution", is_flag=True, default=False, help="Store execution")
def execute(defintinion_file, print_output, save_execution, defined_arguments=list):
    extension = os.path.splitext(defintinion_file.name)[1][1:]

    if not hasattr(FlowParser, f"from_{extension}"):
        error(f"Extension {extension} is not supported")
        exit(1)

    info(f"Running flow from {defintinion_file.name}")

    flow = getattr(FlowParser, f"from_{extension}")(defintinion_file.read())

    arguments = {}
    for argument in defined_arguments:
        key, value = argument.split("=")
        arguments[key] = value

    title(f"Running flow: {flow.name}")
    executor = Executor(flow=flow, defined_arguments=arguments)

    for n, step in enumerate(executor.steps, start=1):
        click.echo(
            f" ** Running step [{n}/{executor.step_count}]: {step.task.name}\r",
            nl=False,
        )
        result = executor.execute_step(step)

        if not result.success:
            error(f"Executing step [{n}/{executor.step_count}]: {step.task.name}")
            if print_output:
                click.echo(result.output)
            break
        else:
            success(f"Running step [{n}/{executor.step_count}]: {step.task.name}")

            if print_output:
                click.echo(result.output)

    if save_execution:
        with open(f"execution.{time.time_ns()}.json", "w") as handler:
            handler.write(ExecutionParser.to_json(executor._execution))
