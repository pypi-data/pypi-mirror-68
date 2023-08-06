import sys
from typing import Any, List

from .github_types.terraform_types import TerraformSyntax, Resource, Block
from .util import convert_type_to_method


class Writer:
    def __init__(self, out, indent: int = 0):
        self._out = out
        self.indent = indent

    def __call__(self, text: str):
        indent = self.indent * " "
        print(indent + str(text), file=self._out)


class Formatter:
    def __init__(self, label: str, value: Any, indentation: int = 0):
        self._label = label
        self._value = value
        self._indent = indentation

    def get_writer(self, out):
        return Writer(out, indent=self._indent)

    @staticmethod
    def format(resource_name: str, item: Resource, out=sys.stdout):
        formatter = get_formatter(type(item))
        if formatter is not None:
            resource_name = sanitize_resource_name(resource_name)
            formatter(resource_name, item).write(out)


class StrFormatter(Formatter):
    def write(self, out):
        writer = self.get_writer(out)

        value = str(self._value)
        if value.startswith("${") and value.endswith("}"):
            value = value[2:-1]
        else:
            value = f'"{value}"'

        writer(f'{self._label} = {value}')


class BoolFormatter(Formatter):
    def write(self, out):
        writer = self.get_writer(out)
        value = "true" if self._value else "false"
        writer(f"{self._label} = {value}")


class IntFormatter(Formatter):
    def write(self, out):
        writer = self.get_writer(out)
        writer(f"{self._label} = {self._value}")


class ListFormatter(Formatter):
    def write(self, out):
        writer = self.get_writer(out)
        if len(self._value) == 0:
            writer(f"{self._label} = []")
            return

        writer(f"{self._label} = [")
        writer.indent += 4
        for item in self._value:
            writer(f'"{item}",')
        writer.indent -= 4
        writer("]")


class ArgumentListFormatter(Formatter):
    IGNORED_ARGUMENTS = ("resource_type", "resource_name")

    def __init__(self, arguments, indentation: int = 0):
        super().__init__(None, None, indentation)
        self._arguments = arguments

    def write(self, out):
        writer = self.get_writer(out)
        for field, field_type, value in self._arguments:
            if field.startswith("_"):
                continue
            if field in ArgumentListFormatter.IGNORED_ARGUMENTS:
                continue
            if value is None:
                continue
            formatter = get_formatter(field_type)
            formatter(field, value, indentation=writer.indent).write(out)


class BlockFormatter(Formatter):
    def write(self, out):
        writer = self.get_writer(out)

        writer(f"{self._label} {{")
        writer.indent += 4

        arguments = zip_annotations(self._value)
        formatter = ArgumentListFormatter(arguments, indentation=writer.indent)
        formatter.write(out)

        writer.indent -= 4
        writer("}")


class ResourceFormatter(Formatter):
    def write(self, out):
        writer = self.get_writer(out)
        type_ = convert_type_to_method(type(self._value))
        name = self._label

        writer(f'resource "{type_}" "{name}" {{')
        writer.indent += 4

        arguments = zip_annotations(self._value)
        formatter = ArgumentListFormatter(arguments, indentation=writer.indent)
        formatter.write(out)

        writer.indent -= 4
        writer("}\n")


class UnresolvedFormatter(Formatter):
    def write(self, out):
        writer = self.get_writer(out)
        writer(f"WARNING: Unresolved handler for {self._label}")


FORMATTERS = {
    TerraformSyntax: UnresolvedFormatter,
    Resource: ResourceFormatter,
    Block: BlockFormatter,
    str: StrFormatter,
    bool: BoolFormatter,
    int: IntFormatter,
    list: ListFormatter,
}


def get_formatter(item: type):
    try:
        classes = type.mro(item)
    except TypeError:
        classes = type.mro(item.__origin__)

    for class_ in classes:
        formatter = FORMATTERS.get(class_, None)
        if formatter is not None:
            return formatter

    return UnresolvedFormatter


def zip_annotations(dataclass):
    annotations = dataclass.__annotations__
    values = map(lambda field: getattr(dataclass, field), annotations)

    return list(zip(annotations.keys(), annotations.values(), values))


def sanitize_resource_name(resource_name):
    resource_name = str(resource_name)
    if not resource_name[0].isalpha():
        resource_name = "n" + resource_name
    
    resource_name = resource_name.replace(" ", "-").replace(":", "-")
    resource_name = resource_name.replace("/", "-").replace(".", "-")
    resource_name = resource_name.replace("\\", "-").replace("(", "-")
    resource_name = resource_name.replace(")", "-")
    resource_name = resource_name.encode("ascii", "ignore").decode()

    return resource_name
