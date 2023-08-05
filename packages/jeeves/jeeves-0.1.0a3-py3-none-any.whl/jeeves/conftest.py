from jeeves.core.actions.stub import (
    StubSuccessAction,
    StubNonSuccessAction,
    StubParametersAction,
    StubNoParametersAction,
    StubUncaughtExceptionAction,
)
from jeeves.core.actions import PROVIDED_ACTIONS
from jeeves.core.registry import ActionRegistry


def pytest_runtest_setup(item):
    for action in [
        StubSuccessAction,
        StubNonSuccessAction,
        StubParametersAction,
        StubNoParametersAction,
        StubUncaughtExceptionAction,
    ]:
        PROVIDED_ACTIONS[action.id] = action

    ActionRegistry.autodiscover()


def pytest_runtest_teardown(item):
    ActionRegistry.actions = {}
#
