# -*- coding: utf-8 -*-

import os
import json
from urlparse import urlparse

from flask import Flask
from flaskext.cache import Cache

from vanity import downloads_total


app = Flask(__name__)

p = urlparse(os.environ.get('REDISTOGO_URL', ''))

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] =  p.hostname or 'localhost'
app.config['CACHE_REDIS_PORT'] = p.port or 6379
app.config['CACHE_REDIS_PASSWORD'] = p.password or None

app.debug = True

cache = Cache(app)
# r = cache.cache._client.connection_pool
# r.password = p.password

# Support Heroku's Redis environment.



@app.route('/')
def index():
    d = {
        'routes': {
            '/:package': 'Given package\'s download stats.'
        }
    }
    return json.dumps(d)


@app.route('/<package>')
@cache.memoize(timeout=6*60*60)
def package_stats(package):

    d = {
        'package': package,
        'downloads': downloads_total(package)
    }

    return json.dumps(d)


if __name__ == '__main__':
    app.run()