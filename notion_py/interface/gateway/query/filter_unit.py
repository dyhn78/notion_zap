from abc import abstractmethod, ABCMeta
from pprint import pprint

from notion_py.interface.struct import ValueCarrier


class QueryFilter(ValueCarrier):
    """참고로, nesting 기준이 Notion 앱에서보다 더 강하다.
    예를 들어 any('contains', ['1', 'A', '@'] 형식으로 필터를 구성할 경우
    Notion 앱에서는 nesting == 0이지만, API 상에서는 1로 판정한다."""

    @property
    @abstractmethod
    def nesting(self):
        pass

    def __and__(self, other):
        """filter1 & filter2 형식으로 사용할 수 있다."""
        return AndFilter([self, other])

    def __or__(self, other):
        """filter1 | filter2 형식으로 사용할 수 있다."""
        return OrFilter([self, other])


class PlainFilter(QueryFilter):
    def __init__(self, plain_filter: dict):
        self._value = plain_filter

    def unpack(self):
        return self._value

    @property
    def nesting(self):
        return 0


class CompoundFilter(QueryFilter, metaclass=ABCMeta):
    def __init__(self, elements: list[QueryFilter]):
        homos = []
        heteros = []
        for e in elements:
            if type(e) == type(self):
                homos.append(e)
            else:
                heteros.append(e)

        self._nesting = 0
        if homos:
            self._nesting = max([e.nesting for e in homos])
        if heteros:
            self._nesting = max(self._nesting, 1 + max([e.nesting for e in heteros]))
        self.elements = heteros
        for e in homos:
            assert isinstance(e, CompoundFilter)
            self.elements.extend(e.elements)

        if self.nesting > 2:
            # TODO: AssertionError 대신 커스텀 에러클래스 정의
            print('Nesting greater than 2!')
            pprint(self.unpack())
            raise AssertionError

    @property
    def nesting(self):
        return self._nesting


class AndFilter(CompoundFilter):
    def unpack(self):
        return {'and': list(e.unpack() for e in self.elements)}


class OrFilter(CompoundFilter):
    def unpack(self):
        return {'or': list(e.unpack() for e in self.elements)}
