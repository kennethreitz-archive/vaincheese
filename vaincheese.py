# -*- coding: utf-8 -*-

import json

from flask import Flask
from flaskext.cache import Cache

from vanity import downloads_total


app = Flask(__name__)
cache = Cache(app)


@app.route('/')
def index():
    d = {
        'routes': {
            '/:package': 'Given package\'s download stats.'
        }
    }
    return json.dumps(d)


@app.route('/<package>')
@cache.cached(timeout=6*60*60)   # Six hours.
def package_stats(package):

    downs = downloads_total(package)

    d = {
        'package': package,
        'downloads': downs
    }

    return json.dumps(d)


if __name__ == '__main__':
    app.run()