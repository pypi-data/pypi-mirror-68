import os.path
from unittest import mock

from jeeves.core.executor import Executor
from jeeves.core.tests.factories import FlowFactory, TaskFactory


def test_executor_success_task_ok():
    task = TaskFactory(type="stub/success")
    flow = FlowFactory(tasks=[task])
    runner = Executor(flow)
    runner.start()
    assert runner._execution.steps[0].result
    assert runner._execution.steps[0].result.success is True
    assert runner._execution.success is True


def test_executor_non_success_task_ok():
    task = TaskFactory(type="stub/non-success")
    flow = FlowFactory(tasks=[task])
    runner = Executor(flow)
    runner.start()
    assert runner._execution.steps[0].result
    assert runner._execution.steps[0].result.success is False
    assert runner._execution.success is False


def test_executor_uncaught_exception_in_task_ok():
    task = TaskFactory(type="stub/uncaught-exception")
    flow = FlowFactory(tasks=[task])
    runner = Executor(flow)
    runner.start()
    assert runner._execution.steps[0].result
    assert runner._execution.steps[0].result.success is False
    assert runner._execution.success is False


@mock.patch("jeeves.core.actions.stub.StubSuccessAction.execute")
def test_executor_run_action_with_workpsace_ok(execute_mock):
    task = TaskFactory(type="stub/success")
    flow = FlowFactory(tasks=[task])
    runner = Executor(flow)
    runner.start()
    assert execute_mock.called
    execute_mock.assert_called_with(workspace=runner._execution.workspace, arguments={})


def test_executor_cleans_workspace_after_ok():
    task = TaskFactory(type="stub/success")
    flow = FlowFactory(tasks=[task])
    runner = Executor(flow)
    path = runner._execution.workspace.path
    runner.start()
    assert not os.path.isdir(path)
