
from nicegui import ui

from .model_database import ModelDatabase


class MainPage:
    def __init__(self, model_database: ModelDatabase):
        self.model_database = model_database

        @ui.page('/')
        def page() -> None:
            self.ui()

    def ui(self) -> None:
        with ui.row().classes('w-10/12 m-auto'):
            ui.label('STL Storage').classes('font-bold text-xl')

        with ui.row().classes('w-10/12 m-auto text-sm'):
            ui.label('Filters').classes('my-auto mr-6')
            ui.input(label='Search').classes('w-96 mr-6')
            ui.select(options=['Creator 1', 'Creator 2', 'Creator 3'], clearable=True, with_input=True, label='Creator').classes('w-40 mr-6')
            ui.select(options=['Collection 1', 'Collection 2', 'Collection 3'], clearable=True, with_input=True, label='Collection').classes('w-40')
            ui.space()
            ui.button('Add Model', icon='add', on_click=lambda: ui.notify('TODO: add model'))

        with ui.row().classes('w-11/12 m-auto justify-center'):
            for model in self.model_database.models:
                model.ui_list()
