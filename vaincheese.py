# -*- coding: utf-8 -*-

import os
import json
from urlparse import urlparse

from flask import Flask
from flaskext.cache import Cache

from vanity import downloads_total


app = Flask(__name__)
# app.config['CACHE_TYPE'] = 'redis'
# app.config['CACHE_REDIS_HOST'] = 'localhost'
# app.config['CACHE_REDIS_PORT'] = 6379

app.debug = True

cache = Cache(app)


# Support Heroku's Redis environment.
# if 'REDISTOGO_URL' in os.environ:
#     r = cache.cache._client.connection_pool
#     p = urlparse(os.environ['REDISTOGO_URL'])

#     r.host = p.host
#     r.port = p.port
#     r.password = p.password
#     r.username = p.username



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