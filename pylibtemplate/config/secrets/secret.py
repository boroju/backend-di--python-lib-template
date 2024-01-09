"""The module `secret` contains the `Secret` base class to extend by child implementations."""
from typing import Any, Tuple, Dict

from pylibtemplate.config.envs.environment import Environment


class MetaSecret(type):
    """
    MetaSecrets is a metaclass that manages the Secrets implementations.
    You don't use it if you don't understand the metaclass implementations.
    """

    __secret_classes__ = dict()
    UnresolvedSecret = type("UnresolvedSecret", (Exception,), dict())

    def __clz_new__(cls: Any, ref: str):
        """
        Get the correct Secret implementation to use in function of the format 'IMPLEMENTATION:REFERENCE'.
        Example: EnvironmentSecret:MY_ENV_VAR

        Force the subclasses to implement `resolve(key: str) -> str` in order to resolve the provided `key`.

        If the Environment variable NO_SECRETS is defined (with any value), the resolution of the secrets must
        be ignored.
        """
        impl, cls.key = ref.split(":")

        if impl not in MetaSecret.__secret_classes__:
            raise NotImplementedError(f"{impl} is not a Secret or MetaSecret implementation.")

        singleton_class = MetaSecret.__secret_classes__[impl]
        if not hasattr(singleton_class, "resolve"):
            raise NotImplementedError(f"{cls.__name__} class must implement 'resolve() -> str' method.")

        try:
            return singleton_class.resolve(cls.key)
        except Exception as e:
            if Environment.from_env() == Environment.NONE:
                return None
            else:
                raise MetaSecret.UnresolvedSecret(f"Impossible to resolve secret {cls.key}: {e}.")

    def __new__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any]):
        """Injects common __new__ contructor to all subclasses defined."""
        attrs["__new__"] = cls.__clz_new__
        clz = super().__new__(cls, name, tuple(), attrs)
        cls.__secret_classes__[name] = clz
        return clz


class Secret(metaclass=MetaSecret):
    """
    Base class to extend by child Secret implementations. The metaclass force to implement the static method
    `resolve(key: str) -> str` in order to resolve the provided `key`.

    ```python
    class MySecretTool(Secret):
        def resolve(key: str) -> str:
            ... implementation to recover the value of the 'key'.
            return ...
    ```

    **All childs of this class are registered and you must use this class to reference it using the format:**

    > Implementation_Class:requested_key

    ```python
    Secret("MySecretTool:my_key")
    ```
    """

    def __new__(cls, scope: str):
        ...
