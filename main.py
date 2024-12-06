#!/usr/bin/env python3
import os

from dotenv import load_dotenv
from nicegui import app, ui


load_dotenv('.env')

def startup() -> None:
    @ui.page('/')
    def page() -> None:
        ui.label('Hello World')

app.on_startup(startup)
ui.run(title='STL Storage', port=80)