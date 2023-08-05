# pylint: disable=no-member
import os
import json
import tempfile

import toml

from jeeves.core.objects import Flow, BaseObject
from jeeves.core.parsers import FlowParser
from .factories import FlowFactory

EXPORTED_FLOW = {
    "name": "Test",
    "tasks": [
        {
            "type": "jeeves.core.actions.stub:StubSuccessfulAction",
            "name": "Test Action",
            "parameters": {},
        }
    ],
}


def test_parser_object_to_dict_ok():
    obj: Flow = FlowFactory()
    result = FlowParser.to_dict(obj)
    assert set(obj.dict()).issuperset(set(result))


def test_parser_dict_to_object_ok():
    obj = FlowParser.from_dict(EXPORTED_FLOW)
    assert isinstance(obj, Flow)


########
# JSON #
########
def test_parser_json_to_object_ok():
    obj = FlowParser.from_json(json.dumps(EXPORTED_FLOW))
    assert isinstance(obj, BaseObject)


def test_parser_json_file_to_object_ok():
    export_file = tempfile.NamedTemporaryFile(delete=False, mode="w")
    with export_file as handler:
        handler.write(json.dumps(EXPORTED_FLOW))

    obj = FlowParser.from_json_file(export_file.name)
    assert isinstance(obj, BaseObject)
    os.unlink(export_file.name)


def test_parser_obj_to_json_ok():
    obj: Flow = FlowFactory()
    result = FlowParser.to_json(obj)
    assert set(obj.dict()).issuperset(set(json.loads(result)))


########
# TOML #
########
def test_parser_toml_to_object_ok():
    obj = FlowParser.from_toml(toml.dumps(EXPORTED_FLOW))
    assert isinstance(obj, BaseObject)


def test_parser_toml_file_to_object_ok():
    export_file = tempfile.NamedTemporaryFile(delete=False, mode="w")
    with export_file as handler:
        handler.write(toml.dumps(EXPORTED_FLOW))

    obj = FlowParser.from_toml_file(export_file.name)
    assert isinstance(obj, BaseObject)
    os.unlink(export_file.name)


def test_parser_obj_to_toml_ok():
    obj: Flow = FlowFactory()
    result = FlowParser.to_toml(obj)
    assert set(obj.dict()).issuperset(set(toml.loads(result)))
