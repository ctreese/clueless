import json
import logging
from wsgiref import simple_server
import random

import falcon


class Gamestate(object):

    playerList = []
    avaliableCharacters = ["Miss-Scarlet", "Professor-Plum", "Mrs-Peacock", "Mr-Green", "Mrs-While", "Colonel-Mustard"]

    def get_playerlist(self):
        return self.playerList

    def add_player(self, playerName):
        if playerName in self.avaliableCharacters:
            self.playerList.append(playerName)
            self.avaliableCharacters.remove(playerName)

    def remove_player(self, playerName):
        if playerName in self.playerList:
            self.playerList.remove(playerName)
            self.avaliableCharacters.append(playerName)

    #placeholder
    def get_gamestate(self):
        return True


class RegisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        player = random.choice(self.gs.avaliableCharacters)
        self.gs.add_player(player)
        resp.set_header('Powered-By', 'Falcon')
        print(player)
        resp.body = json.dumps({ 'playername': player });
        resp.status = falcon.HTTP_200

class DeregisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        self.gs.remove_player(player_id)
        resp.set_header('Powered-By', 'Falcon')
        resp.body = '{}'
        resp.status = falcon.HTTP_200


class TurnResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        if(player_id not in self.gs.get_playerlist()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently registered"
            )
        player_turn = random.choice(self.gs.avaliableCharacters)
        resp.body = json.dumps(self.gs.get_playerlist())
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'playerturn': player_turn });
        resp.status = falcon.HTTP_200

class OptionsResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        if(player_id not in self.gs.get_playerlist()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently registered"
            )
        options = "1. Move 2. Make Suggestion 3. Make Accusation"
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'move_options' : options });
        resp.status = falcon.HTTP_200

class LegalityResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id, move):
        if(player_id not in self.gs.get_playerlist()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently registered"
            )
        resp.set_header('Powered-By', 'Falcon')
        resp.body = '{}'
        resp.status = falcon.HTTP_200

class MoveResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp, player_id):
        if(player_id not in self.gs.get_playerlist()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently registered"
            )
        random_move = " moved from room to hallway."
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'move' : random_move });
        resp.status = falcon.HTTP_201

class initResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)


    def on_post(self, req, resp):
        resp.set_header('Powered-By', 'Falcon')
        #resp.body = '{}'
        character_list = ''
        for character in self.gs.avaliableCharacters:
            character_list = character_list + ' ' + character
        resp.body = json.dumps({ 'info' : character_list });
        resp.status = falcon.HTTP_201

class CORSComponent(object):
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')

        if (req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
        ):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))


# Configure your WSGI server to load "things.app" (app is a WSGI callable)
app = falcon.API(middleware=[CORSComponent()])

gs = Gamestate()

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
app.add_route('/legality/{player_id}/{move}', legality)
app.add_route('/move/{player_id}', move)
app.add_route('/init', gameInit)

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
