from .filter_unit import QueryFilter, PlainFilter
from ..struct import LongRequestor, print_response_error
from ...common import PropertyFrame
from ...editor.struct import PointEditor
from ...utility import page_id_to_url, stopwatch


class Query(LongRequestor):
    def __init__(self, editor: PointEditor, frame: PropertyFrame):
        from .filter_maker import QueryFilterAgent
        from .sort import QuerySort
        super().__init__(editor)
        self._filter_value = PlainFilter({})
        self.sort = QuerySort()
        self.frame = frame
        self.make_filter = QueryFilterAgent(self)

    def __bool__(self):
        return True

    def clear_filter(self):
        self._filter_value = PlainFilter({})

    def push_filter(self, query_filter: QueryFilter):
        if query_filter is not None:
            self._filter_value = query_filter

    def unpack(self, page_size=None, start_cursor=None):
        args = dict(**self.sort.unpack(),
                    database_id=self.target_id,
                    page_size=page_size if page_size else self.MAX_PAGE_SIZE)
        if self._filter_value:
            args.update(filter=self._filter_value.unpack())
        if start_cursor:
            args.update(start_cursor=start_cursor)
        return args

    def execute(self, request_size=0):
        self.print_comments()
        return self._execute_all(request_size, print_comments_each=True)

    @print_response_error
    def _execute_each(self, request_size, start_cursor=None):
        response = self.notion.databases.query(
            **self.unpack(page_size=request_size, start_cursor=start_cursor)
        )
        return response

    def print_comments(self):
        target_url = page_id_to_url(self.target_id)
        if self.target_name:
            form = [f"{self.target_name}", target_url]
        else:
            form = ['query', target_url]
        comments = '  '.join(form)
        stopwatch(comments)
