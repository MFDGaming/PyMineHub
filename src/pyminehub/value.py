from enum import Enum
from typing import NamedTuple as _NamedTuple, Callable, Dict, Iterable, Sequence, Tuple, Union

from pyminehub.config import ConfigKey, get_value

ValueType = Enum

ValueObject = Union[tuple, _NamedTuple('ValueObject', [])]  # To suppress warnings, NamedTuple is specified.


def _snake2camel(name: str) -> str:
    return ''.join(s.title() for s in name.split('_'))


class ValueObjectFactory:

    def __init__(self, value_specs: Dict[ValueType, Sequence[Tuple[str, type]]]) -> None:
        """Build a factory with the specified specification.

        :param value_specs: tuple has attribute name and attribute type pair
        """
        self._factory = dict(
            (
                value_type,
                self._create_namedtuple_factory(value_type, field_names)
            )
            for value_type, field_names in value_specs.items())

    @staticmethod
    def _create_namedtuple_factory(
            value_type: ValueType, field_names: Iterable[Tuple[str, type]]) -> Callable[..., ValueObject]:
        cls_name = _snake2camel(value_type.name)
        cls = _NamedTuple(cls_name, field_names)

        def namedtuple_factory(*args, **kwargs) -> ValueObject:
            try:
                # noinspection PyCallingNonCallable
                return cls(*args, **kwargs)
            except TypeError as exc:
                exc.args = ('{}.{}'.format(cls_name, exc.args[0]), )
                raise exc

        return namedtuple_factory

    def create(self, value_type: ValueType, *args, **kwargs) -> ValueObject:
        """Create value object.

        >>> factory.create(PacketType.unconnected_pong, 8721, 5065, True, 'MCPE;')
        UnconnectedPong(id=28, time_since_start=8721, server_guid=5065, valid_message_data_id=True, server_id='MCPE;')
        """
        return self._factory[value_type](value_type.value, *args, **kwargs)


class LogString:
    """For lazy evaluation when logging."""

    def __init__(self, value: ValueObject) -> None:
        self._value = value

    def __str__(self) -> str:
        max_length = get_value(ConfigKey.MAX_LOG_LENGTH)
        return str(self._value) if max_length is None else str(self._value)[:max_length]


if __name__ == '__main__':
    class PacketType(ValueType):
        unconnected_pong = 0x1c

    _packet_specs = {
        PacketType.unconnected_pong: [
            ('id', int),
            ('time_since_start', int),
            ('server_guid', bytes),
            ('valid_message_data_id', bool),
            ('server_id', str)
        ]
    }

    factory = ValueObjectFactory(_packet_specs)

    import doctest
    doctest_result = doctest.testmod()
