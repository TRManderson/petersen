from flask import Flask
from mako.lookup import TemplateLookup
import pkg_resources
import os

app = Flask("petersen.app")

template_lookup = TemplateLookup([
    os.path.join(pkg_resources.get_distribution('petersen').location, 'petersen', 'templates')
])

@app.route('/')
@app.route('/index.html')
def index():
    return template_lookup.get_template('index.mako').render(config=app.config)