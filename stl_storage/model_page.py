
from nicegui import ui

from .model import Model
from .model_database import ModelDatabase


class ModelPage:
    def __init__(self, model_database: ModelDatabase):
        self.model_database = model_database

        @ui.page('/model/{model_id}')
        def page(model_id: str) -> None:
            ui.page_title(model_id)
            model = self.model_database.get_model(model_id)
            if model is None:
                # TODO: 404 page
                ui.label('Model not found')
                return
            assert isinstance(model, Model)
            model.ui_detailed()
