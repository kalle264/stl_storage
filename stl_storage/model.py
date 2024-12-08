import os
from dataclasses import dataclass, field
from pathlib import Path

from nicegui import app, ui


@dataclass
class ModelData:
    id_: str
    name: str
    description: str
    stl_paths: dict[Path, str] = field(default_factory=dict)
    thumbnail_paths: dict[Path, str] = field(default_factory=dict)
    image_paths: dict[Path, str] = field(default_factory=dict)


    @staticmethod
    def from_directory(model_path: Path) -> 'ModelData':
        stl_path = model_path / 'files'
        stl_paths = {stl_path / filename: f'/model/{model_path.name}/files/{filename}' for filename in os.listdir(stl_path) if filename.endswith('.stl')}
        thumbnail_path = model_path / 'thumbnails'
        thumbnail_paths = {thumbnail_path / filename: f'/model/{model_path.name}/thumbnails/{filename}' for filename in os.listdir(thumbnail_path)}
        image_path = model_path / 'images'
        image_paths = {image_path / filename: f'/model/{model_path.name}/images/{filename}' for filename in os.listdir(image_path)}
        description = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'
        return ModelData(id_=model_path.name, name='test_name', description=description, stl_paths=stl_paths, thumbnail_paths=thumbnail_paths, image_paths=image_paths)


class Model:
    def __init__(self, data: ModelData):
        self._data = data
        self._load_files()

    @property
    def id_(self) -> str:
        return self._data.id_

    def _load_files(self) -> None:
        for stl_path, stl_url in self._data.stl_paths.items():
            app.add_media_file(local_file=stl_path.as_posix(), url_path=stl_url)
        for thumbnail_path, thumbnail_url in self._data.thumbnail_paths.items():
            app.add_media_file(local_file=thumbnail_path.as_posix(), url_path=thumbnail_url)
        for image_path, image_url in self._data.image_paths.items():
            app.add_media_file(local_file=image_path.as_posix(), url_path=image_url)

    def ui_detailed(self) -> None:
        with ui.column().classes('w-1/2 m-auto'):
            with ui.card().tight().classes('w-full justify-center'):
                with ui.row().classes('w-full p-4'):
                    ui.button(icon='arrow_back', on_click=ui.navigate.back)
                    ui.label(self._data.id_).classes('m-auto font-bold text-xl')
                    ui.space()
                    ui.button('Download', on_click=lambda: ui.notify('TODO: download'))
                ui.image(self.title_image_url).classes('mx-0')
                ui.label(self._data.description).classes('mx-4 my-2')

            with ui.card().tight().classes('w-full'):
                # TODO: description label text changes when expanded
                with ui.expansion('Files', icon='folder').classes('w-full m-0'):
                    with ui.column().classes('w-full'):
                        for stl_path, stl_url in self._data.stl_paths.items():
                            with ui.row(wrap=False).classes('w-full border rounded-lg p-2'):
                                # TODO: image url
                                ui.image(self.title_image_url).classes('h-16 w-auto aspect-square')
                                with ui.column().classes('w-full'):
                                    ui.label(stl_path.name).classes('pt-2')
                                    size = 8
                                    ui.label(f'Size: {size}mb').classes('text-xs')
                                ui.space()
                                ui.button(icon='download', on_click=lambda link=stl_url: ui.download(link)).classes('m-auto')
            # with ui.scene().classes('w-full h-64') as scene:
            #     stl_url = next(iter(self._data.stl_paths.values()))
            #     # TODO: center the model
            #     scene.stl(stl_url)

    def ui_list(self) -> None:
        with ui.link(target=self.url).classes('no-underline text-inherit'):
            with ui.card().tight().classes('w-60 m-auto'):
                ui.image(self.title_image_url).classes('aspect-square')
                with ui.row().classes('w-full h-12'):
                    ui.label(self._data.name).classes('text-lg m-auto')
    @property
    def url(self) -> str:
        return f'/model/{self._data.id_}'

    @property
    def title_image_url(self) -> str:
        if len(self._data.image_paths) > 0:
            return next(iter(self._data.image_paths.values()))
        return next(iter(self._data.thumbnail_paths.values()))
