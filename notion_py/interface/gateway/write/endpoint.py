from typing import Optional

from notion_py.interface.utility import stopwatch, page_id_to_url
from .stash_block import BlockChildrenStash
from .stash_property import PagePropertyStash
from ...struct import Gateway, retry_request, ValueCarrier


class UpdatePage(Gateway):
    def __init__(self, page_id):
        self.page_id = page_id
        self.props = PagePropertyStash()

    def __bool__(self):
        return bool(self.props.unpack())

    def unpack(self):
        return dict(**self.props.unpack(),
                    page_id=self.page_id)

    @retry_request
    def execute(self):
        if not bool(self):
            return {}
        res = self.notion.pages.update(**self.unpack())
        stopwatch(' '.join(['update', page_id_to_url(self.page_id)]))
        return res


class CreatePage(Gateway):
    def __init__(self, parent_id: str):
        self.parent_id = parent_id
        self.props = PagePropertyStash()
        self.children = BlockChildrenStash()

    def __bool__(self):
        return any([bool(self.props.unpack()),
                    bool(self.children.unpack())])

    def unpack(self):
        return dict(**self.props.unpack(),
                    **self.children.unpack(),
                    parent={'page_id': self.parent_id})

    @retry_request
    def execute(self):
        if not bool(self):
            return {}
        res = self.notion.pages.create(**self.unpack())
        stopwatch(' '.join(['create', page_id_to_url(res['id'])]))
        return res


class UpdateBlock(Gateway):
    # TODO
    def __init__(self, block_id: str):
        self.block_id = block_id
        self.contents: Optional[ValueCarrier] = None
        pass

    def __bool__(self):
        return self.contents is not None

    def unpack(self):
        return dict(**self.contents.unpack(),
                    block_id=self.block_id)

    @retry_request
    def execute(self):
        if not bool(self):
            return {}
        res = self.notion.blocks.update(**self.unpack())
        stopwatch(' '.join(['update', page_id_to_url(self.block_id)]))
        return res


class AppendBlockChildren(Gateway):
    def __init__(self, parent_id: str):
        self.parent_id = parent_id
        self.children = BlockChildrenStash()
        self.overwrite_option = True

    def __bool__(self):
        return bool(self.children.unpack())

    def unpack(self):
        return dict(**self.children.unpack(),
                    block_id=self.parent_id)

    @retry_request
    def execute(self):
        if not bool(self):
            return {}
        res = self.notion.blocks.children.append(**self.unpack())
        stopwatch(' '.join(['append', page_id_to_url(self.parent_id)]))
        return res
