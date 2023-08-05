import sys
import os.path
import tempfile
from unittest import mock
from subprocess import CompletedProcess

from jeeves.core.objects import Task
from jeeves.core.registry import ActionRegistry


MOCK_DEFINITION = {
    "type": "contrib/script",
    "name": "Say hello world in bash",
    "parameters": {"script": "#!/bin/bash\necho Hello World"},
}


def get_completed_process(returncode=0, stdout=b"", **kwargs):
    """Mocks a :class:`subprocess.CompletedProcess` object"""
    return CompletedProcess("", returncode=returncode, stdout=stdout, **kwargs)


@mock.patch("subprocess.run", mock.MagicMock(return_value=get_completed_process()))
def test_script_bash_task_ok(workspace_obj):
    task = Task.parse_obj(MOCK_DEFINITION)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    result = action.execute(workspace=workspace_obj)
    assert result.success


@mock.patch(
    "subprocess.run", mock.MagicMock(return_value=get_completed_process(returncode=1))
)
def test_script_bash_task_ko(workspace_obj):
    task = Task.parse_obj(MOCK_DEFINITION)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    result = action.execute(workspace=workspace_obj)
    assert not result.success


@mock.patch("subprocess.run", mock.MagicMock(return_value=get_completed_process()))
def test_script_no_shebang_defaults_to_bash_ok(workspace_obj):
    definition = MOCK_DEFINITION.copy()
    definition["parameters"]["script"] = definition["parameters"]["script"].strip(
        "#!/bin/bash"
    )
    task = Task.parse_obj(definition)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    assert action._get_script().startswith(action.DEFAULT_SHEBANG)
    result = action.execute(workspace=workspace_obj)
    assert result.success


@mock.patch("subprocess.run", mock.MagicMock(return_value=get_completed_process()))
def test_script_with_other_shebang_ok(workspace_obj):
    py_interpreter = sys.executable
    expected_output = "Hello world! (from python)"
    definition = MOCK_DEFINITION.copy()
    py_script = f"#!{py_interpreter}\nprint('{expected_output}')"
    definition["parameters"]["script"] = py_script
    task = Task.parse_obj(definition)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    assert action._get_script().startswith(f"#!{py_interpreter}")
    result = action.execute(workspace=workspace_obj)
    assert result.success


def test_script_stdout_and_stderr_is_sent_to_result_ok(workspace_obj):
    """
    ..warning:: This test actually calls ``subprocess.run``.

    Not 100% sure this one is needed since we are just testing that subprocess.STDOUT works.
    I'm leaving it for now since it's important to ensure we get the entire stdout/err in the
    :any:`Result` object.
    """
    script = "\n".join(
        [
            f"#!{sys.executable}",
            "import sys",
            "sys.stdout.write('Hello')",
            "sys.stderr.write('World')",
        ]
    )
    definition = MOCK_DEFINITION.copy()
    definition["parameters"]["script"] = script
    task = Task.parse_obj(definition)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    result = action.execute(workspace=workspace_obj)
    assert "Hello" in result.output
    assert "World" in result.output


@mock.patch("subprocess.run", mock.MagicMock(return_value=get_completed_process()))
def test_script_task_cleans_tempfile_ok(workspace_obj):
    """Make sure that the script is removed from the system after execution"""
    task = Task.parse_obj(MOCK_DEFINITION)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    with mock.patch(
        "tempfile.NamedTemporaryFile", mock.MagicMock(return_value=temp)
    ) as mocked:
        action.execute(workspace=workspace_obj)
        assert not os.path.isfile(mocked.return_value.name)


@mock.patch("subprocess.run", mock.MagicMock(return_value=get_completed_process()))
def test_script_task_sets_permissions_for_owner_only_ok(workspace_obj):
    """Make sure that the script have only read and execution permissions for owner"""
    task = Task.parse_obj(MOCK_DEFINITION)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    with mock.patch(
        "tempfile.NamedTemporaryFile", mock.MagicMock(return_value=temp)
    ) as mocked:
        with mock.patch("os.unlink"):
            action.execute(workspace=workspace_obj)
        stat = os.stat(mocked.return_value.name)
        assert oct(stat.st_mode).endswith("500")
        os.unlink(mocked.return_value.name)


@mock.patch("subprocess.run")
def test_script_task_appends_workspace_env_variable_ok(run_mock, workspace_obj):
    """Make sure that the WORKSPACE_PATH environment variable is sent correctly"""
    run_mock.return_value = get_completed_process()
    task = Task.parse_obj(MOCK_DEFINITION)
    action = ActionRegistry.get_action(action_id=task.type, parameters=task.parameters)
    action.execute(workspace=workspace_obj)
    assert run_mock.call_args[1]["env"] == {"WORKSPACE_PATH": workspace_obj.path}
