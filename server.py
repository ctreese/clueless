import json
import logging
from wsgiref import simple_server
import random

import falcon

import game_logic


class Gamestate(object):

    playerList = []
    playerListActive = []
    avaliableCharacters = ["Miss-Scarlet", "Professor-Plum", "Mrs-Peacock", "Mr-Green", "Mrs-White", "Colonel-Mustard"]
    playerTurn = ""
    gameStarted = False

    cards = []
    rooms = []
    hallways =[]
    players = []
    deck = []
    caseFile = []
    board = []

    def get_activePlayers(self):
        return self.playerListActive

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

    def init_gamestate(self):
        self.playerListActive = self.playerList
        self.cards = game_logic.cardInitialization()
        self.rooms = game_logic.roomInitialization()
        self.hallways = game_logic.hallwayInitialization(self.rooms)
        self.players = game_logic.playerInitialization(self.hallways, self.playerListActive)
        self.deck = game_logic.Deck(self.players,self.cards)
        self.caseFile = self.deck.deal()
        self.board = game_logic.Board(self.rooms, self.hallways, self.caseFile)
        self.playerTurn = random.choice(self.playerListActive)
        self.gameStarted = True

    def nextTurn(self, player_id):
        idx = self.playerListActive.index(player_id)
        if(len(self.playerListActive)-1 == idx):
            #last item
            self.playerTurn = self.playerListActive[0]
        else:
            self.playerTurn = self.playerListActive[idx+1]
        #check to see if accusation has been made, if so skip turn
        if(self.players[self.playerTurn].accusation_made):
            self.nextTurn(self.playerTurn)

    def makeSuggestion(self, character, suspect, weapon, location):
        if suspect in self.playerListActive:
            for player in self.players.values():
                print(player, flush = True)
                if player.name == suspect:
                    player.location = location
                    player.suggested = True
        return game_logic.performSuggestion(suspect, weapon, location.name, self.players);

    def makeAccusation(self, player_id, character, weapon, location):
        gameWon = game_logic.performAccusation(self.board, self.players[player_id], character, weapon, location);
        if(gameWon):
            self.gameStarted = False
            return "You have won the game!"
        else:
            return "Sorry, that is incorrect."

#/register
#GET: Assigns the client a player, and adds that player to the next started game
#Each client should only call this method ONCE, and should remember its assigned player_id
class RegisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        player = random.choice(self.gs.avaliableCharacters)
        self.gs.add_player(player)
        resp.set_header('Powered-By', 'Falcon')
        print(player)
        resp.body = json.dumps({ 'player_name': player });
        resp.status = falcon.HTTP_200

#/deregister/{player_id}
#GET: Removes the given player_id from any subsequent games
#This method can be called multiple times, and should be called when a client disconnects from the game
class DeregisterResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        self.gs.remove_player(player_id)
        resp.set_header('Powered-By', 'Falcon')
        resp.body = '{}'
        resp.status = falcon.HTTP_200

#/turn/{player_id}
#GET: Returns what players turn it currently is
#This should be called periodically by the client, so that it knows when it is ready to receive player input
class TurnResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        if not self.gs.gameStarted:
            raise falcon.HTTPInternalServerError(
            "Game Not Started",
            "Please start the game before issuing commands"
            )
        if(player_id not in self.gs.get_activePlayers()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently playing"
            )
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'playerTurn': self.gs.playerTurn });
        resp.status = falcon.HTTP_200

#/options/{player_id}
#GET: returns legal moves, adjacent rooms, and the list of seen cards
#This should be called by the client after a call to the turn method indicates it is the players turn
class OptionsResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):

        if not self.gs.gameStarted:
            raise falcon.HTTPInternalServerError(
            "Game Not Started",
            "Please start the game before issuing commands"
            )
        if(player_id not in self.gs.get_activePlayers()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently playing"
            )
        options = self.gs.players[player_id].getLegalMoves()
        moveCandidates = []
        for index, position in enumerate(self.gs.players[player_id].location.adj_locs):
            moveCandidates.append({'destination': position.name, 'id': index})

        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'move_options' : options, 'adj' : moveCandidates});
        resp.status = falcon.HTTP_200

