# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:57:44 2019

@author: ctreese
"""
import random

#global numPlayers

class Card:
    def __init__(self,card_type,number,name):
        """
        card_type: character, weapon, location
        number: each card will have unique number
        name: will hold name of character/weapon/location
        """
        self.type = card_type
        self.number = number
        self.name = name

class Player:
    def __init__(self,name,location):
        self.name = name
        self.accusation_made = 0
        self.location = location
        self.hand = []
        self.suggested = False

    def get_hand(self):
        return [card.name for card in self.hand]

    def getLegalMoves(self):
        if self.accusation_made is True:
            #player can only move and respond to accusations
            print("\nYou have already made an accusation. You can only move and respond to suggestions")
            return 4
        if self.location.type == 1: #location type 1 will designate a room. 0 will be a hallway
            exits = self.location.get_exits
            #if self.location.exits is False and self.suggested is not True:
            if not exits and self.suggested is not True:
                #this means the player put themselves in room and therefore will have their turn skiped
                #or they could make an accusation
                print("\nYou have been blocked in a room. Your turn will be skipped.")
                #return some integer code signalling this is the situation
                return 3
            #elif self.location.exits is False and self.suggested is True:
            elif not exits and self.suggested is True:
                #player can only make a suggestion
                #or they could make an accusation
                print("\nYou are blocked in a room, but were moved there by a suggestion. Thus, you can only make a suggestion.")
                #return some integer code signalling this is the situation
                return 2
            else:
                print("\nYou can move out of the room or make a suggestion.")
                #return some integer code signalling this is the situation
                return 0
        else:
            #they can do whatever
            print("\nYou can move into a room or make a suggestion.")
            return 1

class Room:
    def __init__(self, name, corner_room):
        self.name = name
        self. corner_room = corner_room
        #self.adj_room = []
        self.adj_hall = []
        #self.exits = []
        self.chars_in_room = []
        self.type = 1
    def get_exits(self):
        exits = []
        for hall in self.adj_hall:
            if hall.occupied == 0:
                exits.append(hall)
        return exits

class Hallway:
    def __init__(self, adj_room):
        self.adj_room = adj_room
        self.type = 0
        self.occupied = 0

class CaseFile:
    def __init__(self, suspect, weapon, room):
        self.suspect = suspect
        self.weapon = weapon
        self.room = room

class Deck:
    def __init__(self, Players, cards):
        self.Players = Players
        self.numPlayers = len(Players)
        self.cards= cards
    def deal(self):
        character_flag = 0
        weapon_flag = 0
        location_flag = 0
        while (character_flag + weapon_flag + location_flag) != 3:
            case_file_card = random.choice(self.cards)
            if case_file_card.type == 1 and character_flag == 0:
                character_card = case_file_card
                character_flag = 1
                self.cards.remove(character_card)
            elif case_file_card.type == 2 and weapon_flag == 0:
                weapon_card = case_file_card
                weapon_flag = 1
                self.cards.remove(weapon_card)
            elif case_file_card.type == 3 and location_flag == 0:
                location_card = case_file_card
                location_flag = 1
                self.cards.remove(location_card)
        case_file = CaseFile(character_card, weapon_card, location_card)
        i = 0
        while len(self.cards) > 0:
            dealt_card = random.choice(self.cards)
            self.Players[i].hand.append(dealt_card)
            self.cards.remove(dealt_card)
            i += 1
            if i > (self.numPlayers -1):
                i = 0

        return case_file

class Board:
    def __init__(self, rooms, hallways, caseFile, players):
        self.rooms = rooms
        self.hallways = hallways
        self.caseFile = caseFile
        self.players = players

def cardInitialization():
    #initialize character cards
    card = []

    card.append(Card(1, 1, "Rev. Green"))
    card.append(Card(1, 2, "Colonel Mustard"))
    card.append(Card(1, 3, "Mrs. Peacock"))
    card.append(Card(1, 4, "Professor Plum"))
    card.append(Card(1, 5, "Miss Scarlett"))
    card.append(Card(1, 6, "Mrs. White"))

    #initialize weapon cards
    card.append(Card(2, 7, "Candlestick"))
    card.append(Card(2, 8, "Dagger"))
    card.append(Card(2, 9, "Lead Pipe"))
    card.append(Card(2, 10, "Revolver"))
    card.append(Card(2, 11, "Rope"))
    card.append(Card(2, 12, "Wrench"))

    #initialize room cards
    card.append(Card(3, 13, "Ballroom"))
    card.append(Card(3, 14, "Billard Room"))
    card.append(Card(3, 15, "Conservatory"))
    card.append(Card(3, 16, "Dining Room"))
    card.append(Card(3, 17, "Hall"))
    card.append(Card(3, 18, "Kitchen"))
    card.append(Card(3, 19, "Library"))
    card.append(Card(3, 20, "Lounge"))
    card.append(Card(3, 21, "Study"))

    return card

def roomInitialization():
    room = []
    room.append(Room("Study",1))
    room.append(Room("Hall",0))
    room.append(Room("Lounge",1))
    room.append(Room("Dining Room",0))
    room.append(Room("Kitchen",1))
    room.append(Room("Ballroom",0))
    room.append(Room("Conservatory",1))
    room.append(Room("Library",0))
    room.append(Room("Billard Room",0))

    return room

def hallwayInitialization(room):
    hallway = []
    hallway.append(Hallway([room[0], room[1]])) #study to hall
    hallway.append(Hallway([room[1], room[2]])) #hall to lounge
    hallway.append(Hallway([room[2], room[3]])) #lounge to dining room
    hallway.append(Hallway([room[3], room[4]])) #dining room to kitchen
    hallway.append(Hallway([room[4], room[5]])) #kitchen to ballroom
    hallway.append(Hallway([room[5], room[6]])) #ballroom to conservatory
    hallway.append(Hallway([room[6], room[7]])) #conservatory to library
    hallway.append(Hallway([room[7], room[0]])) #library to study
    hallway.append(Hallway([room[1], room[8]])) #hall to billiard room
    hallway.append(Hallway([room[3], room[8]])) #dining room to billiard room
    hallway.append(Hallway([room[5], room[8]])) #ballroom to billiard room
    hallway.append(Hallway([room[7], room[8]])) #library to billiard room

    #for i in range(9):
    room[0].adj_hall.append(hallway[0])
    room[0].adj_hall.append(hallway[7])

    room[1].adj_hall.append(hallway[0])
    room[1].adj_hall.append(hallway[1])
    room[1].adj_hall.append(hallway[8])

    room[2].adj_hall.append(hallway[1])
    room[2].adj_hall.append(hallway[2])

    room[3].adj_hall.append(hallway[2])
    room[3].adj_hall.append(hallway[3])
    room[3].adj_hall.append(hallway[9])

    room[4].adj_hall.append(hallway[3])
    room[4].adj_hall.append(hallway[4])

    room[5].adj_hall.append(hallway[4])
    room[5].adj_hall.append(hallway[5])
    room[5].adj_hall.append(hallway[10])

    room[6].adj_hall.append(hallway[5])
    room[6].adj_hall.append(hallway[6])

    room[7].adj_hall.append(hallway[6])
    room[7].adj_hall.append(hallway[7])
    room[7].adj_hall.append(hallway[11])

    room[8].adj_hall.append(hallway[1])
    room[8].adj_hall.append(hallway[3])
    room[8].adj_hall.append(hallway[5])
    room[8].adj_hall.append(hallway[7])

    return hallway

def playerInitialization(hallway):
    player = []
    player.append(Player("Rev. Green", hallway[5]))
    player.append(Player("Colonel Mustard", hallway[2]))
    player.append(Player("Mrs. Peacock", hallway[6]))
    player.append(Player("Professor Plum", hallway[7]))
    player.append(Player("Miss Scarlett", hallway[1]))
    player.append(Player("Mrs. White", hallway[4]))

    global numPlayers
    numPlayers = len(player)

    return player

def performTurn(board, player, move_number):
    option = player.getLegalMoves()
    if option == 1:
        response = -1
        while response != 1 and response != 2 and response != 3 and response != 4:
            #response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n"))
            response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make accusation \n"))
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
        while valid_response == -1:
            optionIdx = []
            optionLoc = []
            idx = 0
            i = 0
            # Find all possible moves if in a room
            while i < len(player.location.adj_hall):

                if player.location.adj_hall[i].adj_room[0] != player.location:
                    optionIdx.append(idx)
                    print("", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[0].name)
                    optionLoc.append(player.location.adj_hall[i])
                    idx = idx + 1
                else:
                    optionIdx.append(idx)
                    print("", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[1].name)
                    optionLoc.append(player.location.adj_hall[i])
                    idx = idx + 1
                i = i + 1
            if player.location.corner_room == 1:
                optionIdx.append(idx)
                optionLoc.append(board.rooms[8])
                print("", idx+1, ". " + "Move to Billard Room")
                idx = idx + 1

            print("", idx+1, ". " + "Make suggestion")
            print("", idx+2, ". " + "Make Accusation")

            response = input()
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
                            print("", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[0].name)
                            optionLoc.append(player.location.adj_hall[i])
                            idx = idx + 1
                        else:
                            optionIdx.append(idx)
                            print("", idx+1, ". " + "Move towards " + player.location.adj_hall[i].adj_room[1].name)
                            optionLoc.append(player.location.adj_hall[i])
                            idx = idx + 1
                    i = i + 1
                if player.location.corner_room == 1:
                    optionIdx.append(idx)
                    optionLoc.append(board.rooms[8])
                    print("", idx+1, ". " + "Move to Billard Room")
                    idx = idx + 1

                response = input()
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
                    #response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n"))
                    response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n"))
                    if response == 1:
                        performMove(board, player, player.location.adj_room[0])
                    elif response == 2:
                        performMove(board, player, player.location.adj_room[1])
    elif option == 2:
        while response != 1 or response != 2:
            #response = int(input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n"))
            response = int(input("Choose from the following options: \n1. Make Suggestion \n2. Make Accusation "))
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
        print("\n" + player.name + " has moved to the " + location.name)
    else:
        player.location.occupied == 1
        print("\n" + player.name + " has moved to the hallway between " + player.location.adj_room[0].name + " and " + player.location.adj_room[1].name)

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

# def gameLoop(board):
#    print("")
#    print("*****************************************")
#    print("**********GAME IS NOW STARTING!**********")
#    print("*****************************************")
#    print("")
#    i = 0
#    j = 0
#    global game_over_flag
#    game_over_flag = 0
#    while game_over_flag != 1 and i < 30:
#        print("\nIt is " + board.players[j].name + "'s turn!")
#        performTurn(board, board.players[j])
#        i += 1
#        j += 1
#        if j > (len(board.players) -1):
#            j = 0

#
# def gameInitialization():
#     cards = cardInitialization()
#     rooms = roomInitialization()
#     hallways = hallwayInitialization(rooms)
#     players = playerInitialization(hallways)
#     deck = Deck(players,cards)
#     caseFile = deck.deal()
#     board = Board(rooms, hallways, caseFile, players)
#
#     print("You are playing as: " + players[0].name)
#     print(players[0].name + " is starting in the hallway between the " + players[0].location.adj_room[0].name + " and the " + players[0].location.adj_room[1].name)
#     print("The case file contains the following cards: " + caseFile.suspect.name + ", " + caseFile.weapon.name + ", " + caseFile.room.name)
#     print("The number of players in the game is: ", deck.numPlayers)
#     print("The cards in your hand are: ")
#     for card in players[0].hand:
#         print(card.name)
#
#     gameLoop(board) #calls the main game loop... this will loop through players turns until the game is won
#

#gameInitialization()
#gameLoop()
