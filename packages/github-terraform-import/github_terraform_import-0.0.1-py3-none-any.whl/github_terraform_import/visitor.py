import inspect

from .github_types import RESOURCES

from .util import convert_type_to_method


class VisitMethodInjector(type):
    def __new__(mcls, name, bases, attrs):
        ignore_missing = attrs.get("ignore_missing", True)
        default_method = attrs.get("default", None)

        new_attrs = attrs.copy()
        declared = []
        missing = []

        for type_ in RESOURCES:
            resource = convert_type_to_method(type_)
            method = f"visit_{resource}"
            visitor = attrs.get(method, None)
            if visitor is not None:
                declared.append(resource)
                continue

            if default_method is not None:
                declared.append(resource)
                new_attrs[method] = default_method
            missing.append(method)

        new_attrs["resources"] = declared

        if not ignore_missing and len(missing) > 0:
            nl = "\n\t"
            raise TypeError(
                f"{name} class missing the following visitor methods (set ignore_missing to true to ignore):{nl}{nl.join(missing)}"
            )

        return super(VisitMethodInjector, mcls).__new__(mcls, name, bases, new_attrs)


class DebugVisitor(metaclass=VisitMethodInjector):
    ignore_missing = True

    def default(self, resource):
        print(resource)
