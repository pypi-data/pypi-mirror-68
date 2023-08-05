import pytest

from jeeves.core.registry import ActionRegistry
from jeeves.core.actions.base import Action
from jeeves.core.actions.stub import StubSuccessAction


def test_registry_get_action_cls_ok():
    action = ActionRegistry.get_action_cls("stub/success")
    assert issubclass(action, Action) and not isinstance(action, Action)


def test_registry_get_action_cls_ko():
    with pytest.raises(ActionRegistry.ActionDoesNotExist):
        ActionRegistry.get_action_cls("non.existant:action")


def test_registry_get_action_ok():
    action = ActionRegistry.get_action("stub/success")
    assert issubclass(action.__class__, Action) and isinstance(action, Action)


def test_registry_namespace_conflict_ok():
    assert StubSuccessAction.id in ActionRegistry.actions
    with pytest.raises(ActionRegistry.ActionIDConflict):
        ActionRegistry.register_action(StubSuccessAction.id, StubSuccessAction)
