from abc import ABCMeta, abstractmethod

from notion_py.interface.common.struct import Requestor
from .master_logic import BlockEditor


class ListEditor(BlockEditor, metaclass=ABCMeta):
    def __init__(self, caller: BlockEditor):
        super().__init__(caller)

    @property
    @abstractmethod
    def blocks(self):
        """must return list of MasterEditor"""
        pass

    def save(self):
        return [child.save() for child in self.blocks]

    def save_info(self):
        return [child.save_info() for child in self.blocks]

    def save_required(self):
        return any([child for child in self.blocks])

    def __iter__(self):
        return iter(self.blocks)

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, index: int):
        return self.blocks[index]


class GroundEditor(BlockEditor, metaclass=ABCMeta):
    def __init__(self, caller: BlockEditor):
        super().__init__(caller)
        self.enable_overwrite = True

    @property
    @abstractmethod
    def requestor(self) -> Requestor:
        pass

    def save_info(self):
        return self.requestor.encode()

    def save(self):
        return self.requestor.execute()

    def save_required(self):
        return self.requestor.__bool__()


class AdaptiveEditor(BlockEditor, metaclass=ABCMeta):
    def __init__(self, caller: BlockEditor):
        super().__init__(caller)
        self.enable_overwrite = True

    @property
    @abstractmethod
    def value(self) -> BlockEditor:
        pass

    def save_info(self):
        return self.value.save_info()

    def save(self):
        return self.value.save()

    def save_required(self):
        return self.value.save_required()


"""
from itertools import chain
from typing import ValuesView, Mapping

class AbstractMasterEditor(Executable):
    def __init__(self, master_id: str):
        self.master_id = master_id
        self.set_overwrite_option(True)

    @abstractmethod
    def set_overwrite_option(self, option: bool):
        pass

class EditorComponentStash(dict):
    def __init__(self, caller: EditorControl):
        super().__init__()
        self.caller = caller

    def blocks(self) -> ValuesView[EditorComponent]:
        return super().blocks()

    def update(self, __m: Mapping[str, EditorComponent],
               **kwargs: dict[str, EditorComponent]):
        super().update(__m, **kwargs)
        for key, value in chain(__m, kwargs):
            setattr(self.caller, key, value)


class StackEditor(AbstractMainEditor):
    def __init__(self, master_id: str):
        super().__init__(master_id)
        self.rows: list[MainEditor] = []

    def __iter__(self) -> list[MainEditor]:
        return self.rows

    def set_overwrite_option(self, option: bool):
        for child in self:
            child.set_overwrite_option(option)

    def unpack(self):
        return [child.unpack() for child in self]

    def execute(self):
        return [child.execute() for child in self]
"""
