from flask import Flask
from mako.lookup import TemplateLookup
import pkg_resources
import os
from jsmin import jsmin

module_path = os.path.join(pkg_resources.get_distribution('petersen').location, 'petersen')

app = Flask("petersen.app")
app.config['db_url'] = 'sqlite:///:memory:'

template_lookup = TemplateLookup([
    os.path.join(pkg_resources.get_distribution('petersen').location, 'petersen', 'templates')
])

@app.route('/')
@app.route('/index.html')
def index():
    return template_lookup.get_template('index.mako').render(config=app.config)

@app.route('/assets/<path:path>')
def static_files(path):
    path = path.split('/')
    if path[0] == 'js':
        with open(os.path.join(module_path, 'assets', *path)) as f:
            return jsmin(f.read())
    else:
        with open(os.path.join(module_path, 'assets', *path)) as f:
            return f.read()