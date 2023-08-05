import copy
import logging
from abc import abstractmethod

from jinja2 import Template
import pydantic


class Action:
    id = ""

    class Parameters(pydantic.BaseModel):
        PARSE_WITH_ARGUMENTS = set()

    def __init__(self, parameters=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.parameters = self.Parameters(**(parameters or {}))
        self.parsed_parameters = copy.deepcopy(parameters)

    def parse_parameters(self, current_execution=None, **arguments):
        """
        Returns a dict with the parameters parsed in base of the provided arguments and context.
        Parsing using jinja2 template themes only on the fields defined on the `Parameters.PARSE_WITH_ARGUMENTS`.
        """
        for parameter_name in self.parameters.PARSE_WITH_ARGUMENTS:
            self.parsed_parameters[parameter_name] = Template(
                self.parameters.dict()[parameter_name]
            ).render(current_execution=current_execution, **arguments)

    @abstractmethod
    def execute(self, workspace, **kwargs):
        """
        Main method to override that handles the work for the defining action.
        """
        pass
