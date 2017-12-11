from typing import NamedTuple as _NamedTuple, Tuple, Union, Optional

from pyminehub.mcpe.const import *
from pyminehub.mcpe.geometry import *

PlayerData = _NamedTuple('PlayerData', [
    ('xuid', int),
    ('identity', str),
    ('display_name', str),
    ('identity_public_key', str)
])

ClientData = _NamedTuple('ClientData', [
    ('client_random_id', int),
    ('language_code', str)
])


class ConnectionRequest(_NamedTuple('ConnectionRequest', [
    ('chain', Tuple[dict, ...]),  # NOTE: dict is mutable
    ('client', dict)  # NOTE: dict is mutable
])):
    _KEY_EXTRA = 'extraData'

    def get_player_data(self) -> PlayerData:
        for webtoken in self.chain:
            if self._KEY_EXTRA in webtoken:
                extra_data = webtoken[self._KEY_EXTRA]
                return PlayerData(
                    int(extra_data['XUID']), extra_data['identity'], extra_data['displayName'],
                    webtoken['identityPublicKey'])
        raise AssertionError('ConnectionRequest must have extraData.')

    def get_client_data(self) -> ClientData:
        return ClientData(self.client['ClientRandomId'], self.client['LanguageCode'])


PackEntry = _NamedTuple('PackEntry', [
    ('id', str),
    ('version', str),
    ('size', int),
    ('unknown1', str),
    ('unknown2', str)
])

PackStack = _NamedTuple('PackStack', [
    ('id', str),
    ('version', str),
    ('unknown1', str)
])

GameRule = _NamedTuple('GameRule', [
    ('name', str),
    ('type', GameRuleType),
    ('value', Union[bool, int, float])
])

Attribute = _NamedTuple('Attribute', [
    ('min', float),
    ('max', float),
    ('current', float),
    ('default', float),
    ('name', str)
])

CommandEnum = _NamedTuple('CommandEnum', [
    ('name', str),
    ('index', Tuple[int, ...])
])

CommandParameter = _NamedTuple('CommandParameter', [
    ('name', str),
    ('type', int),
    ('is_optional', bool)
])

CommandData = _NamedTuple('CommandData', [
    ('name', str),
    ('description', str),
    ('flags', int),
    ('permission', int),
    ('aliases', int),
    ('overloads', Tuple[Tuple[CommandParameter], ...])
])

Slot = _NamedTuple('Slot', [
    ('id', int),
    ('aux_value', Optional[int]),
    ('nbt', Optional[bytes]),
    ('place_on', Optional[str]),
    ('destroy', Optional[str])
])

MetaDataValue = Union[int, float, str, Vector3, Slot]

EntityMetaData = _NamedTuple('EntityMetaData', [
    ('key', int),
    ('type', MetaDataType),
    ('value', MetaDataValue)
])

UUID = _NamedTuple('UUID', [
    ('part1', int),
    ('part0', int),
    ('part3', int),
    ('part2', int)
])

Skin = _NamedTuple('Skin', [
    ('id', str),
    ('data', bytes),
    ('cape', str),
    ('geometry_name', str),
    ('geometry_data', str)
])

PlayerListEntry = _NamedTuple('PlayerListEntry', [
    ('uuid', UUID),
    ('entity_unique_id', Optional[int]),
    ('user_name', Optional[str]),
    ('skin', Optional[Skin]),
    ('xbox_user_id', Optional[str])
])

RecipeForNormal = _NamedTuple('RecipeForNormal', [
    ('width', Optional[int]),
    ('height', Optional[int]),
    ('input', Tuple[Slot, ...]),
    ('output', Tuple[Slot, ...]),
    ('uuid', UUID)
])

RecipeForFurnace = _NamedTuple('RecipeForFurnace', [
    ('input_id', int),
    ('input_damage', Optional[int]),
    ('output', Slot)
])

RecipeForMulti = _NamedTuple('RecipeForMulti', [
    ('uuid', UUID)
])

RecipeData = Union[RecipeForNormal, RecipeForFurnace, RecipeForMulti]

Recipe = _NamedTuple('Recipe', [
    ('type', RecipeType),
    ('data', RecipeData)
])
