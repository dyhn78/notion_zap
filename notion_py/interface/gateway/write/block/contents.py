from typing import Optional

from notion_py.interface.struct import ValueCarrier
from notion_py.interface.gateway.parse_deprecated import BlockChildParser


class BlockContents(ValueCarrier):
    def __init__(self):
        self.read: Optional[BlockChildParser] = None
        self._overwrite = True

    def unpack(self) -> dict:
        pass

    def fetch(self, value: BlockChildParser):
        self.read = value

    def set_overwrite(self, value: bool):
        self._overwrite = value
