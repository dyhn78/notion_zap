from enum import Enum

from notion_zap.cli.utility.page_id_to_url import url_to_id
from notion_zap.apps.helpers.emoji_code import EmojiCode


class MyBlock(Enum):
    def __new__(cls, title: str, id_or_url: str, prefix: str):
        obj = object.__new__(cls)
        obj._value_ = title
        obj.title = title
        obj.block_id = url_to_id(id_or_url)
        obj.prefix = prefix
        return obj

    @property
    def prefix_title(self):
        return self.prefix + self.title

    events = ('일과', 'c226cffe6cf84ab996bbc384bf26bf1d', EmojiCode.GLOBE_ASIA)
    journals = ('진행', 'c8d46c01d6c941a9bf8df5d115a05f03', EmojiCode.PURPLE_CIRCLE)
    notes = ('전개', '069bbebd632f4a6ea3044575a064cf0f', EmojiCode.PURPLE_HEART)

    issues = ('꼭지', 'e8782fe4e1a34c9d846d57b01a370327', EmojiCode.BLUE_CIRCLE)
    targets = ('체계', 'fa7d93f6fbd341f089b185745c834811', EmojiCode.BLUE_HEART)

    projects = ('주제', '69b4e661c4ee43b6a5e40c8b28e6f9d1', EmojiCode.ORANGE_CIRCLE)
    domains = ('분야', 'eca1ba6d4831459ca8becc283f1f8c4e', EmojiCode.ORANGE_HEART)
    channels = ('채널', '2d3f4ea770854b8e9e30abecd4d31a86', EmojiCode.ORANGE_DIAMOND)

    readings = ('읽기', 'c326f77425a0446a8aa309478767c85b', EmojiCode.YELLOW_CIRCLE)
    points = ('요점', '2c5411ba6a0f43a0a8aa06295751e37a', EmojiCode.YELLOW_HEART)

    streams = ('활동', 'eb2f09a1de41412e8b2357bc04f26e74', EmojiCode.RED_CIRCLE)
    groups = ('갈래', '679c2515870d46e3a107b42cd2a5ffc3', EmojiCode.RED_HEART)

    people = ('인물', '3c08cdba5a044e9c9b7e31ee8509f506', EmojiCode.BROWN_CIRCLE)
    locations = ('장소', '920e2e10225d450d8bb084697f6d0fc6', EmojiCode.BROWN_HEART)

    weeks = ('주간', 'd020b399cf5947a59d11a0b9e0ea45d0', EmojiCode.GREEN_CIRCLE)
    dates = ('일간', '961d1ca0a3d24a46b838ba85e710f18d', EmojiCode.GREEN_HEART)


if __name__ == '__main__':
    # for testing
    from notion_zap.cli.utility.page_id_to_url import id_to_url

    print(id_to_url(MyBlock.events.block_id))
