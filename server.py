import json
import logging
from wsgiref import simple_server
import random
import falcon
from game_logic import *
import time

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

        self.client_input = None
        self.console_output = {}
        self.current_options = []

        self.has_started = False

    def find_player(self, player_name):
        found = next((player for player in self.playerList if player.name == player_name), None)
        if not found:
            raise Exception('Player not found')

    def get_playerlist(self):
        return self.playerList

    def get_current_turn_player_name(self):
        current_turn_number = self.gs.turn_number
        num_players = len(self.gs.playerList)
        return self.playerList[self.turn_number % num_players].name

    def add_player(self, playerName):
        if playerName in self.avaliableCharacters:
            self.playerList.append(playerName)
            self.avaliableCharacters = [player for player in self.avaliableCharacters if player.name!=playerName.name] # remove player via list comprehension

    def remove_player(self, playerName):
        if playerName in self.playerList:
            self.playerList = [player for player in self.playerList if player.name!=playerName.name] # remove player via list comprehension
            self.avaliableCharacters.append(playerName)

    def receive_input():

        while self.client_input is None:
            time.sleep(1)
        current_input = self.client_input
        self.client_input = None
        return current_input

    def performTurn(board, player, move_number):
        option = player.getLegalMoves()
        if option == 1:
            response = -1
            while response != 1 and response != 2 and response != 3 and response != 4:
                # response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n"))
                # response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make accusation \n"))
                self.current_options = [
                    "1. Move to " + player.location.adj_room[0].name,
                    "2. Move to " +  player.location.adj_room[1].name,
                    "3. Make accusation"
                ]
                response = receive_input()
                if response == 1:
                    performMove(board, player, player.location.adj_room[0])
                elif response == 2:
                    performMove(board, player, player.location.adj_room[1])
                elif response == 3:
                    performAccusation(board, player)
    #    elif option == 0:
    #        response = -1
    #        #NEED TO UPDATE THIS TO GIVE CORRECT MOVE OPTIONS AND RESPONSES
    #        while response != 1 and response != 2 and response != 3 and response != 4:
    #            #response = int(input("Choose from the following options: \n1. Move to hallway connecting " + player.location.name + " and " + player.location.adj_hall.adj_room[0].name + "\n2. Move to hallway connecting " +  player.location.name + " and " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n"))
    #            response = int(input("\n3. Make suggestion \n4. Make accusation \n"))
    #            if response == 1:
    #                hallway = findHallway(player.location.name, player.location.adj_room[0].name)
    #                performMove(board, player, hallway)
    #            elif response == 2:
    #                performMove(board, player, player.location.adj_room[1])
    #            elif response == 3:
    #                #performSuggestion
    #                performSuggestion(board, player)
    #            elif response == 4:
    #                #performAccusation
    #                performAccusation(board, player)
        elif option == 0:
            response = -1
            optionIdx = []
            optionLoc = []
            idx = 0
            i = 0
            valid_response = -1

            self.current_options = []

            while valid_response == -1:
                optionIdx = []
                optionLoc = []
                idx = 0
                i = 0
                # Find all possible moves if in a room
                while i < len(player.location.adj_hall):

                    if player.location.adj_hall[i].adj_room[0] != player.location:
                        optionIdx.append(idx)
                        optionLoc.append(player.location.adj_hall[i])

                        option_string = " ".join(["", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[0].name])
                        print(option_string)
                        self.current_options.append(option_string)

                        idx += 1
                    else:
                        optionIdx.append(idx)
                        optionLoc.append(player.location.adj_hall[i])

                        option_string = " ".join(["", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[1].name])
                        print(option_string)
                        self.current_options.append(option_string)

                        idx += 1

                    i += 1

                if player.location.corner_room == 1:
                    optionIdx.append(idx)
                    optionLoc.append(board.rooms[8])

                    option_string = " ".join("", idx+1, ". " + "Move to Billard Room")
                    print(option_strong)
                    self.current_options.append(option_string)

                    idx += 1

                self.current_options.append(" ".join(["", idx+1, ". " + "Make suggestion"]))
                self.current_options.append(" ".join(["", idx+2, ". " + "Make Accusation"]))
                print("", idx+1, ". " + "Make suggestion")
                print("", idx+2, ". " + "Make Accusation")

                # response = input()
                response = receive_input()
                print(response)
                # Move player if there response was a move
                responseIdx = int(response)-1
                if responseIdx <= idx-1:
                    valid_response = 1
                    #player.location = optionLoc[responseIdx]
                    performMove(board,player,optionLoc[responseIdx])
                    #print("Moved player to hallway connecting " + optionLoc[responseIdx].adj_room[0].name + " and " + optionLoc[responseIdx].adj_room[1].name)

                elif responseIdx == idx:
                    valid_response = 1
                    performSuggestion(board, player)

                elif responseIdx == idx+1:
                    valid_response = 1
                    performAccusation(board, player)
        elif option == 4:
            self.console_output = []
            if player.location.type == 1: #in a room
                response = -1
                optionIdx = []
                optionLoc = []
                idx = 0
                i = 0
                valid_response = -1
                while valid_response == -1:
                    optionIdx = []
                    optionLoc = []
                    idx = 0
                    i = 0
                    # Find all possible moves if in a room
                    while i < len(player.location.adj_hall):
                        if player.location.adj_hall[i].occupied == 0:
                            if player.location.adj_hall[i].adj_room[0] != player.location:
                                optionIdx.append(idx)
                                optionLoc.append(player.location.adj_hall[i])

                                output_string = " ".join(["", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[0].name])
                                print(output_string)
                                self.console_output.append(output_string)

                                idx += 1
                            else:
                                optionIdx.append(idx)
                                optionLoc.append(player.location.adj_hall[i])

                                output_string = " ".join("", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[1].name)
                                print(output_string)
                                self.console_output.append(output_string)

                                idx += 1
                        i = i + 1
                    if player.location.corner_room == 1:
                        optionIdx.append(idx)
                        optionLoc.append(board.rooms[8])

                        output_string = " ".join("", idx+1, ". " + "Move to Billard Room")
                        print(output_string)
                        self.console_output.append(output_string)

                        idx = idx + 1


                    # response = input()
                    receive_input()

                    print(response)
                    # Move player if there response was a move
                    responseIdx = int(response)-1
                    if responseIdx <= idx-1:
                        valid_response = 1
                        #player.location = optionLoc[responseIdx]
                        performMove(board,player,optionLoc[responseIdx])
                        #print("Moved player to hallway connecting " + optionLoc[responseIdx].adj_room[0].name + " and " + optionLoc[responseIdx].adj_room[1].name)
            elif player.location.type == 0: #in a room
                    response = -1
                    while response != 1 and response != 2 and response != 3 and response != 4:
                        # response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n"))
                        # response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n"))
                        self.console_output = " ".join(["1. Move to " + player.location.adj_room[0].name, "2. Move to " +  player.location.adj_room[1].name])
                        receive_input()
                        if response == 1:
                            performMove(board, player, player.location.adj_room[0])
                        elif response == 2:
                            performMove(board, player, player.location.adj_room[1])
        elif option == 2:
            while response != 1 or response != 2:
                # response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n"))
                # response = int(input("Choose from the following options: \n1. Make Suggestion \n2. Make Accusation "))
                self.current_options = [
                    "1. Make Suggestion",
                    "2. Make Accusation"
                ]
                response = receive_input()
                if response == 1:
                    performSuggestion(board, player)
                elif response == 2:
                    performAccusation(board, player)

    def findHallway(board, room1, room2):
        found_flag = 0
        i = 0
        while found_flag == 0:
            if board.hallways[i].adj_room[0] == room1 or board.hallways[i].adj_room[0] == room2:
                if board.hallways[i].adj_room[1] == room1 or board.hallways[i].adj_room[1] == room2:
                    found_flag = 1
        return board.hallways[i]

    def performMove(board, player, location):
        #print(player.name + " " + "has moved from " + player.location.name + " to " + location.name)
        if player.location.type == 0:
            player.location.occupied = 0
        player.location = location
        if player.location.type == 1:
            output_string = " ".join("\n" + player.name + " has moved to the " + location.name)
            print(output_string)

        else:
            player.location.occupied == 1
            output_string = " ".join("\n" + player.name + " has moved to the hallway between " + player.location.adj_room[0].name + " and " + player.location.adj_room[1].name)
            print(output_string)

        self.console_output["move_result"] = output_string

    def performSuggestion(board, player):
        #TODO
        response = 0
        suspects = []
        self.current_options = []
        while response < 1 or response >= numPlayers:
            i = 1
            print("The following players are suspects: ")
            for suspect in board.players:
                 if suspect.name != player.name:
                     suspects.append(suspect)
                     output_string = " ".join("", i, ". " + suspect.name)
                     print(output_string)
                     self.current_options.append(output_string)
                     i += 1
            # response = int(input("Please select a suspect (using numbers):"))
            response = receive_input()

        suspectName = suspects[response-1].name
        suggestedPlayer = suspects[response-1]
        #print("You selected: " + suspectName)

        response = 0
        self.current_options = []
        while response < 1 or response > 6:

            output_string_arr = ["1. Candlestick", "2. Dagger", "3. Lead Pipe", "4. Revolver", "5. Rope", "6. Wrench"]
            print(output_string_arr)
            self.current_options = output_string_arr
            response = receive_input()
            # response = int(input("Please select a weapon (using numbers):"))
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
                    self.console_output["move_result"] = player.name + " has disproved the suggestion!"
                    print(player.name + " has disproved the suggestion!")
                    return
        self.console_output["move_result"] = "No one could disprove the suggestion!"
        print("No one could disprove the suggestion!")
        return

    def performAccusation(board, player):
        #TODO
        response = 0
        suspects = []
        self.current_options = []
        while response < 1 or response >= numPlayers:
            i = 1
            print("The following players are suspects: ")
            for suspect in board.players:
                 if suspect.name != player.name:
                     suspects.append(suspect)
                     output_string = " ".join("", i, ". " + suspect.name)
                     print(output_string)
                     self.current_options.append(output_string)
                     i += 1
            # response = int(input("Please select a suspect (using numbers):"))
            response = receive_input()
        suspectName = suspects[response-1].name
        #print("You selected: " + suspectName)
        response = 0
        self.current_options = []
        while response < 1 or response > len(board.rooms):
            i = 1
            for room in board.rooms:
                output_string = " ".join(["", i, ". " + room.name])
                print(output_string)
                self.current_options.append(output_string)
                i += 1
            response = receive_input()
            # response = int(input("Please select a room (using numbers):"))
        roomName = board.rooms[response-1].name
        #print("You selected: " + roomName)
        response = 0
        self.current_options = []
        while response < 1 or response > 6:
            output_string_arr = ["1. Candlestick", "2. Dagger", "3. Lead Pipe", "4. Revolver", "5. Rope", "6. Wrench"]
            print(output_string_arr)
            self.current_options = output_string_arr
            response = receive_input()
            # response = int(input("Please select a weapon (using numbers):"))
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

        output_string = "".join([player.name + "made the following accusation!", "Suspect: " + suspectName, "Room: " + roomName, "Weapon: " + weaponName])
        self.console_output['move_result'] = output_string
        print(output_string)

        if board.caseFile.suspect.name == suspectName and board.caseFile.room.name == roomName and board.caseFile.weapon.name == weaponName:

            self.console_output['move_result'] = player.name + " has won the game!"

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
            self.console_output['move_result'] = player.name + "'s accusation was wrong!"
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

class GameStateResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp):
        resp.set_header('Powered-By', 'Falcon')
        current_player_name = req.player_id
        def general_gs():
            self.console_output['hand'] = self.gs.find_player(current_player_name).get_hand()
            # TODO get position of all players
        def player_gs():
            self.console_output['options'] = self.gs.current_options

        general_gs()
        if(current_player_name is self.gs.get_current_turn_player_name):
            player_gs()

        else:
            self.console_output['error'] = "Not your turn, buddy."
        self.console_output = {}
        resp = json.dumps(self.gs.console_output)

class StartResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        def gameInitialization(req, resp):
            resp.set_header('Powered-By', 'Falcon')
            resp.body = json.dumps({ 'message': "Game has started" });
            resp.status = falcon.HTTP_200
            self.gs.deck = Deck(self.gs.playerList, self.gs.cards)
            self.gs.caseFile = self.gs.deck.deal()
            self.gs.board = Board(self.gs.rooms, self.gs.hallways, self.gs.caseFile, self.gs.playerList)

        def gameStartOutput(req, resp):
            print("You are playing as: " + self.gs.playerList[-1].name)
            print(self.gs.playerList[-1].name + " is starting in the hallway between the " + self.gs.playerList[-1].location.adj_room[0].name + " and the " + self.gs.playerList[-1].location.adj_room[1].name)
            print("The case file contains the following cards: " + self.gs.caseFile.suspect.name + ", " + self.gs.caseFile.weapon.name + ", " + self.gs.caseFile.room.name)
            print("The number of players in the game is: ", len(self.gs.playerList))
            print("The cards in your hand are: ")
            for card in self.gs.playerList[-1].hand:
                print(card.name)

        if not self.gs.has_started:
            gameInitialization(req, resp)
            gameStartOutput(req, resp)
            self.gs.has_started = True
        else:
            resp.body = json.dumps({ 'message': "Game has already started. Stop pressing start." });
            # self.gameStartOutput(req, resp)

class MoveResource(object):

    def __init__(self, db):
        self.gs = gs
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp):
        # TODO add move number legality check
        # TODO add player turn legality check

        current_turn_number = self.gs.turn_number
        num_players = len(self.gs.playerList)
        current_player_name = self.gs.playerList[self.gs.turn_number % num_players].name

        if(req.player_name not in gs.get_playerlist()):
            self.gs.console_output['error'] = "Invalid Player Name"
            raise falcon.HTTPBadRequest(
            "Invalid Player Name",
            "That player name is not currently registered"
            )
        elif(req.player_name is not current_player_name):
            self.gs.console_output['error'] = "Not your turn"
            raise falcon.HTTPBadRequest(
            "Invalid Move",
            "Your turn is not now"
            )
        elif(req.move > 10):
            self.gs.console_output['error'] = "Move is invalid"
            raise falcon.HTTPBadRequest(
            "Invalid Move",
            "Move is not from list of options"
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
                self.gs.client_input = req.move
                # performTurn(self.gs.board, current_player, move_number)
        self.gs.console_output = {}

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

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':

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

    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
