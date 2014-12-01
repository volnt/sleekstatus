from app import app
from flask import request, send_file, abort


@app.route('/')
def index():
    return send_file('templates/base.html')


@app.route('/<page>.html')
def page(page):
    try:
        return send_file('templates/{}.html'.format(page))
    except IOError:
        abort(404)
