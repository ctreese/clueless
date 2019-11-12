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
            nextTurn(self, self.playerTurn)

    def makeSuggestion(self, character, weapon, location):
        return game_logic.performSuggestion(character, weapon, location);

    def makeAccusation(self, character, weapon, location):
        gameWon = game_logic.performAccusation(character, weapon, location);
        if(gameWon):
            self.gameStarted = False
            return "You have won the game!"
        else:
            return "Sorry, that is incorrect."
        
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
        resp.body = json.dumps({ 'playerturn': self.gs.playerTurn });
        resp.status = falcon.HTTP_200

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
        for position in self.gs.players[player_id].location.adj_locs:
            moveCandidates.append(position.name)
        cardsList = []
        for card in self.gs.players[player_id].hand:
            cardsList.append(card.name)
            
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'move_options' : options, 'adj' : moveCandidates, 'cardsList' : cardsList });
        resp.status = falcon.HTTP_200

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
            self.gs.players[player_id].location = self.gs.players[player_id].location.adj_locs[req.media.get('adjIndex')]
            info = player_id + "moved from room to hallway"
        elif(move == "moveToRoom"):
            #move to room
            self.gs.players[player_id].location = self.gs.players[player_id].location.adj_locs[req.media.get('adjIndex')]
            info = player_id + "moved from hallway to " + self.gs.players[player_id].location.name + ".  "
            #suggestion logic
            info += self.gs.makeSuggestion(req.media.get('character'), req.media.get('weapon'), self.gs.players[player_id].location.name)
            pass
        elif(move == "suggest"):
            #suggestion logic
            info = self.gs.makeSuggestion(req.media.get('character'), req.media.get('weapon'), self.gs.players[player_id].location.name)
            pass
        elif(move == "accuse"):
            #accusation logic
            info = self.gs.makeAccusation(req.media.get('character'), req.media.get('weapon'), req.media.get('location'))
            pass
        else:
            pass
            #skip turn
        
        
        self.gs.nextTurn(player_id)
        
        random_move = " moved from room to hallway."
        resp.set_header('Powered-By', 'Falcon')
        resp.body = json.dumps({ 'moveResult' : info });
        resp.status = falcon.HTTP_201

class initResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)
        
    def on_get(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        if not self.gs.gameStarted:
            resp.body = json.dumps({ 'gameStarted' : "false" });
            resp.status = falcon.HTTP_200
        else:
            startingPos1 = self.gs.players[player_id].location.adj_locs[0].name
            startingPos2 = self.gs.players[player_id].location.adj_locs[1].name
            caseFileSuspect = self.gs.caseFile.suspect.name
            caseFileWeapon = self.gs.caseFile.weapon.name
            caseFileRoom = self.gs.caseFile.room.name
            numPlayers = self.gs.deck.numPlayers
            cardsList = []
            for card in self.gs.players[player_id].hand:
                cardsList.append(card.name)
                
            resp.body = json.dumps({ 'startingPos1' : startingPos1, 'startingPos2' : startingPos2, 'caseFileSuspect' : caseFileSuspect, 'caseFileWeapon' : caseFileWeapon, \
                'caseFileRoom' : caseFileRoom, 'numPlayers' : numPlayers, 'cardList' : cardsList})
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp, player_id):
        resp.set_header('Powered-By', 'Falcon')
        #resp.body = '{}'
        if len(self.gs.playerList) < 2:
            raise falcon.HTTPInternalServerError(
            "Insufficent Players Registered",
            "Not enough players are currently registered.  Please register at least 2 players."
            )
        character_list = ''
        self.gs.init_gamestate()
        resp.body = json.dumps({ 'info' : self.gs.playerListActive });
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
app.add_route('/move/{player_id}/{move}', move)
app.add_route('/init/{player_id}', gameInit)

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
