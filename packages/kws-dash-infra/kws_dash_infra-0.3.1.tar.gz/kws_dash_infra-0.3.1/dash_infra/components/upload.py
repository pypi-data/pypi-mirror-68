import base64
import io
import os

import pandas as pd
from dash_bootstrap_components import Alert
from dash_core_components import Upload
from dash_html_components import Div
from dash_infra import ComponentGroup, as_callback, as_component
from dash_infra.components.storage import ContextStorage, PickleStorage


class FileInput(ComponentGroup):
    def __init__(self, id, *parsers, store=None, alert=None, **kwargs):
        # fmt: off
        self.id = id
        # components
        self.store = store or ContextStorage(f"{id}-store")
        self.input = as_component(
            Upload, 
            id=id, 
            children=Div("Select a file", className="col s12"),
            className="file-input row",
        )

        # fmt: on
        self.alert = alert or as_component(
            Alert,
            id=f"alert-{id}",
            color="success",
            children="hello",
            dismissable=True,
            duration=2000,
            is_open=False,
        )
        # fmt: off
        #callbacks
        self.parse_to_store = (
            as_callback(
                inputs=(id, "contents"), 
                states=[(id, "filename"), (id, "last_modified")],
            )(self._parse_to_store)
                .to(self.store)
        )

        self.show_alert = as_callback(
            inputs=[(self.store.id, f"trigger-{id}-container")], 
            outputs=[(self.alert.id, "children"), (self.alert.id, "is_open")],
            states=[(id, "filename")]
        )(self._show_alert)

        # fmt: on
        self.parsers = parsers

        if store:
            if alert:
                super().__init__(f"{id}-container", self.input, **kwargs)
            else:
                super().__init__(f"{id}-container", self.alert, self.input, **kwargs)
        else:
            if alert:
                super().__init__(f"{id}-container", self.input, self.store, **kwargs)
            else:
                super().__init__(
                    f"{id}-container", self.alert, self.input, self.store, **kwargs
                )

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

    def _show_alert(self, _, filename):
        if not filename:
            return "", False
        return f"{filename} uploaded", True


class DataFrameParsers(object):
    @staticmethod
    def csv(contents):
        return pd.read_csv(io.StringIO(contents.decode()), sep=";")

    @staticmethod
    def xls(contents):
        return pd.read_excel(io.BytesIO(contents))
