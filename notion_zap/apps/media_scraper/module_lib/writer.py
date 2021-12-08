from typing import Union

from notion_zap.apps.media_scraper.structs.controller_base_logic import ReadingPageWriter


class LibraryDataWriter:
    def __init__(self, status: ReadingPageWriter):
        self.status = status
        self.page = status.page
        self.book_names = status.book_names

    def set_lib_data(self, data: dict, first_lib: str):
        datastrings = []
        first_data = data.pop(first_lib)
        string, available = self._cleaned_data(first_data)
        datastrings.append(string)
        datastrings.extend([self._cleaned_data(data)[0]
                            for lib, data in data.items()])
        joined_string = '; '.join(datastrings)

        writer = self.page.props
        writer.write_text(tag='location', value=joined_string)
        property_writer = self.page.props
        value = not available
        property_writer.write_checkbox(tag='not_available', value=value)

    @staticmethod
    def _cleaned_data(res: Union[dict, str]) -> tuple[str, bool]:
        if type(res) == dict:
            string = f"{res['lib_name']}"
            if book_code := res['book_code']:
                string += f" {book_code}"
            available = res['available']
            return string, available
        elif type(res) == str:
            available = not ('불가능' not in res)
            return res, available