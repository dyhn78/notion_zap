from typing import Union

from notion_zap.apps.media_scraper.common.struct import ReadingPageChecker
from notion_zap.apps.media_scraper.module_lib.gy import GoyangLibraryAgent


class LibraryDataWriter:
    def __init__(self, checker: ReadingPageChecker, data: dict):
        self.checker = checker
        self.page = checker.page
        try:
            self.first_lib = self.prioritize_data(data)
            self.encode(data)
        except ValueError:
            self.checker.mark_as_lib_missing()

    def encode(self, data: dict):
        datastrings = []
        first_data = data.pop(self.first_lib)
        string, available = self._cleaned_data(first_data)
        datastrings.append(string)
        datastrings.extend([self._cleaned_data(data)[0]
                            for lib, data in data.items()])
        joined_string = '; '.join(datastrings)

        self.page.write_text(tag='location', value=joined_string)
        value = not available
        self.page.write_checkbox(tag='not_available', value=value)

    @staticmethod
    def prioritize_data(data: dict):
        if 'gy' in data.keys() and \
                data['gy']['lib_name'] == GoyangLibraryAgent.GAJWA_LIB:
            return 'gy'
        elif 'snu' in data.keys():
            return 'snu'
        elif 'gy' in data.keys():
            return 'gy'
        raise ValueError

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
