"""
This is a collection of Actions provided for testing purposes only.
"""
from typing import Text, Optional

from jeeves.core.objects import Result
from .base import Action


class StubSuccessAction(Action):
    id = "stub/success"

    def execute(self, **kwargs):
        return Result(success=True)


class StubNonSuccessAction(Action):
    id = "stub/non-success"

    def execute(self, **kwargs):
        return Result(output="error!", success=False)


class StubUncaughtExceptionAction(Action):
    id = "stub/uncaught-exception"

    def execute(self, **kwargs):
        raise Exception("Oh god...")


class StubNoParametersAction(StubSuccessAction):
    """
    An empty Action that provides no configurable parameters.
    """

    id = "stub/no-parameters"


class StubParametersAction(StubSuccessAction):
    """
    An empty Action that provide two configurable parameters.
    """

    id = "stub/parameters"

    class Parameters(Action.Parameters):
        mandatory: Text
        non_mandatory: Optional[Text] = None
