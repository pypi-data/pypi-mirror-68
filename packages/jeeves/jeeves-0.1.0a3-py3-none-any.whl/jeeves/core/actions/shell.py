import os
import tempfile
import subprocess
from typing import Text

from jeeves.core.objects import Result
from jeeves.core.actions.base import Action


class ScriptAction(Action):
    """
    Executes the provided script direcly on the system.

    The script is written into a temporary file that is then executed.

    If no shebang is provided, a default of ``#!/bin/bash -e`` will be used, if
    the provided shebang interpreter is not found on the system the action will fail.

    The working directory for the process is the workspace path by default. This path
    is also exposed as the ``WORKSPACE_PATH`` environment variable.

    .. automethod:: _get_script
    """

    DEFAULT_SHEBANG = "#!/bin/bash"

    id = "contrib/script"
    verbose_name = "Execute script"

    class Parameters(Action.Parameters):
        """
        +----------------+------+-----------+---------------------------+
        | Parameter name | Type | Mandatory | Description               |
        +================+======+===========+===========================+
        | ``script``     | text | yes       | The script to be executed |
        +----------------+------+-----------+---------------------------+
        """
        PARSE_WITH_ARGUMENTS = {"script"}

        script: Text

    def _get_script(self):
        """
        Returns the script defined in the parameters, checking for a shebang.

        If no shebang is defined, :any:`ScriptAction.DEFAULT_SHEBANG` with be used.
        """
        script = self.parsed_parameters["script"]
        if not script.startswith("#!"):
            return f"{self.DEFAULT_SHEBANG}{os.linesep}{script}"
        return script

    def execute(self, **kwargs):
        workspace = kwargs.get("workspace")
        script = self._get_script()

        # Write the script to a temporary file
        script_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        with script_file as handler:
            handler.write(script)

        # Read/Execute only for owner
        os.chmod(script_file.name, mode=0o500)

        process = subprocess.run(
            script_file.name,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=workspace.path,
            env={"WORKSPACE_PATH": workspace.path},
        )

        os.unlink(script_file.name)

        return Result(
            success=process.returncode == 0, output=process.stdout.decode("utf-8")
        )
