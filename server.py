import json
import logging
from wsgiref import simple_server
import random

import falcon

from game_logic import *


class Game(object):


    def __init__(self):
        #TODO: get this done
        def player_init_phase():
            return

        self.cards = cardInitialization()
        self.rooms = roomInitialization()
        self.hallways = hallwayInitialization(self.rooms)
        self.avaliableCharacters = playerInitialization(self.hallways)

        self.playerList = []
        self.turn_number = 0
        self.game_over_flag = 0

        self.has_started = False

    def find_player(player_name):
        found = next((player for player in test_list if player.name == player_name), None)
        if not found:
            raise Exception('Player not found')

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

    def performSuggestion(board, player):
        #TODO
        response = 0
        suspects = []
        while response < 1 or response >= numPlayers:
            i = 1
            print("The following players are suspects: ")
            for suspect in board.players:
                 if suspect.name != player.name:
                     suspects.append(suspect)
                     print("", i, ". " + suspect.name)
                     i += 1
            response = int(input("Please select a suspect (using numbers):"))
        suspectName = suspects[response-1].name
        suggestedPlayer = suspects[response-1]
        #print("You selected: " + suspectName)

        response = 0
        while response < 1 or response > 6:
            print("1. Candlestick")
            print("2. Dagger")
            print("3. Lead Pipe")
            print("4. Revolver")
            print("5. Rope")
            print("6. Wrench")
            response = int(input("Please select a weapon (using numbers):"))
            #print(type(response))
            #print("The response is: ", response)
        weaponName = ""
        if response == 1:
            weaponName = "CandleStick"
        elif response == 2:
            weaponName = "Dagger"
        elif response == 3:
            weaponName = "Lead Pipe"
        elif response == 4:
            weaponName = "Revolver"
        elif response == 5:
            weaponName = "Rope"
        elif response == 6:
            weaponName = "Wrench"

        suggestedPlayer.location = player.location #moves suggested player into room
        suggestionResponse(board, suspectName, player.location.name, weaponName)

    def suggestionResponse(board, suspectName, locationName, weaponName):
        for player in board.players:
            for card in player.hand:
                if card.name == suspectName or card.name == locationName or card.name == weaponName:
                    print(player.name + " has disproved the suggestion!")
                    return
        print("No one could disprove the suggestion!")
        return


    def performAccusation(board, player):
        #TODO
        response = 0
        suspects = []
        while response < 1 or response >= numPlayers:
            i = 1
            print("The following players are suspects: ")
            for suspect in board.players:
                 if suspect.name != player.name:
                     suspects.append(suspect)
                     print("", i, ". " + suspect.name)
                     i += 1
            response = int(input("Please select a suspect (using numbers):"))
        suspectName = suspects[response-1].name
        #print("You selected: " + suspectName)
        response = 0
        while response < 1 or response > len(board.rooms):
            i = 1
            for room in board.rooms:
                print("", i, ". " + room.name)
                i += 1
            response = int(input("Please select a room (using numbers):"))
        roomName = board.rooms[response-1].name
        #print("You selected: " + roomName)
        response = 0
        while response < 1 or response > 6:
            print("1. Candlestick")
            print("2. Dagger")
            print("3. Lead Pipe")
            print("4. Revolver")
            print("5. Rope")
            print("6. Wrench")
            response = int(input("Please select a weapon (using numbers):"))
            #print(type(response))
            #print("The response is: ", response)
        weaponName = ""
        if response == 1:
            weaponName = "CandleStick"
        elif response == 2:
            weaponName = "Dagger"
        elif response == 3:
            weaponName = "Lead Pipe"
        elif response == 4:
            weaponName = "Revolver"
        elif response == 5:
            weaponName = "Rope"
        elif response == 6:
            weaponName = "Wrench"

        #print("You have selected the following: ")
        print(player.name + "made the following accusation!")
        print("Suspect: " + suspectName)
        print("Room: " + roomName)
        print("Weapon: " + weaponName)

        if board.caseFile.suspect.name == suspectName and board.caseFile.room.name == roomName and board.caseFile.weapon.name == weaponName:

            print("")
            print("*****************************************")
            print(player.name + " has won the game!")
            print("*****************************************")
            print("")
            print("The suspect was: " + board.caseFile.suspect.name)
            print("The room was: " + board.caseFile.room.name)
            print("The weapon was: " + board.caseFile.weapon.name)
            global game_over_flag
            game_over_flag = 1
        else:
            print(player.name + "'s accusation was wrong!")
            player.accusation_made = True

class RegisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        player = random.choice(self.gs.avaliableCharacters)
        self.gs.add_player(player)
        resp.set_header('Powered-By', 'Falcon')
        print(player.name)
        resp.body = json.dumps({ 'player_name': player.name });
        resp.status = falcon.HTTP_200


class StartResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        def gameInitialization(self, req, resp):
            resp.set_header('Powered-By', 'Falcon')
            resp.body = json.dumps({ 'started': "Game has started" });
            resp.status = falcon.HTTP_200
            self.gs.deck = Deck(self.gs.playerList,self.cards)
            self.gs.caseFile = deck.deal()
            self.board = Board(self.rooms, self.hallways, self.caseFile)

        def gameStartOutput(self, req, resp):
            print("You are playing as: " + self.gs.playerList[-1].name)
            print(self.gs.playerList[-1].name + " is starting in the hallway between the " + self.gs.playerList[-1].location.adj_room[0].name + " and the " + self.gs.playerList[-1].location.adj_room[1].name)
            print("The case file contains the following cards: " + self.gs.caseFile.suspect.name + ", " + self.gs.caseFile.weapon.name + ", " + self.gs.caseFile.room.name)
            print("The number of players in the game is: ", len(self.gs.playerList()))
            print("The cards in your hand are: ")
            for card in self.gs.playerList[-1].hand:
                print(card.name)

        if not self.gs.has_started:
            self.gameInitialization(req, resp)
            self.gameStartOutput(req, resp)
            self.gs.has_started = True
        else:
            self.gameStartOutput(req, resp)

class MoveResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp, player_id, move_number):
        # TODO add move number legality check
        # TODO add player turn legality check

        current_turn_number = self.gs.turn_number
        num_players = len(self.gs.playerList)
        current_player_name = self.gs.playerList[self.gs.turn_number % num_players].name

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

            if gs.game_over_flag == 0:
                resp.set_header('Powered-By', 'Falcon')
                resp.body = json.dumps({ 'move' : "game is over" });
                resp.status = falcon.HTTP_201
            else:
                current_player = self.gs.find_player(current_player_name)
                performTurn(self.gs.board, current_player, move_number)

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
move = MoveResource(gs)
start = StartResource(gs)

### TODO: Add option select resource

app.add_route('/register', register)
app.add_route('/move', move)
app.add_route('/start', start)

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