#/cards/{player_id}
#GET: returns cards in hand for requesting player
#This should be called periodically by the client to update user on his or her hand
class CardsResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):

        if not self.gs.gameStarted:
            raise falcon.HTTPInternalServerError(
            "Game Not Started",
            "Please start the game before issuing commands"
            )
        if(player_id not in self.gs.get_activePlayers()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently playing"
            )

        cardsList = []
        for card in self.gs.players[player_id].hand:
            cardsList.append(card.name)

        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({'cardsList' : cardsList });
        resp.status = falcon.HTTP_200

#/positions
#GET: returns position data objects for all player's positions
#This should be called periodically by the client, so that the map may update
class PositionsResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):

        if not self.gs.gameStarted:
            raise falcon.HTTPInternalServerError(
            "Game Not Started",
            "Please start the game before issuing commands"
            )

        character_to_pos_dict = {player_name: {'type': player_obj.location.type, 'name': player_obj.location.name, 'adj_locs': [loc.name for loc in player_obj.location.adj_locs]} for (player_name, player_obj) in self.gs.players.items()}
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps(character_to_pos_dict);
        resp.status = falcon.HTTP_200

#/legality/{player_id}/{move}
#GET: returns the validity of the given move for the given player
#this is somewhat redundant with the options method currently
class LegalityResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id, move):
        resp.set_header('Powered-By', 'Falcon')
        if not self.gs.gameStarted:
            raise falcon.HTTPInternalServerError(
            "Game Not Started",
            "Please start the game before issuing commands"
            )
        if(player_id not in self.gs.get_activePlayers()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently playing"
            )
        if(move in self.gs.players[player_id].getLegalMoves()):
            resp.body = '{OK}'
            resp.status = falcon.HTTP_200
        else:
            resp.body = '{INVALID}'
            resp.status = falcon.HTTP_200

#/move/{player_id}/{move}
#POST: Attempts to execute the given move for the given player.  There are 6 possible moves, not all of which will be valid:
#moveToHallway: Moves to a hallway connected to the current room. Takes the "adjIndex" argument in the request body
#moveToRoom: Moves to the room connected to the current hallway, and makes a suggestion.  Takes the "adjIndex", "character" and "weapon" arguments in the request body
#secretPassage: Moves to the room connected to the current room via the secret passage, and makes a suggestion.  Takes the "character" and "weapon" arguments in the request body
#suggest: Makes a suggestion without moving to a new room. Takes the "character" and "weapon" arguments in the request body
#accuse: Makes an accusation.  Takes the "character", "weapon", and "location" arguments in the request body
#skip: skips the players turn.  Takes no arguments in the request body.
#Arguments:
#adjIndex: The index of the location in the adj_locs element of the Room/Hallway object we are navigating to.
#character: The player name, with avaliable options defined in the gamestate object.
#weapon: The weapon name, with avaliable options defined in the game_logic.py
#location: The room name, with avaliable options defined in the game_logic.py
class MoveResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp, player_id, move):
        if not self.gs.gameStarted:
            raise falcon.HTTPInternalServerError(
            "Game Not Started",
            "Please start the game before issuing commands"
            )
        if(player_id not in self.gs.get_activePlayers()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently playing"
            )
        if(player_id not in self.gs.playerTurn):
            raise falcon.HTTPBadRequest(
            "Wrong Turn",
            "It is not your turn."
            )
        if(move not in self.gs.players[player_id].getLegalMoves()):
            raise falcon.HTTPBadRequest(
            "Invalid Move",
            "This is not a valid move."
            )
        info = ""
        if(move == "moveToHallway"):
            #move to hallway logic
            self.gs.players[player_id].location = self.gs.players[player_id].location.adj_locs[int(req.media.get('adjIndex'))]
            info = player_id + " moved from room to hallway"
        elif(move == "moveToRoom"):
            #move to room
            self.gs.players[player_id].location = self.gs.players[player_id].location.adj_locs[int(req.media.get('adjIndex'))]
            info = player_id + " moved from hallway to " + self.gs.players[player_id].location.name + ".  "
            #suggestion logic
            info += self.gs.makeSuggestion(player_id, req.media.get('character'), req.media.get('weapon'), self.gs.players[player_id].location)
        elif(move == "secretPassage"):
            self.gs.players[player_id].location = self.gs.players[player_id].location.corner_room
            info = player_id + " moved from has taken the secret passage to " + self.gs.players[player_id].location.name + ".  "
            info += self.gs.makeSuggestion(player_id, req.media.get('character'), req.media.get('weapon'), self.gs.players[player_id].location)
        elif(move == "suggest"):
            #suggestion logic
            info = self.gs.makeSuggestion(player_id, req.media.get('character'), req.media.get('weapon'), self.gs.players[player_id].location)
            pass
        elif(move == "accuse"):
            #accusation logic
            info = self.gs.makeAccusation(player_id, req.media.get('character'), req.media.get('weapon'), req.media.get('location'))
            pass
        else:
            pass
            #skip turn


        self.gs.nextTurn(player_id)
        self.gs.players[player_id].suggested = False

        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'moveResult' : info });
        resp.status = falcon.HTTP_201

