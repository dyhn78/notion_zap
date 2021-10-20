from abc import ABCMeta
from typing import Optional

from notion_py.interface.common.struct import Editor
from notion_py.interface.editor.struct import GroundEditor
from notion_py.interface.parser import BlockContentsParser
from ..child_bearing import ChildBearingBlock


class ContentsBearingBlock(ChildBearingBlock, metaclass=ABCMeta):
    def __init__(self, caller: Editor, block_id: str):
        super().__init__(caller, block_id)
        self.caller = caller
        self.contents: Optional[BlockContents] = None

    def reads(self):
        return {'contents': self.contents.reads(),
                'children': self.sphere.reads()}

    def reads_rich(self):
        return {'contents': self.contents.reads_rich(),
                'children': self.sphere.reads_rich()}

    def preview(self):
        return {'contents': self.contents.preview(),
                **self.sphere.preview()}


class BlockContents(GroundEditor, metaclass=ABCMeta):
    def __init__(self, caller: ContentsBearingBlock):
        super().__init__(caller)
        self.caller = caller
        self._read_plain = ''
        self._read_rich = []

    def reads(self) -> str:
        return self._read_plain

    def reads_rich(self) -> list:
        return self._read_rich

    def apply_block_parser(self, parser: BlockContentsParser):
        if parser.block_id:
            self.master_id = parser.block_id
            self.yet_not_created = False
        self.caller.has_children = parser.has_children
        self.caller.can_have_children = parser.can_have_children
        self._read_plain = parser.read_plain
        self._read_rich = parser.read_rich
