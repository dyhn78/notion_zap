from ..structure import Requestor
from ..parse import PageParser
from ..read import RetrievePage
from ..write import UpdateBasicPage, BasicPagePropertyStash, \
    AppendBlockChildren, UpdateTabularPage


class BasicPage(Requestor):
    def __init__(self, parsed_page: PageParser, parent_id=''):
        self.page_id = parsed_page.page_id
        self.title = parsed_page.title
        if parent_id:
            self.parent_id = parent_id
        else:
            self.parent_id = parsed_page.parent_id

        self._update_props = UpdateBasicPage(parsed_page.page_id)
        self.props: BasicPagePropertyStash = self._update_props.props
        self.props.fetch(parsed_page.props)

        self._append_blocks = AppendBlockChildren(self.page_id)
        self.children = self._append_blocks.children

    @classmethod
    def from_direct_retrieve(cls, page_id):
        response = RetrievePage(page_id).execute()
        parsed_page = PageParser.from_retrieve_response(response)
        return cls(parsed_page)

    def apply(self):
        return [self._update_props.apply(), self._append_blocks.apply()]

    def execute(self):
        return [self._update_props.execute(), self._append_blocks.execute()]


class TabularPage(BasicPage):
    def __init__(self, parsed_page: PageParser, parent_id=''):
        super().__init__(parsed_page, parent_id=parent_id)
        self._update_props = UpdateTabularPage(self.page_id)
        self.props = self._update_props.props
        self.props.fetch(parsed_page.props)

    @classmethod
    def from_direct_retrieve(cls, page_id):
        response = RetrievePage(page_id).execute()
        parsed_page = PageParser.from_retrieve_response(response)
        return cls(parsed_page)