from typing import Text
import os

from jinja2 import Template

from jeeves.core.objects import Result
from jeeves.core.actions.base import Action


class TemplateAction(Action):
    """
    Parses the source jinja2 template into the output path
    """

    id = "contrib/template"
    verbose_name = "Render template"

    class Parameters(Action.Parameters):
        """
        +----------------+------+-----------+----------------------------------------------+
        | Parameter name | Type | Mandatory | Description                                  |
        +================+======+===========+==============================================+
        | ``src``        | text | yes       | The source template                          |
        | ``dest``       | text | yes       | The destination file (relative to workspace) |
        +----------------+------+-----------+----------------------------------------------+
        """

        src: Text
        dest: Text

    def execute(self, **kwargs):
        workspace = kwargs.get("workspace")
        arguments = kwargs.get("arguments")

        source_path = os.path.join(os.getcwd(), self.parameters.src)

        assert os.path.exists(source_path), "Source template does not exist"

        template = Template(open(source_path, "r").read())
        with open(os.path.join(workspace.path, self.parameters.dest), "w") as handler:
            handler.write(template.render(**arguments))

        return Result(success=True)
