import logging
from typing import Any, Dict, Text, Type, Optional

from jeeves.core.actions import PROVIDED_ACTIONS
from jeeves.core.actions.base import Action


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class ActionRegistry(metaclass=Singleton):
    actions: Dict[str, str] = {}

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @classmethod
    def autodiscover(cls):
        """Loads all provided actions."""
        # TODO: Third party plugins
        registry = cls()
        for action_id, action_cls in PROVIDED_ACTIONS.items():
            registry.register_action(action_id, action_cls)

    @classmethod
    def register_action(cls, action_id, action_cls):
        registry = cls()

        if action_id in registry.actions:
            raise cls.ActionIDConflict(
                f"Action ID '{action_id}' is already registered"
            )

        registry.actions[action_id] = action_cls

    @classmethod
    def get_action_cls(cls, action_id) -> Type[Action]:
        """Returns the class for the provided action ID"""
        # Right now actions are being imported and returned dinamically because it's easier,
        # but we will need a way of autodiscover all (or register them manually) and
        # referencing them on a list so the user knows which actions are available.

        try:
            return cls.actions[action_id]
        except KeyError as error:
            raise cls.ActionDoesNotExist(f"Error importing action {action_id}: {error}")

    @classmethod
    def get_action(
        cls, action_id: Text, parameters: Optional[Dict[Any, Any]] = None
    ) -> Action:
        """Returns the instanced action for the provided action_id"""
        action_cls: Type[Action] = cls.get_action_cls(action_id)
        return action_cls(parameters=parameters or {})

    class ActionIDConflict(Exception):
        """Raised when an action is defined with an already registered action id"""

        pass

    class ActionDoesNotExist(Exception):
        """Raised when there's a problem retrieving an action. More info will be available on the message."""

        pass
