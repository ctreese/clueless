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
            return 4
        if self.location.type == 1: #location type 1 will designate a room. 0 will be a hallway
            if self.location.exits is False and self.suggested is not True:
                #this means the player put themselves in room and therefore will have their turn skiped
                #or they could make an accusation
                print("You have been blocked in a room. Your turn will be skipped.")
                #return some integer code signalling this is the situation
                return 3
            elif self.location.exits is False and self.suggested is True:
                #player can only make a suggestion
                #or they could make an accusation
                print("You are blocked in a room, but were moved there by a suggestion. Thus, you can only make a suggestion.")
                #return some integer code signalling this is the situation
                return 4
            else:
                print("You can move out of the room or make a suggestion.")
                #return some integer code signalling this is the situation
                return 0
        else:
            #they can do whatever
            print("You can move into a room or make a suggestion.")
            return 1
            
class Room:
    def __init__(self, name, corner_room):
        self.name = name
        self. corner_room = corner_room
        #self.adj_room = []
        self.adj_hall = []
        self.exits = True
        self.chars_in_room = []
        self.type = 1
        
class Hallway:
    def __init__(self, adj_room):
        self.adj_room = adj_room
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
        while len(self.cards) > 0:
            dealt_card = random.choice(self.cards)
            self.Players[i].hand.append(dealt_card)
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

def performTurn(player):
    option = player.getLegalMoves()
    if option == 1:
        response = -1
        #while response != 1 and response != 2 and response != 3 and response != 4:
        response = input("Choose from the following options: \n1. Move to " + player.location.adj_room[0].name + "\n2. Move to " +  player.location.adj_room[1].name + "\n3. Make suggestion \n4. Make accusation \n")
        print(response)
    

def gameLoop(board, players):
   print("")
   print("*****************************************")   
   print("**********GAME IS NOW STARTING!**********") 
   print("*****************************************") 
   print("")
   i = 0
   j = 0
   game_over_flag = 0
   while game_over_flag != 1 and i < 20:
       print("It is " + players[j].name + "'s turn!")
       performTurn(players[j])
       
       i += 1
       j += 1
       if j > (len(players) -1):
           j = 0
       
   
def gameInitialization():
    cards = cardInitialization()
    rooms = roomInitialization()
    hallways = hallwayInitialization(rooms)
    players = playerInitialization(hallways)
    deck = Deck(players,cards)
    caseFile = deck.deal()
    board = Board(rooms, hallways, caseFile)
    
    print("You are playing as: " + players[0].name)
    print(players[0].name + " is starting in the hallway between the " + players[0].location.adj_room[0].name + " and the " + players[0].location.adj_room[1].name)
    print("The case file contains the following cards: " + caseFile.suspect.name + ", " + caseFile.weapon.name + ", " + caseFile.room.name)
    print("The number of players in the game is: ", deck.numPlayers)
    print("The cards in your hand are: ")
    for card in players[0].hand:
        print(card.name)
        
    #gameLoop(board, players) #calls the main game loop... this will loop through players turns until the game is won
    
        
#gameInitialization()
#gameLoop()


        
        
        
        
        
