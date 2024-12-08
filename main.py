#!/usr/bin/env python3
import os

from dotenv import load_dotenv
from nicegui import app, ui

from stl_storage import ModelDatabase
from stl_storage.main_page import MainPage as main_page
from stl_storage.model_page import ModelPage as model_page

load_dotenv('.env')
data_dir = os.getenv('DATA_DIR')
assert data_dir is not None, 'DATA_DIR is not set'
port_str = os.getenv('PORT')
assert port_str is not None, 'PORT is not set'
port = int(port_str)
assert isinstance(port, int)

def startup() -> None:
    assert data_dir is not None
    model_database = ModelDatabase(data_dir)
    model_database.load_models()
    main_page(model_database)
    model_page(model_database)

app.on_startup(startup)
ui.run(title='STL Storage', port=port, on_air=os.getenv('ON_AIR', None), dark=False)
