#!/usr/bin/python3
from flup.server.fcgi import WSGIServer
from wasabicalc-web import app

if __name__ == '__main__':
    WSGIServer(app).run()
