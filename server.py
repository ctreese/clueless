import json
import logging
import uuid
from wsgiref import simple_server

import falcon
import requests


class Gamestate(object):

    #placeholder
    def get_gamestate():
        return True

class RegisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, user_id):
        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200

class DeregisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200

class TurnResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200

class OptionsResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200

class LegalityResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200

class MoveResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_201

class initResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)


    def on_post(self, req, resp):
        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_201


# Configure your WSGI server to load "things.app" (app is a WSGI callable)
app = falcon.API()

gs = gamestate()

register = RegisterResource(gs)
deregister = DeregisterResource(gs)
turn = TurnResource(gs)
gameOptions = OptionsResource(gs)
legality = LegalityResource(gs)
move = MoveResource(gs)
gameInit = initResource(gs)

app.add_route('/register', register)
app.add_route('/deregister/{player_id}', deregister)
app.add_route('/turn/{player_id}', turn)
app.add_route('/options/{player_id}', gameOptions)
app.add_route('/legality//{player_id}/{move}', legality)
app.add_route('/move/{player_id}', things)
app.add_route('/init', gameInit)

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()