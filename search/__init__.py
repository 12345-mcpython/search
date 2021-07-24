from flask import Flask

# from search.crawler.crawler_manager import spider_console
from search.config.config import config
from search.views import index


def create_app(config_name):
    app = Flask(__name__)
    app.register_blueprint(index.a)
    app.config.from_object(config[config_name])
    return app
