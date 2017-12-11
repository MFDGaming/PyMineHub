from pyminehub.mcpe.const import GameMode, PlayerPermission
from pyminehub.mcpe.geometry import Vector3
from pyminehub.mcpe.value import PlayerData, ClientData

PlayerID = int
EntityUniqueID = int
EntityRuntimeID = int


class Player:

    def __init__(self):
        self._protocol = None
        self._player_data = None
        self._client_data = None
        self._entity_unique_id = 1
        self._entity_runtime_id = 1
        self._game_mode = GameMode.SURVIVAL
        self._position = Vector3(256.0, 57.625, 256.0)
        self._pitch = 0.0
        self._yaw = 358.0
        self._spawn = Vector3(512, 56, 512)
        self._permission = PlayerPermission.MEMBER

    def id(self) -> PlayerID:
        return self._player_data.xuid

    def login(self, protocol: int, player_data: PlayerData, client_data: ClientData) -> None:
        self._protocol = protocol
        self._player_data = player_data
        self._client_data = client_data

    def get_entity_unique_id(self) -> EntityUniqueID:
        return self._entity_unique_id

    def get_entity_runtime_id(self) -> EntityRuntimeID:
        return self._entity_runtime_id

    def get_game_mode(self) -> GameMode:
        return self._game_mode

    def get_position(self) -> Vector3[float]:
        return self._position

    def get_pitch(self) -> float:
        return self._pitch

    def get_yaw(self) -> float:
        return self._yaw

    def get_sapwn(self) -> Vector3[int]:
        return self._spawn

    def get_permission(self) -> PlayerPermission:
        return self._permission
