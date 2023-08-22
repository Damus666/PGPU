import typing

if typing.TYPE_CHECKING:
    from ..component.entities import RigidbodyEntity

class Physics:
    _rigidbodies:list["RigidbodyEntity"] = []

    @classmethod
    def _register(cls, rigidbody:"RigidbodyEntity"):
        cls._rigidbodies.append(rigidbody)

    @classmethod
    def _destroyed(cls, rigidbody:"RigidbodyEntity"):
        if rigidbody in cls._rigidbodies: cls._rigidbodies.remove(rigidbody)