from flask import Flask
from mako.lookup import TemplateLookup
import pkg_resources
import os

module_path = os.path.join(pkg_resources.get_distribution('petersen').location, 'petersen')

app = Flask("petersen.app")
app.config['db_url'] = 'sqlite:///dev.db'
app.secret_key = 'TRMISAVATARAANGCONFIRMED'  # TODO Move to env var and use an actual random string

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
    with open(os.path.join(module_path, 'assets', *path)) as f:
        return f.read()