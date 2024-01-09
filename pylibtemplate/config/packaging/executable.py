"""
The module `executable` defines the base class to extend. If you use the `packaging` package, some
functionalities recognize this class as an executable to use
(like `packaging.setup.create_entry_points_from_package` functionality).
"""


class Executable:
    """
    Defines the base class to extend. Must implement a method named `execute(...)`.
    """

    @classmethod
    def execute(cls):
        raise NotImplementedError(
            f"The `execute()` classmethod must be implemented for class {cls.__name__}."
        )
