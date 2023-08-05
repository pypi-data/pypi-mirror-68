from dash_infra.core import Component
from dash_infra.html_helpers.divs import Row


class ComponentGroup(Component):
    def __init__(self, id, *components, container=Row):
        super().__init__(id)
        self.components = components
        self.container = container

    def layout(self):
        return self.container([c.layout() for c in self.components], id=self.id)
