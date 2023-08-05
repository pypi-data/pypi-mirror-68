from typing import Any, Text, MutableMapping
from pathlib import Path

import toml
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from jeeves.core.objects import Flow, BaseObject, Execution


class ObjectParser:
    object: BaseObject = None

    @classmethod
    def from_dict(cls, serialized: MutableMapping[str, Any]) -> BaseObject:
        return cls.object.parse_obj(serialized)

    @classmethod
    def to_dict(cls, obj: BaseObject) -> dict:
        return obj.dict()

    @classmethod
    def from_json(cls, serialized: Text) -> BaseObject:
        return cls.object.parse_raw(serialized)

    @classmethod
    def from_json_file(cls, path: Path) -> BaseObject:
        return cls.object.parse_file(path)

    @classmethod
    def to_json(cls, obj: BaseObject) -> Text:
        return obj.json()

    @classmethod
    def from_toml(cls, serialized: Text) -> BaseObject:
        dct = toml.loads(serialized)
        return cls.from_dict(dct)

    @classmethod
    def from_toml_file(cls, path) -> BaseObject:
        dct = toml.load(path)
        return cls.from_dict(dct)

    @classmethod
    def to_toml(cls, obj: BaseObject) -> Text:
        return toml.dumps(cls.to_dict(obj))

    @classmethod
    def from_yaml(cls, serialized: Text) -> BaseObject:
        dct = yaml.load(serialized, Loader=Loader)
        return cls.from_dict(dct)

    @classmethod
    def from_yaml_file(cls, path) -> BaseObject:
        dct = yaml.load(path, Loader=Loader)
        return cls.from_dict(dct)

    @classmethod
    def to_yaml(cls, obj: BaseObject) -> Text:
        return yaml.dump(cls.to_dict(obj), Dumper=Dumper)


class FlowParser(ObjectParser):
    object = Flow


class ExecutionParser(ObjectParser):
    object = Execution
