#!/usr/bin/env python

from app import create_app

import gevent.monkey
gevent.monkey.patch_all()
application = create_app()

if __name__ == '__main__':
    print "== Running in debug mode =="
    application.run(host='localhost', port=8080, debug=True)
