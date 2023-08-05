import os

import pytest

from jeeves.core.objects import Workspace


@pytest.fixture
def workspace_obj():
    """
    Fixture that returns a :any:`core.objects.Workspace` object and then ensures
    the path it's deleted.

    Used for action tests.
    """
    workspace = Workspace()
    yield workspace
    os.rmdir(workspace.path)
