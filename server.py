import json
import logging
from wsgiref import simple_server
import random

import falcon

from game_logic import *

class Game(object):


    def __init__():


        #TODO: get this done
        def player_init_phase():
            return

        self.cards = cardInitialization()
        self.rooms = roomInitialization()
        self.hallways = hallwayInitialization(rooms)
        self.avaliableCharacters = playerInitialization(hallways)
        self.rooms = roomHallwayInitilization(rooms, hallways)
        self.deck = Deck(players,cards)
        self.caseFile = deck.deal()
        self.board = Board(rooms, hallways, caseFile)
        self.playerList = []
        self.turn_number = 0
        self.game_over_flag = 0

        print("You are playing as: " + players[0].name)
        print(players[0].name + " is starting in the hallway between the " + players[0].location.adj_room[0].name + " and the " + players[0].location.adj_room[1].name)
        print("The case file contains the following cards: " + caseFile.suspect.name + ", " + caseFile.weapon.name + ", " + caseFile.room.name)
        print("The number of players in the game is: ", deck.numPlayers)
        print("The cards in your hand are: ")
        for card in players[0].hand:
            print(card.name)

    def get_playerlist(self):
        return self.playerList

    def add_player(self, playerName):
        if playerName in self.avaliableCharacters:
            self.playerList.append(playerName)
            self.avaliableCharacters = [player for player in self.avaliableCharacters if player.name!=playerName.name] # remove player via list comprehension

    def remove_player(self, playerName):
        if playerName in self.playerList:
            self.playerList = [player for player in self.playerList if player.name!=playerName.name] # remove player via list comprehension
            self.avaliableCharacters.append(playerName)

    def gameLoop():
       print("")
       print("*****************************************")
       print("**********GAME IS NOW STARTING!**********")
       print("*****************************************")
       print("")
       num_players = len(self.playerList)
       while self.game_over_flag != 1 and self.turn_number < 20:
           print("It is " + players[self.turn_number % num_players].name + "'s turn!")
           performTurn(players[self.turn_number % num_players], self.board)
           self.turn_number += 1

    #placeholder
    def get_gamestate(self):
        return True

# Urgent
class RegisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        player = random.choice(self.gs.avaliableCharacters)
        self.gs.add_player(player)
        resp.set_header('Powered-By', 'Falcon')
        print(player.name)
        resp.body = json.dumps({ 'playername': player.name });
        resp.status = falcon.HTTP_200

class StartResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'started': "Game has started" });
        resp.status = falcon.HTTP_200

# # TODO: FIX THIS LATER
# class DeregisterResource(object):
#
#     def __init__(self, db):
#         self.gs = gs
#         self.logger = logging.getLogger('thingsapp.' + __name__)
#
#     def on_get(self, req, resp, player_id):
#         self.gs.remove_player(player_id)
#         resp.set_header('Powered-By', 'Falcon')
#         resp.body = '{}'
#         resp.status = falcon.HTTP_200
#
# # TODO: FIX THIS LATER
# class TurnResource(object):
#
#     def __init__(self, db):
#         self.gs = gs
#         self.logger = logging.getLogger('thingsapp.' + __name__)
#
#     def on_get(self, req, resp, player_id):
#         if(player_id not in self.gs.get_playerlist()):
#             raise falcon.HTTPBadRequest(
#             "Invalid Player Name",
#             "That player name is not currently registered"
#             )
#         player_turn = random.choice(self.gs.avaliableCharacters)
#         resp.body = json.dumps(self.gs.get_playerlist())
#         resp.set_header('Powered-By', 'Falcon')
#         resp.body = json.dumps({ 'playerturn': player_turn });
#         resp.status = falcon.HTTP_200
#
# # TODO: FIX THIS LATER
# class OptionsResource(object):
#
#     def __init__(self, db):
#         self.gs = gs
#         self.logger = logging.getLogger('thingsapp.' + __name__)
#
#     def on_get(self, req, resp, player_id):
#         if(player_id not in self.gs.get_playerlist()):
#             raise falcon.HTTPBadRequest(
#             "Invalid Player Name",
#             "That player name is not currently registered"
#             )
#         options = "1. Move 2. Make Suggestion 3. Make Accusation"
#         resp.set_header('Powered-By', 'Falcon')
#         resp.body = json.dumps({ 'move_options' : options });
#         resp.status = falcon.HTTP_200
#
# # TODO: FIX THIS LATER
# class LegalityResource(object):
#
#     def __init__(self, db):
#         self.gs = gs
#         self.logger = logging.getLogger('thingsapp.' + __name__)
#
#     def on_get(self, req, resp, player_id, move):
#         if(player_id not in self.gs.get_playerlist()):
#             raise falcon.HTTPBadRequest(
#             "Invalid Player Name",
#             "That player name is not currently registered"
#             )
#         resp.set_header('Powered-By', 'Falcon')
#         resp.body = '{}'
#         resp.status = falcon.HTTP_200
#


class MoveResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp, player_id, move_number):
        # TODO add move number legality check
        # TODO add player turn legality check

        current_turn_number = gs.turn_number
        num_players = len(gs.playerList)
        current_player_name = gs.playerList[gs.turn_number % num_players]

        if(player_id not in gs.get_playerlist()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently registered"
            )


        elif(player_id is not current_player_name):
            raise falcon.HTTPBadRequest(
            "Invalid Move",
            "Your turn is not now"
            )
        else:
            # random_move = " moved from room to hallway."
            resp.set_header('Powered-By', 'Falcon')
            resp.body = json.dumps({ 'move' : move_number });
            resp.status = falcon.HTTP_201

            if gs.game_over_flag = 0:
                resp.set_header('Powered-By', 'Falcon')
                resp.body = json.dumps({ 'move' : "game is over" });
                resp.status = falcon.HTTP_201
            else:
                performTurn(gs.playerList[gs.turn_number % num_players], gs.board)

class consoleOutput(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'message': "Game has started" });
        resp.status = falcon.HTTP_200

# # TODO: FIX THIS LATER
# class initResource(object):
#
#     def __init__(self, db):
#         self.gs = gs
#         self.logger = logging.getLogger('thingsapp.' + __name__)
#
#
#     def on_post(self, req, resp):
#         resp.set_header('Powered-By', 'Falcon')
#         #resp.body = '{}'
#         character_list = ''
#         for character in self.gs.avaliableCharacters:
#             character_list = character_list + ' ' + character
#         resp.body = json.dumps({ 'info' : character_list });
#         resp.status = falcon.HTTP_201

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

gs = Game()

register = RegisterResource(gs)
# deregister = DeregisterResource(gs)
# turn = TurnResource(gs)
# gameOptions = OptionsResource(gs)
# legality = LegalityResource(gs)
move = MoveResource(gs)
# gameInit = initResource(gs)

start = StartResource(gs)
console_output = consoleOutput(gs)

### TODO: Add option select resource

app.add_route('/register', register)
# app.add_route('/deregister/{player_id}', deregister)
# app.add_route('/turn/{player_id}', turn)
# app.add_route('/options/{player_id}', gameOptions)
# app.add_route('/legality/{player_id}/{move}', legality)
app.add_route('/move/{player_id}/{move_number}', move)
app.add_route('/start', start)
app.add_route('/consoleOutput', console_output)
# app.add_route('/init', gameInit)

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
