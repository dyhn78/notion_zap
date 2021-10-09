from typing import Any, Optional

from .stash import BlockChildrenStash, PagePropertyStash
from notion_py.interface.struct import Gateway, PointEditor,\
    drop_empty_request, print_response_error
from notion_py.interface.api_encode import ContentsEncoder
from ...utility import stopwatch, page_id_to_url


class CreatePage(Gateway, PagePropertyStash, BlockChildrenStash):
    def __init__(self, editor: PointEditor, under_database: bool):
        Gateway.__init__(self, editor)
        PagePropertyStash.__init__(self)
        BlockChildrenStash.__init__(self)
        self.parent_type = 'database_id' if under_database else 'page_id'

    @property
    def target_id(self):
        return self.editor.parent_id

    @property
    def target_name(self):
        return self.editor.parent.master_name

    def __bool__(self):
        return any([PagePropertyStash.__bool__(self),
                    BlockChildrenStash.__bool__(self)])

    def unpack(self):
        res = dict(**PagePropertyStash.unpack(self),
                   **BlockChildrenStash.unpack(self),
                   parent={self.parent_type: self.target_id})
        return res

    @drop_empty_request
    @print_response_error
    def execute(self) -> dict:
        res = self.notion.pages.create(**self.unpack())
        self.clear()
        self.print_comments(res)
        return res

    def clear(self):
        PagePropertyStash.clear(self)
        BlockChildrenStash.clear(self)

    def print_comments(self, res):
        comments = ' '.join(
            ['create', f"< {self.target_name} >", '\n\t', page_id_to_url(res['id'])])
        stopwatch(comments)


class UpdatePage(Gateway, PagePropertyStash):
    def __init__(self, editor: PointEditor):
        Gateway.__init__(self, editor)
        PagePropertyStash.__init__(self)
        self._archive_value = None

    def __bool__(self):
        return PagePropertyStash.__bool__(self) \
               or self._archive_value is not None

    def clear(self):
        PagePropertyStash.clear(self)
        self._archive_value = None

    def archive(self):
        self._archive_value = True

    def un_archive(self):
        self._archive_value = False

    def unpack(self):
        res = dict(page_id=self.target_id,
                   **PagePropertyStash.unpack(self))
        if self._archive_value is not None:
            res.update(archived=self._archive_value)
        return res

    @drop_empty_request
    @print_response_error
    def execute(self) -> dict:
        res = self.notion.pages.update(**self.unpack())
        self.clear()
        self.print_comments()
        return res

    def print_comments(self):
        comments = ' '.join(
            ['update', f"< {self.target_name} >", '\n\t',
             page_id_to_url(self.target_id)])
        stopwatch(comments)


class UpdateBlock(Gateway):
    def __init__(self, editor: PointEditor):
        Gateway.__init__(self, editor)
        self._contents_value: Optional[ContentsEncoder] = None
        self._archive_value = None

    def __bool__(self):
        return self._contents_value is not None \
               or self._archive_value is not None

    def clear(self):
        self._contents_value = None
        self._archive_value = None

    def archive(self):
        self._archive_value = True

    def un_archive(self):
        self._archive_value = False

    def apply_contents(self, carrier: ContentsEncoder):
        self._contents_value = carrier
        return carrier

    def unpack(self):
        res = dict(block_id=self.target_id)
        if self._contents_value is not None:
            res.update(**self._contents_value.unpack())
        if self._archive_value is not None:
            res.update(archived=self._archive_value)
        return res

    @drop_empty_request
    @print_response_error
    def execute(self) -> dict:
        res = self.notion.blocks.update(**self.unpack())
        self.clear()
        self.print_comments()
        return res

    def print_comments(self):
        comments = ' '.join(
            ['update', f"< {self.target_name} >", '\n\t',
             page_id_to_url(self.target_id)])
        stopwatch(comments)


class AppendBlockChildren(Gateway, BlockChildrenStash):
    def __init__(self, editor: PointEditor):
        Gateway.__init__(self, editor)
        BlockChildrenStash.__init__(self)

    def __bool__(self):
        return BlockChildrenStash.__bool__(self)

    def unpack(self) -> dict[str, Any]:
        return dict(**BlockChildrenStash.unpack(self),
                    block_id=self.target_id)

    @drop_empty_request
    @print_response_error
    def execute(self) -> dict:
        res = self.notion.blocks.children.append(**self.unpack())
        self.clear()
        self.print_comments()
        return res

    def clear(self):
        BlockChildrenStash.clear(self)

    def print_comments(self):
        if self.target_name:
            comments = ' '.join(
                ['append', f"< {self.target_name} >", '\n\t',
                 page_id_to_url(self.target_id)])
        else:
            comments = ' '.join(['append', page_id_to_url(self.target_id)])
        stopwatch(comments)
