import os
from pprint import pprint
from typing import Optional

from notion_client import Client, AsyncClient

from ..common import PropertyFrame
from ..common.struct import AbstractRootEditor
from ..utility import page_url_to_id
from .struct import MasterEditor
from .inline.text_block import TextBlock
from .inline.page_block import InlinePageBlock
from .tabular.database import Database
from .tabular.page import TabularPageBlock


class RootEditor(AbstractRootEditor):
    def __init__(self, async_client=False):
        super().__init__()
        self.top_editors: list[MasterEditor] = []
        self.by_id: dict[str, MasterEditor] = {}
        if async_client:
            self.notion = AsyncClient(auth=self.token)
        else:
            self.notion = Client(auth=self.token)

    def __bool__(self):
        return any([bool(editor) for editor in self.top_editors])

    def ids(self):
        return self.by_id.keys()

    def open_text_block(self, id_or_url: str):
        block_id = page_url_to_id(id_or_url)
        editor = TextBlock(self, block_id)
        self.top_editors.append(editor)
        return editor

    def preview(self, pprint_this=True):
        preview = [editor.preview() for editor in self.top_editors]
        if pprint_this:
            pprint(preview)
        return preview

    def open_database(self, database_alias: str, id_or_url: str,
                      frame: Optional[PropertyFrame] = None):
        database_id = page_url_to_id(id_or_url)
        editor = Database(self, database_id, database_alias, frame)
        self.top_editors.append(editor)
        return editor

    def open_pagelist(self, database_alias: str, id_or_url: str,
                      frame: Optional[PropertyFrame] = None):
        database_id = page_url_to_id(id_or_url)
        database = Database(self, database_id, database_alias, frame)
        editor = database.pagelist
        self.top_editors.append(editor)
        return editor

    def open_tabular_page(self, id_or_url: str,
                          frame: Optional[PropertyFrame] = None):
        page_id = page_url_to_id(id_or_url)
        editor = TabularPageBlock(self, page_id, frame)
        self.top_editors.append(editor)
        return editor

    def execute(self):
        for editor in self.top_editors:
            editor.execute()

    def open_inline_page(self, id_or_url: str):
        page_id = page_url_to_id(id_or_url)
        editor = InlinePageBlock(self, page_id)
        self.top_editors.append(editor)
        return editor

    @property
    def token(self):
        return os.environ['NOTION_TOKEN'].strip("'").strip('"')
