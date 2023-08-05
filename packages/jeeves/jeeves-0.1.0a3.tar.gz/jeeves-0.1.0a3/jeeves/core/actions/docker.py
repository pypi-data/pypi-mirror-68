import os.path
from typing import Text, Optional

import docker
import requests

from jeeves.core.objects import Result
from .base import Action


class DockerBuildAction(Action):
    """
    """

    id = "contrib/docker/build"
    verbose_name = "Build docker image"

    class Parameters(Action.Parameters):
        """
        """

        dockerfile_path: Text
        image_name: Text
        tag: Text = "latest"

    def execute(self, **kwargs):
        workspace = kwargs.get("workspace")

        client = docker.from_env()

        client.images.build(
            path=workspace,
            fileobj=os.path.join(workspace, self.parameters.dockerfile_path),
        )


class DockerRunAction(Action):
    """
    """

    id = "contrib/docker/run"
    verbose_name = "Execute docker container"

    class Parameters(Action.Parameters):
        """
        +----------------------+------+-----------+--------------------------------------------------------------+
        | Parameter name       | Type | Mandatory | Description                                                  |
        +======================+======+===========+==============================================================+
        | ``image``            | text | no        | Image to run (defaults to ``alpine:latest``)                 |
        | ``command``          | text | yes       | The command to be executed                                   |
        | ``entrypoint``       | text | no        | The entrypoint to use (defaults in image)                    |
        | ``tty``              | bool | no        | Allocate pseudo-tty (defaults to ``false``)                  |
        | ``remove_container`` | text | no        | Select to remove container after run (defaults to ``true`` ) |
        +----------------------+------+-----------+--------------------------------------------------------------+
        """

        image: Text = "alpine:latest"
        command: Text
        entrypoint: Optional[Text] = None
        tty: bool = False
        remove_container: bool = True

        PARSE_WITH_ARGUMENTS = {"command", "image"}

    def execute(self, **kwargs):
        workspace = kwargs.get("workspace")
        arguments = kwargs.get("arguments")
        image = self.parameters.image
        environment = {"WORKSPACE_PATH": "/workspace"}

        # Add arguments as uppercase environment variables prefixed with JEEVES_
        if arguments:
            for key, value in arguments.items():
                environment[f"JEEVES_{key.upper}"] = value

        client = docker.from_env()

        self.logger.info("Pulling image...")
        try:
            client.images.get(image)
        except docker.errors.ImageNotFound:
            self.logger.error(f"Image '{image}' does not exist")
            return Result(success=False)

        run_kwargs = dict(
            image=image,
            command=self.parsed_parameters["command"],
            detach=True,
            environment=environment,
            tty=self.parameters.tty,
            volumes={"/workspace": {"bind": str(workspace.path), "mode": "rw"}},
            working_dir="/workspace",
        )

        if self.parameters.entrypoint:
            run_kwargs["entrypoint"] = self.parameters.entrypoint

        self.logger.info("Execute command in container...")
        container = client.containers.run(**run_kwargs)

        try:
            result = container.wait(timeout=30, condition="not-running")
            logs = container.logs()
            success = result["StatusCode"] == 0
        except requests.exceptions.ReadTimeout:
            success = False
            logs = container.logs()

        if self.parameters.remove_container:
            self.logger.info("Removing container")
            container.remove()

        return Result(success=success, output=logs)
