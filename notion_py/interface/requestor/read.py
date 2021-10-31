from notion_py.interface.editor.common.struct import PointEditor
from .struct import TruthyPointRequestor, TruthyLongRequestor, print_response_error
from ..utility import stopwatch


class RetrieveDatabase(TruthyPointRequestor):
    def __init__(self, editor: PointEditor):
        super().__init__(editor)

    def __bool__(self):
        return bool(self.target_id)

    def encode(self):
        return dict(database_id=self.target_id)

    @print_response_error
    def execute(self):
        return self.notion.databases.retrieve(**self.encode())

    def print_comments(self):
        if self.target_name:
            form = ['retrieve_database', f"< {self.target_name} >",
                    '\n\t', self.target_id]
        else:
            form = ['retrieve_database', self.target_id]
        comments = ' '.join(form)
        stopwatch(comments)


class RetrievePage(TruthyPointRequestor):
    def __init__(self, editor: PointEditor):
        super().__init__(editor)

    def encode(self):
        return dict(page_id=self.target_id)

    @print_response_error
    def execute(self):
        res = self.notion.pages.retrieve(**self.encode())
        self.print_comments()
        return res

    def print_comments(self):
        if self.target_name:
            form = ['retrieve_page', f"< {self.target_name} >",
                    '\n\t', self.target_url]
        else:
            form = ['retrieve_page', self.target_url]
        comments = ' '.join(form)
        stopwatch(comments)


class RetrieveBlock(TruthyPointRequestor):
    def __init__(self, editor: PointEditor):
        super().__init__(editor)

    def __bool__(self):
        return bool(self.target_id)

    def encode(self):
        return dict(block_id=self.target_id)

    @print_response_error
    def execute(self):
        res = self.notion.blocks.retrieve(**self.encode())
        self.print_comments()
        return res

    def print_comments(self):
        if self.target_name:
            form = ['retrieve_block', f"< {self.target_name} >",
                    '\n\t', self.target_id]
        else:
            form = ['retrieve_block', self.target_id]
        comments = ' '.join(form)
        stopwatch(comments)


class GetBlockChildren(TruthyLongRequestor):
    def __init__(self, editor: PointEditor):
        super().__init__(editor)

    def __bool__(self):
        return bool(self.target_id)

    def encode(self, page_size=None, start_cursor=None):
        args = dict(block_id=self.target_id,
                    page_size=(page_size if page_size else self.MAX_PAGE_SIZE))
        if start_cursor:
            args.update(start_cursor=start_cursor)
        return args

    def execute(self, request_size=0):
        res = self._execute_all(request_size, False)
        self.print_comments()
        return res

    @print_response_error
    def _execute_each(self, request_size, start_cursor=None):
        return self.notion.blocks.children.list(
            **self.encode()
        )

    def print_comments(self):
        if self.target_name:
            form = ['fetch_children', f"< {self.target_name} >",
                    '\n\t', self.target_id]
        else:
            form = ['fetch_children', self.target_id]
        comments = ' '.join(form)
        stopwatch(comments)
