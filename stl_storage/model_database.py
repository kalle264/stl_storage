import os
from pathlib import Path

from .model import Model, ModelData


class ModelDatabase:
    def __init__(self, directory_path: str):
        self._directory = Path(directory_path)
        self._model_data: dict[str, ModelData] = {}

    def load_models(self) -> None:
        for model_id in os.listdir(self._directory):
            for i in range(20):
                model_path = self._directory / model_id
                if not model_path.is_dir():
                    continue
                new_model_id = model_id + '_' + str(i)
                model_data = ModelData.from_directory(model_path)
                model_data.id_ = new_model_id
                self._model_data[new_model_id] = model_data

    @property
    def models(self) -> list[Model]:
        return [model for model_id in self._model_data if (model := self.get_model(model_id)) is not None]

    def get_model(self, model_id: str) -> Model | None:
        if model_id not in self._model_data:
            return None
        return Model(self._model_data[model_id])
