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
        'resources': {
            '/pypi/:package': 'Given package\'s download stats.'
        },
        'source': 'https://github.com/kennethreitz/vaincheese'
    }
    return jsonify(d)


def total_downloads(package):
    count = downloads_total(package)
    package = package.swapcase() if package.isupper() else package
    while not count:
        for pos, value in enumerate(package):
            temp_package = package[:pos].swapcase() + package[pos:]
            count = downloads_total(temp_package)
            if count:
                return count
        else:
            return count
        
@app.route('/pypi/<package>')
@cache.memoize(timeout=6*60*60)
def package_stats(package):

    d = {
        'package': package,
        'downloads': total_downloads(package)
    }

    return jsonify(d)


if __name__ == '__main__':
    app.run()
