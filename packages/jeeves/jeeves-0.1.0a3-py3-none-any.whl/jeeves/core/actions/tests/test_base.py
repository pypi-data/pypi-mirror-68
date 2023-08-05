import pytest
import pydantic

from jeeves.core.registry import ActionRegistry


def test_action_with_empty_parameters_ok():
    action = ActionRegistry.get_action_cls("stub/no-parameters")
    action()
    action(parameters=None)
    action(parameters={})


def test_action_with_parameters_ok():
    action = ActionRegistry.get_action_cls("stub/parameters")
    action(parameters=dict(mandatory="text", non_mandatory="text"))


def test_action_with_parameters_ko():
    action = ActionRegistry.get_action_cls("stub/parameters")
    with pytest.raises(pydantic.ValidationError):
        action(parameters=dict(thisshould="fail"))
