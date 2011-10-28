# -*- coding: utf-8 -*-

import os
from urlparse import urlparse

from flask import Flask, jsonify
from flaskext.cache import Cache

from vanity import downloads_total


app = Flask(__name__)

# Support Heroku's Redis environment.
p = urlparse(os.environ.get('REDISTOGO_URL', ''))

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] =  p.hostname or 'localhost'
app.config['CACHE_REDIS_PORT'] = p.port or 6379
app.config['CACHE_REDIS_PASSWORD'] = p.password or None

cache = Cache(app)


@app.route('/')
def index():
    d = {
        'routes': {
            '/pypi/:package': 'Given package\'s download stats.'
        }
    }
    return jsonify(d)


@app.route('/pypi/<package>')
@cache.memoize(timeout=6*60*60)
def package_stats(package):

    d = {
        'package': package,
        'downloads': downloads_total(package)
    }

    return jsonify(d)


if __name__ == '__main__':
    app.run()