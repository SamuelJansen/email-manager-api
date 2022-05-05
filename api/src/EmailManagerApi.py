from flask import render_template

from python_framework import ResourceManager
from queue_manager_api import QueueManager
import ModelAssociation


app = ResourceManager.initialize(__name__, ModelAssociation.MODEL, managerList=[
    QueueManager()
])


# @app.route(f'{app.api.baseUrl}')
# def home():
#     return render_template('index.html', staticUrl=ResourceManager.getApiStaticUrl(app))
