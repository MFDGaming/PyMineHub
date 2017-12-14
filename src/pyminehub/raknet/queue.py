import time
from queue import PriorityQueue
from typing import Callable, Set

from pyminehub.config import ConfigKey, get_value
from pyminehub.network.packet import Packet
from pyminehub.raknet.codec import capsule_codec


class SendQueue:

    def __init__(self, max_payload_size: int, send_frames: Callable[[bytes], None]) -> None:
        self._max_payload_size = max_payload_size
        self._send_frames = send_frames
        self._queue = PriorityQueue()
        self._messages_to_be_discarded = set()  # type: Set[int]  # set of reliable_message_num

    @staticmethod
    def _get_current_time() -> int:
        return time.time()

    @staticmethod
    def _get_resend_time_in_future() -> int:
        return time.time() + get_value(ConfigKey.RESEND_TIME)

    def push(self, capsule: Packet, send_time_in_future=0) -> None:
        self._queue.put_nowait((self._get_current_time() + send_time_in_future, capsule))

    def discard(self, reliable_message_num: int) -> None:
        self._messages_to_be_discarded.add(reliable_message_num)

    def send(self) -> None:
        buffer = bytearray()
        while not self._queue.empty():
            send_time, capsule = self._queue.get_nowait()
            if send_time > self._get_current_time():
                self._queue.put_nowait((send_time, capsule))
                break
            if hasattr(capsule, 'reliable_message_num'):
                if capsule.reliable_message_num in self._messages_to_be_discarded:
                    continue
                else:
                    self._queue.put_nowait((self._get_resend_time_in_future(), capsule))
            payload = capsule_codec.encode(capsule)
            # TODO: len(buffer) > self._max_payload_size
            if len(buffer) + len(payload) > self._max_payload_size:
                self._send_frames(bytes(buffer))
                buffer = bytearray()
            else:
                buffer.extend(payload)
        if len(buffer) > 0:
            self._send_frames(bytes(buffer))
