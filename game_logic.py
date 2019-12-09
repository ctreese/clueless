# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:57:44 2019

@author: ctreese
"""
import random

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
        
    def getLegalMoves(self):
        if self.accusation_made is True:
            #player can only move and respond to accusations
            print("You have already made an accusation. You can only move and respond to accusations")
            return []
        if self.location.type == 1: #location type 1 will designate a room. 0 will be a hallway
            legalMoves = ["accuse"]
            if self.location.corner_room:
                legalMoves.append("secretPassage")
            if self.suggested:
                legalMoves.append("suggest")
            if self.location.exits:
                legalMoves.append("moveToHallway")
            return legalMoves
        else:
            #they can do whatever
            print("You can move into a room or make a accusation.")
            return ["moveToRoom", "accuse"]
            
class Room:
    def __init__(self, name, corner_room):
        self.name = name
        self.corner_room = corner_room
        #self.adj_room = []
        self.adj_locs = []
        self.exits = True
        self.chars_in_room = []
        self.type = 1
        
class Hallway:
    def __init__(self, adj_locs):
        self.name = "Hallway connecting " + adj_locs[0].name + " to " + adj_locs[1].name
        self.adj_locs = adj_locs
        self.type = 0

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
        playerNames = list(self.Players.keys())
        while len(self.cards) > 0:
            playerDealtTo = playerNames[i]
            dealt_card = random.choice(self.cards)
            self.Players[playerDealtTo].hand.append(dealt_card)
            self.cards.remove(dealt_card)
            i += 1
            if i > (self.numPlayers -1):
                i = 0
        
        return case_file
class Board:
    def __init__(self, rooms, hallways, caseFile):
        self.rooms = rooms
        self.hallways = hallways
        self.caseFile = caseFile

def cardInitialization():
    #initialize character cards
    card = []
    
    card.append(Card(1, 1, "Rev. Green"))
    card.append(Card(1, 2, "Colonel Mustard"))
    card.append(Card(1, 3, "Mrs. Peacock"))
    card.append(Card(1, 4, "Professor Plum"))
    card.append(Card(1, 5, "Miss Scarlett"))
    card.append(Card(1, 6, "Mrs. White"))
    
    #card[0] = Card(1, 1, "Rev. Green")
    #card[1] = Card(1, 2, "Colonel Mustard")
    #card[2] = Card(1, 3, "Mrs. Peacock")
    #card[3] = Card(1, 4, "Professor Plum")
    #card[4] = Card(1, 5, "Miss Scarlett")
    #card[5] = Card(1, 6, "Mrs. White")
    
    #initialize weapon cards
    card.append(Card(2, 7, "Candlestick"))
    card.append(Card(2, 8, "Dagger"))
    card.append(Card(2, 9, "Lead Pipe"))
    card.append(Card(2, 10, "Revolver"))
    card.append(Card(2, 11, "Rope"))
    card.append(Card(2, 12, "Wrench"))
    
    
#    card[6] = Card(2, 7, "Candlestick")
#    card[7] = Card(2, 8, "Dagger")
#    card[8] = Card(2, 9, "Lead Pipe")
#    card[9] = Card(2, 10, "Revolver")
#    card[10] = Card(2, 11, "Rope")
#    card[11] = Card(2, 12, "Wrench")
    
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
    
#    card[12] = Card(3, 13, "Ballroom")
#    card[13] = Card(3, 14, "Billard Room")
#    card[14] = Card(3, 15, "Conservatory")
#    card[15] = Card(3, 16, "Dining Room")
#    card[16] = Card(3, 17, "Hall")
#    card[17] = Card(3, 18, "Kitchen")
#    card[18] = Card(3, 19, "Library")
#    card[19] = Card(3, 20, "Lounge")
#    card[20] = Card(3, 21, "Study")
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
    
    room[0].corner_room = room[4]
    room[2].corner_room = room[6]
    room[4].corner_room = room[0]
    room[6].corner_room = room[2]
    
#    room[0]= Room("Study",1)
#    room[1] = Room("Hall",0)
#    room[2] = Room("Lounge",1)
#    room[3] = Room("Dining Room",0)
#    room[4] = Room("Kitchen",1)
#    room[5] = Room("Ballroom",0)
#    room[6] = Room("Conservatory",1)
#    room[7] = Room("Library",0)
#    room[8] = Room("Billard Room",0)  
    return room
    
def hallwayInitialization(room):
    hallway = []
    hallway.append(Hallway([room[0], room[1]])) #study to hall 0
    hallway.append(Hallway([room[1], room[2]])) #hall to lounge
    hallway.append(Hallway([room[2], room[3]])) #lounge to dining room
    hallway.append(Hallway([room[3], room[4]])) #dining room to kitchen
    hallway.append(Hallway([room[4], room[5]])) #kitchen to ballroom
    hallway.append(Hallway([room[5], room[6]])) #ballroom to conservatory 5
    hallway.append(Hallway([room[6], room[7]])) #conservatory to library
    hallway.append(Hallway([room[7], room[0]])) #library to study
    hallway.append(Hallway([room[1], room[8]])) #hall to billiard room
    hallway.append(Hallway([room[3], room[8]])) #dining room to billiard room
    hallway.append(Hallway([room[5], room[8]])) #ballroom to billiard room 10
    hallway.append(Hallway([room[7], room[8]])) #library to billiard room
    
    room[0].adj_locs = [hallway[0], hallway[7]]
    room[1].adj_locs = [hallway[0], hallway[1], hallway[8]]
    room[2].adj_locs = [hallway[1], hallway[2]]
    room[3].adj_locs = [hallway[2], hallway[3], hallway[9]]
    room[4].adj_locs = [hallway[3], hallway[4]]
    room[5].adj_locs = [hallway[4], hallway[5], hallway[10]]
    room[6].adj_locs = [hallway[5], hallway[6]]
    room[7].adj_locs = [hallway[6], hallway[7], hallway[11]]
    room[8].adj_locs = [hallway[8], hallway[9], hallway[10], hallway[11]]
    
    
#    hallway[0] = Hallway([room[0], room[1]]) #study to hall
#    hallway[1] = Hallway([room[1], room[2]]) #hall to lounge
#    hallway[2] = Hallway([room[2], room[3]]) #lounge to dining room
#    hallway[3] = Hallway([room[3], room[4]]) #dining room to kitchen
#    hallway[4] = Hallway([room[4], room[5]]) #kitchen to ballroom
#    hallway[5] = Hallway([room[5], room[6]]) #ballroom to conservatory
#    hallway[6] = Hallway([room[6], room[7]]) #conservatory to library
#    hallway[7] = Hallway([room[7], room[0]]) #library to study
#    hallway[8] = Hallway([room[1], room[9]]) #hall to billiard room
#    hallway[9] = Hallway([room[3], room[9]]) #dining room to billiard room
#    hallway[10] = Hallway([room[5], room[9]]) #ballroom to billiard room
#    hallway[11] = Hallway([room[7], room[9]]) #library to billiard room
    return hallway
    
def playerInitialization(hallway, playerList):
    player = {}
    i = 0
    for character in playerList:
        player.update({character : Player(character, hallway[i])})
        i += 1
    
    
#    player[0] = Player("Rev. Green", hallway[5])
#    player[1] = Player("Colonel Mustard", hallway[2])
#    player[2] = Player("Mrs. Peacock", hallway[6])
#    player[3] = Player("Professor Plum", hallway[7])
#    player[4] = Player("Miss Scarlett", hallway[1])
#    player[5] = Player("Mrs. White", hallway[4])
    return player

def performSuggestion(suspectName, weaponName, locationName, playerList):
    #TODO
    return suggestionResponse(suspectName, locationName, weaponName, playerList)
    
def suggestionResponse(suspectName, locationName, weaponName, playerList):
    for player in playerList.values():
        for card in player.hand:
            if card.name == suspectName or card.name == locationName or card.name == weaponName:
                return player.name + " has disproved the suggestion, by showing the card " + card.name;
    return "No one could disprove the suggestion!"
    
    
def performAccusation(board, player, suspectName, weaponName, roomName):
        
    print(player.name + "has selected the following: ")
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
        print("The weapon was: " + board.caseFile.weapon.name, flush=True)
        global game_over_flag 
        game_over_flag = 1
        return True
    else:
        print(player.name + " was incorrect.", flush=True)
        player.accusation_made = True
        return False



        
        
        
        
        
