#!/srv/http/michalwalczak.eu/wasabicalc/venv/bin/python3
from flup.server.fcgi import WSGIServer
from wasabicalcweb import server

if __name__ == '__main__':
    WSGIServer(server).run()
