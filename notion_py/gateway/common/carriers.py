from __future__ import annotations
from abc import abstractmethod, ABC, ABCMeta


class ValueCarrier(ABC):
    @abstractmethod
    def unpack(self) -> dict:
        pass

    def __bool__(self):
        return bool(self.unpack())


class ValueCarrierDeprecated(ValueCarrier, metaclass=ABCMeta):
    pass


class Requestor(ValueCarrier):
    @abstractmethod
    def execute(self):
        pass


class Stash(ValueCarrierDeprecated, metaclass=ABCMeta):
    def __init__(self):
        self._subdicts: list[dict] = []

    def __bool__(self):
        return bool(self._subdicts)

    def clear(self):
        self._subdicts = []


class ListStash(Stash, metaclass=ABCMeta):
    def _unpack(self):
        return self._subdicts


class DictStash(Stash, metaclass=ABCMeta):
    def _unpack(self):
        res = {}
        for subdict in self._subdicts:
            for key, value in subdict.items():
                res[key] = value
        return res


class TwofoldStash(ValueCarrier, metaclass=ABCMeta):
    def __init__(self):
        self._subcarriers: list[ValueCarrier] = []

    def __bool__(self):
        if not self._subcarriers:
            return False
        return any(bool(carrier) for carrier in self._subcarriers)

    def clear(self):
        self._subcarriers = []

    def apply(self, carrier: ValueCarrier):
        """
        return 값을 carrier가 아니라 subcarriers[-1]로 설정하였다.
        본래 리스트 append 메소드는 원본 id를 그대로 유지한 채 집어넣어야 정상이지만,
        id 값을 조사해보면 컴퓨터가 carrier의 복사본을 넣는다는 점을 발견할 수 있다.
        """
        self._subcarriers.append(carrier)
        return self._subcarriers[-1]
