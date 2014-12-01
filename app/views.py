"""
Views module

It contains the views needed by Angularjs to load the templates.
"""
from app import app
from flask import send_file, abort


@app.route('/')
def index():
    """
    Send the base template loading the js app.
    """
    return send_file('templates/base.html')


@app.route('/<page>.html')
def send_template(page):
    """
    Send templates dynamically
    """
    try:
        return send_file('templates/{}.html'.format(page))
    except IOError:
        abort(404)
