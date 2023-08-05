from jeeves.core.actions.shell import ScriptAction
from jeeves.core.actions.docker import DockerBuildAction, DockerRunAction
from jeeves.core.actions.files import TemplateAction

__all__ = [
    # Files
    TemplateAction,
    # Shell
    ScriptAction,
    # Docker
    DockerBuildAction,
    DockerRunAction,
]

PROVIDED_ACTIONS = {action.id: action for action in __all__}
