from .filter_maker import QueryFilterAgent
from .filter_unit import QueryFilter, PlainFilter
from .sort import QuerySort
from ...struct import LongGateway, PointEditor, PropertyFrame, print_response_error


class Query(LongGateway):
    def __init__(self, editor: PointEditor):
        super().__init__(editor)
        self._filter_value = PlainFilter({})
        self.sort = QuerySort()
        self.frame = editor.frame if hasattr(editor, 'frame') else PropertyFrame()
        self.make_filter = QueryFilterAgent(self)

    def __bool__(self):
        return True

    def unpack(self, page_size=None, start_cursor=None):
        args = dict(**self.sort.unpack(),
                    database_id=self.target_id,
                    page_size=page_size if page_size else self.MAX_PAGE_SIZE)
        if self._filter_value:
            args.update(filter=self._filter_value.unpack())
        if start_cursor:
            args.update(start_cursor=start_cursor)
        return args

    @print_response_error
    def _execute_once(self, page_size=None, start_cursor=None):
        response = self.notion.databases.query(
            **self.unpack(page_size=page_size, start_cursor=start_cursor)
        )
        return response

    def clear_filter(self):
        self._filter_value = PlainFilter({})

    def push_filter(self, query_filter: QueryFilter):
        if query_filter is not None:
            self._filter_value = query_filter
