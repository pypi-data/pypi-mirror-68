import traceback
from typing import Dict

from jeeves.core.objects import Flow, Result, Execution, ExecutionStep
from jeeves.core.registry import ActionRegistry


class Executor:
    def __init__(self, flow: Flow, defined_arguments: Dict = None):
        defined_arguments = defined_arguments or {}
        self.step_count = len(flow.tasks)
        self._flow: Flow = flow
        self._execution = Execution(flow=flow, steps=self._generate_execution_steps(flow))
        self._arguments = {}
        if self._flow.arguments:
            for argument in self._flow.arguments:
                # TODO: What happens if not default?
                self._arguments[argument.name] = defined_arguments.get(argument.name, argument.default)
        self._execution.arguments = self._arguments

    @property
    def steps(self):
        for step in self._execution.steps:
            yield step

    def _generate_execution_steps(self, flow: Flow):
        for task in flow.tasks:
            yield ExecutionStep(task=task, result=Result())

    def execute_step(self, step: ExecutionStep):
        try:
            action = ActionRegistry.get_action(action_id=step.task.type, parameters=step.task.parameters)
            action.parse_parameters(current_execution=self._execution, **self._arguments)
            step.result = action.execute(workspace=self._execution.workspace, arguments=self._arguments)
        except Exception as error:
            # Catch unhandled exceptions, mark the result as unsuccessful
            # and append the error as output.
            tb = traceback.format_exc()
            output = "\n".join(
                (
                    "=" * 30,
                    f"Uncaught exception on task {step.task.type}",
                    f"\t{step.task}",
                    f"Error: {error}",
                    tb,
                    "=" * 30,
                )
            )
            step.result = Result(success=False, output=output)
        return step.result

    def start(self):
        """
        Executes (sync) all the actions for the provided flow.
        """
        for step in self.steps:
            self.execute_step(step)
        self._execution.success = step.result.success
        self.post_execution()

    def post_execution(self):
        """
        Cleanup after a flow have been executed.
        """
        self._execution.workspace.destroy()