#/init/{player_id}
#GET: returns the starting gamestate for the given player, including the rooms adjacent to them, their starting hand, and the number of players
#returns {gameStarted : false} if no clients have started the game via the post method yet
#this should periodically be called by all registed clients
#POST: starts (or restarts) the game.  At least 2 players must be registered.  Does not require a request body
#this should be callable by all clients.
class initResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        if not self.gs.gameStarted:
            resp.body = json.dumps({ 'gameStarted' : "false" });
            resp.status = falcon.HTTP_200
        elif(player_id not in self.gs.get_activePlayers()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently playing"
            )
        else:
            startingPos1 = self.gs.players[player_id].location.adj_locs[0].name
            startingPos2 = self.gs.players[player_id].location.adj_locs[1].name
            print("The suspect is: " + self.gs.board.caseFile.suspect.name)
            print("The room is: " + self.gs.board.caseFile.room.name)
            print("The weapon is: " + self.gs.board.caseFile.weapon.name, flush=True)
            numPlayers = self.gs.deck.numPlayers
            cardsList = []
            for card in self.gs.players[player_id].hand:
                cardsList.append(card.name)

            resp.body = json.dumps({
                'adjacentPosition1' : startingPos1,
                'adjacentPosition2' : startingPos2,
                'numPlayers' : numPlayers,
                'cardList' : " ".join(cardsList)
            })

            resp.status = falcon.HTTP_200

    def on_post(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        #resp.body = '{}'
        if len(self.gs.playerList) < 2:
            raise falcon.HTTPInternalServerError(
            "Insufficent Players Registered",
            "Not enough players are currently registered.  Please register at least 2 players."
            )
        elif(player_id not in self.gs.get_playerlist()):
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently playing"
            )
        character_list = ''
        self.gs.init_gamestate()
        resp.body = json.dumps({ 'info' : " ".join(self.gs.playerListActive) });
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
cards = CardsResource(gs)
positions = PositionsResource(gs)
move = MoveResource(gs)
gameInit = initResource(gs)

app.add_route('/register', register)
app.add_route('/deregister/{player_id}', deregister)
app.add_route('/turn/{player_id}', turn)
app.add_route('/options/{player_id}', gameOptions)
app.add_route('/cards/{player_id}', cards)
app.add_route('/legality/{player_id}/{move}', legality)
app.add_route('/positions', positions)
app.add_route('/move/{player_id}/{move}', move)
app.add_route('/init/{player_id}', gameInit)

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
