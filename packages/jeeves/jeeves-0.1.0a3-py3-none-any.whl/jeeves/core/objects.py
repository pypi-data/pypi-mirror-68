import shutil
import tempfile
from typing import Any, Dict, List, Text, Optional
from dataclasses import field

import pydantic


class BaseObject(pydantic.BaseModel):
    kind: Text = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kind = self.__class__.__name__


class Result(BaseObject):
    output: Text = ""
    success: bool = False


class Task(BaseObject):
    name: Text
    type: Text
    parameters: Optional[Dict[Any, Any]] = None


class Argument(BaseObject):
    name: Text
    default: Optional[Any] = None
    type: Text = "text"
    required: bool = False


class Flow(BaseObject):
    name: Text
    tasks: List[Task] = field(default_factory=list)
    arguments: Optional[List[Argument]] = None


class ExecutionStep(BaseObject):
    task: Task
    result: Optional[Result] = None


class Workspace(BaseObject):
    path: pydantic.DirectoryPath = None  # type: ignore

    @pydantic.validator("path", pre=True, always=True)
    def path_default(cls, v):  # pylint: disable=no-self-argument
        """
        Ensures that a Workspace always have a path set up.
        """
        return v or tempfile.mkdtemp(prefix="jeeves_")

    def destroy(self):
        """
        Removes the workspace path from the filesystem
        """
        shutil.rmtree(self.path)


class Execution(BaseObject):
    flow: Flow
    steps: List[ExecutionStep]
    workspace: Workspace = None  # type: ignore
    arguments: Optional[List[Argument]] = None
    success: bool = False

    @pydantic.validator("workspace", pre=True, always=True)
    def workspace_default(cls, v):  # pylint: disable=no-self-argument
        return v or Workspace()

    # TODO: @pydantic.validator("arguments")

    @property
    def output(self):
        for step in self.steps:
            if step.result.output:
                yield step.result.output
