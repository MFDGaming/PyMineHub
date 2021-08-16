import binascii
import json
import os
import pickle
from typing import Optional

from pyminehub.config import ConfigKey, get_value
from pyminehub.mcpe.chunk import Chunk, encode_chunk, decode_chunk
from pyminehub.mcpe.geometry import ChunkPosition
from pyminehub.mcpe.value import PlayerState

__all__ = [
    'DataStore',
    'create_data_store'
]


_PICKLE_PROTOCOL = 4


class DataStore:

    def delete_all(self) -> None:
        raise NotImplementedError()

    def save_chunk(self, position: ChunkPosition, chunk: Chunk, insert_only=False) -> None:
        raise NotImplementedError()

    def load_chunk(self, position: ChunkPosition) -> Optional[Chunk]:
        raise NotImplementedError()

    def count_chunk(self) -> int:
        raise NotImplementedError()

    def save_player(self, player_id: str, player: PlayerState, insert_only=False) -> None:
        raise NotImplementedError()

    def load_player(self, player_id: str) -> Optional[PlayerState]:
        raise NotImplementedError()


class _DataBase(DataStore):

    def __init__(self, name: str) -> None:
        self._path = name + '.json'
        if os.path.isfile(self._path):
            try:
                with open(self._path, 'r') as file:
                    self._data = json.load(file)
                    file.close()
            except Exception:
                self._data = {}
        else:
            self._data = {}
        self._create_table()
        
    def _save_table(self) -> None:
        with open(self._path, 'w') as file:
            json.dump(self._data, file)
            file.close()

    def _create_table(self) -> None:
        if "chunk" not in self._data:
            self._data["chunk"] = {}
        if "player" not in self._data:
            self._data["player"] = {}
        self._save_table()

    def delete_all(self) -> None:
        del self._data["chunk"]
        del self._data["player"]
        self._save_table()

    def save_chunk(self, position: ChunkPosition, chunk: Chunk, insert_only=False) -> None:
        encoded_chunk = encode_chunk(chunk)
        self._data["chunk"][":".join([str(position.x), str(position.z)])] = binascii.hexlify(encoded_chunk).decode()
        self._save_table()

    def load_chunk(self, position: ChunkPosition) -> Optional[Chunk]:
        param = ":".join([str(position.x), str(position.z)])
        if param in self._data["chunk"]:
            return decode_chunk(binascii.unhexlify(self._data["chunk"][param]))

    def count_chunk(self) -> int:
        return len(self._data["chunk"])

    def save_player(self, player_id: str, player: PlayerState, insert_only=False) -> None:
        self._data["player"][player_id] = binascii.hexlify(pickle.dumps(player, protocol=_PICKLE_PROTOCOL)).decode()
        self._save_table()

    def load_player(self, player_id: str) -> Optional[PlayerState]:
        if player_id in self._data["player"]:
            return pickle.loads(binascii.unhexlify(self._data["player"][player_id]))

def create_data_store() -> DataStore:
    world_name = get_value(ConfigKey.WORLD_NAME)
    name = world_name.replace(' ', '_')
    seed = get_value(ConfigKey.SEED)
    suffix = ('p' if seed >= 0 else 'n') + str(seed)
    db_name = '{}-{}'.format(name, suffix)
    return _DataBase(db_name)
