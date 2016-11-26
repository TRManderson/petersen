from flask import Flask
from mako.lookup import TemplateLookup
import pkg_resources
import os

module_path = os.path.join(pkg_resources.get_distribution('petersen').location, 'petersen')

app = Flask("petersen.app", static_folder=os.path.join(module_path, 'static'))

template_lookup = TemplateLookup([
    os.path.join(pkg_resources.get_distribution('petersen').location, 'petersen', 'templates')
])

@app.route('/')
@app.route('/index.html')
def index():
    return template_lookup.get_template('index.mako').render(config=app.config)