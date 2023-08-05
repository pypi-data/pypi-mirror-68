import base64
import io
import os

from dash_html_components import Div
from dash_core_components import Upload
import pandas as pd

from dash_infra import ComponentGroup, as_callback, as_component
from dash_infra.components.storage import ContextStorage, PickleStorage


class FileInput(ComponentGroup):
    def __init__(self, id, *parsers, store=None, **kwargs):
        self.id = id
        self.store = store or ContextStorage(f"{id}-store")
        self.parse_to_store = as_callback(
            inputs=(id, "contents"), states=[(id, "filename"), (id, "last_modified")],
        )(self._parse_to_store).to(self.store)
        self.input = as_component(
            Upload, id=id, children=Div("Select a file"), className="file-input row",
        )
        self.parsers = parsers
        if store:
            super().__init__(f"{id}-container", self.input)
        else:
            super().__init__(f"{id}-container", self.input, self.store, container=Div)

        self.parse_to_store.func.__name__ = self.id

    def _parse_to_store(self, contents, filename, _):
        if not contents:
            return ""
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        extension = os.path.splitext(filename)[1].strip(".")
        for parser in self.parsers:
            func = getattr(parser, extension, None)
            if func:
                return func(decoded)

        return ""


class DataFrameParsers(object):
    @staticmethod
    def csv(contents):
        return pd.read_csv(io.StringIO(contents.decode()), sep=";")

    @staticmethod
    def xls(contents):
        return pd.read_excel(io.BytesIO(contents))
