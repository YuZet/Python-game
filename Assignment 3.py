import math                                    #S10221991, Tee Yu Zet, CICTP04, 9 Aug 2021
import random

# Save game function
def reservedSaveGame(reservedState):
    try:
        f = open('savefile.txt', 'wt')
        f.write(str(reservedState))
        print()
        print("Game saved!")
        f.close()
    except:
        print("Unable to write to file") #no game to be saved
    pass
# Start game
def reservedStartNewGame(reservedState):
    reservedBuildingsName = list(reservedState['building'].keys())
    reservedRandomChoice1 = 0
    reservedRandomChoice2 = 0
    turnExecuted = False
    firstRun = True
    while(True):
        if(firstRun or turnExecuted):
            reservedRandomChoice1 = random.randint(0,len(reservedBuildingsName) - 1) #first randomb building
            reservedRandomChoice2 = random.randint(0,len(reservedBuildingsName) - 1) #second random building
            turnExecuted = False
            firstRun = False
        if(reservedState['counter'] == 16):
            print("Final layout of Simp City:")
            reservedPrintState(reservedState)
            reservedSeeCurrentScore(reservedState) #When it reaches turn 16, the game ends
            break
		
        print(f"Turn {reservedState['counter'] + 1}") #turn number
        reservedPrintState(reservedState)
        print(f"1. Build a {reservedBuildingsName[reservedRandomChoice1]}") #printing of the options
        print(f"2. Build a {reservedBuildingsName[reservedRandomChoice2]}")
        print("3. See remaining buildings")
        print("4. See current score")
        print("5. Save game")
        print("0. Exit to main menu")
        reservedChoice = input("Your choice? ")
        if(reservedChoice == '0'):
            break #go back to main menu
        elif(reservedChoice == '1'):
            
            reservedResult = reservedBuild(reservedBuildingsName[reservedRandomChoice1], reservedState, reservedState['counter'] == 0) #runs the function that allows you to build the building
            if(reservedResult):
                reservedState['counter'] += 1
                turnExecuted = True #increases the turn number
        elif(reservedChoice == '2'):
            reservedResult = reservedBuild(reservedBuildingsName[reservedRandomChoice2], reservedState, reservedState['counter'] == 0) #runs the function that allows you to build the building
            if(reservedResult):
                reservedState['counter'] += 1
                turnExecuted = True #increases turn number
        elif(reservedChoice == '3'):
            reservedSeeRemainingBuilding(reservedState) #runs the function that sees remaining building
        elif(reservedChoice == '4'):
            reservedSeeCurrentScore(reservedState) #runs the function that sees your current score
        elif(reservedChoice == '5'):
            reservedSaveGame(reservedState) #runs the function that saves the game
        elif(reservedChoice == '0'): #go back to main menu
            break

#Main function
def main():
    reservedState = {
        'building': {
            'BCH' : {
                'quantity' : 8
            },
            'FAC' : {
                'quantity' : 8
            },
            'HSE' : {
                'quantity' : 8
            },
            'SHP' : {
                'quantity' : 8
            },
            'HWY' : {
                'quantity' : 8
            }
        },
        'score': 0,
        'placements': [[0 ,0 ,0 ,0],[0 ,0 ,0 ,0],[0 ,0 ,0 ,0],[0 ,0 ,0 ,0]],      #The type of buildings that can be built and the amount of times it can be built
        'counter': 0
    }
    while(True):
        reservedChoice = reservedMenu()
        if(reservedChoice == "1"):
            reservedStartNewGame(reservedState) #Start a new game
        elif(reservedChoice == "2"):
            s = open('savefile.txt', 'r').read()
            reservedState = eval(s)  #built-in function to run the saved file
            reservedStartNewGame(reservedState) #brings up the previous saved game
        elif(reservedChoice == "0"):
            exit() #allows you to kill the program


#Prints menu
def reservedMenu():
    print("Welcome, mayor of Simp City!")
    print("----------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print("0. Exit")
    return input("Your choice? ")

#prints the board
def reservedPrintState(reservedState):
    
    print(" "* 4 + "A" + " "* 5 + "B" + " "* 5 + "C" + " "* 5 + "D") #Prints the A B C D coluum
    for reserved in range(1,5):
        reservedCurrentIndex = reserved - 1
        print(" " + ("+" + "-" * 5)*4 + "+")
        reservedString = str(reserved)
        for reservedPlacement in reservedState["placements"][reservedCurrentIndex]:
            if(reservedPlacement == 0):
                reservedString += ("|" + " " * 5)
            else:
                reservedString += ("|" + " " + reservedPlacement + " ")
        reservedString += "|"
        print(reservedString)
    print(" " + ("+" + "-" * 5)*4 + "+")

# building on board
def reservedBuild(building, reservedState, firstTurn=False):
    reservedMapper = { #dictionary to store the coluum alphabets
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
    }
    reservedBuildWhere = input("Build where? ");
    reservedX = int(reservedBuildWhere[1]) - 1
    reservedY = reservedMapper[reservedBuildWhere[0]] #X and Y is the coordinates
    # Check for existing building
    if(reservedState["placements"][reservedX][reservedY] == 0):
        #Check for adjacent
        if(firstTurn):
            reservedState["building"][building]['quantity'] -= 1
            reservedState["placements"][reservedX][reservedY] = building
        elif((reservedX - 1) > -1 and (reservedState["placements"][reservedX - 1][reservedY] != 0)):
            reservedState["building"][building]['quantity'] -= 1
            reservedState["placements"][reservedX][reservedY] = building
        elif((reservedX + 1) < 4 and (reservedState["placements"][reservedX + 1][reservedY] != 0)):
            reservedState["building"][building]['quantity'] -= 1
            reservedState["placements"][reservedX][reservedY] = building
        elif((reservedY - 1) > -1 and (reservedState["placements"][reservedX][reservedY - 1] != 0)):
            reservedState["building"][building]['quantity'] -= 1
            reservedState["placements"][reservedX][reservedY] = building
        elif((reservedY + 1) < 4 and (reservedState["placements"][reservedX][reservedY + 1] != 0)):
            reservedState["building"][building]['quantity'] -= 1
            reservedState["placements"][reservedX][reservedY] = building
        else:
            print("You must build next to an existing building.")
            return False #allows you to choose where you can build the building
    return True

# Check the quantity of building
def reservedSeeRemainingBuilding(reservedState):
    print()
    print("Building\t\tRemaining")
    print("--------\t\t---------")
    for reservedBuilding in reservedState["building"]:
        print(f"{reservedBuilding}\t\t\t{reservedState['building'][reservedBuilding]['quantity']}")
    pass

# This function calculates the highway points
def reservedHighwayCalculation(reservedPlacement , currentX, currentY, currentLinkage, direction):
    if(direction == -1):
        if(currentY + direction > -1 and reservedPlacement[currentX][currentY + direction] == 'HWY'):  #checks the left and right side of the current HWY for other HWY
            return reservedHighwayCalculation(reservedPlacement , currentX, currentY  + direction, currentLinkage + 1, direction)
        else:
            return currentLinkage
    else:
        if(currentY + direction < 4 and reservedPlacement[currentX][currentY + direction] == 'HWY'):
            return reservedHighwayCalculation(reservedPlacement , currentX, currentY  + direction, currentLinkage + 1, direction)
        else:
            return currentLinkage
# See the current score
def reservedSeeCurrentScore(reservedState):
    reservedTotal = {   #calculate the score in a list
        'BCH': [],
        'FAC': [],
        'HSE': [],
        'SHP': [],
        'HWY': []
    }

    reservedTotalScore = 0
    reservedPlacement = reservedState['placements']
    # Adding of scores
    for reservedX, x in enumerate(reservedPlacement):  #enumerate to increase the count of the amount of placement of buildings
        for reservedY, y in enumerate(x):
            if(y == 'BCH'):
                # Column A or D
                if(y == 0 or y == 3):
                    reservedTotal[y].append(3)
                else:
                    reservedTotal[y].append(1)  #calculate the scoring for BCH
            elif(y == 'FAC'):
                # More than 4
                if(sum(reservedTotal[y]) >= 16):
                    reservedTotal[y].append(1)
                else:
                    #Less than or equal to 4
                    if(sum(reservedTotal[y]) == 0):
                        reservedTotal[y].append(1)
                    elif(sum(reservedTotal[y]) == 1):
                        reservedTotal[y].append(3)
                    elif(sum(reservedTotal[y]) == 4):
                        reservedTotal[y].append(5)
                    elif(sum(reservedTotal[y]) == 9):
                        reservedTotal[y].append(7)  #Calculate the scoring for FAC
            elif(y == 'HSE'):
                # Side check
                reservedTS = 0
                if((reservedX - 1) > -1 and (reservedState["placements"][reservedX - 1][reservedY] == "SHP") or (reservedState["placements"][reservedX - 1][reservedY] == "HSE")): #If it is next to a HSE or SHP -- +1
                    reservedTS += 1
                if((reservedX + 1) < 4):
                    if(reservedState["placements"][reservedX + 1][reservedY] == "SHP") or (reservedState["placements"][reservedX + 1][reservedY] == "HSE"):
                        reservedTS += 1
                if((reservedY - 1) > -1 and (reservedState["placements"][reservedX][reservedY - 1] == "SHP") or (reservedState["placements"][reservedX][reservedY - 1] == "HSE")):
                    reservedTS += 1
                if((reservedY + 1) < 4):
                    if((reservedState["placements"][reservedX][reservedY + 1] == "SHP") or (reservedState["placements"][reservedX][reservedY + 1] == "HSE")):
                        reservedTS += 1
                if((reservedX - 1) > -1 and (reservedState["placements"][reservedX - 1][reservedY] == "BCH")): #If it is next to a BCH -- +2
                    reservedTS += 2
                if((reservedX + 1) < 4 and (reservedState["placements"][reservedX + 1][reservedY] == "BCH")):  #checks 4 direction
                    reservedTS += 2
                if((reservedY - 1) > -1 and (reservedState["placements"][reservedX][reservedY - 1] == "BCH")):
                    reservedTS += 2
                if((reservedY + 1) < 4 and (reservedState["placements"][reservedX][reservedY + 1] == "BCH")):
                    reservedTS += 2
                reservedTotal[y].append(reservedTS)
            elif(y == 'SHP'):
                #side check
                reservedAdded = [] #special list so no repeated buildings will affect the total points for each SHP
                if((reservedX - 1) > -1):
                    if(reservedState["placements"][reservedX - 1][reservedY] not in reservedAdded):
                        reservedAdded.append(reservedState["placements"][reservedX - 1][reservedY])
                if((reservedX + 1) < 4):
                    if(reservedState["placements"][reservedX + 1][reservedY] not in reservedAdded):
                        reservedAdded.append(reservedState["placements"][reservedX - 1][reservedY])
                if((reservedY - 1) > -1):
                    if(reservedState["placements"][reservedX][reservedY - 1] not in reservedAdded):
                        reservedAdded.append(reservedState["placements"][reservedX - 1][reservedY])
                if((reservedY + 1) < 4):
                    if(reservedState["placements"][reservedX][reservedY + 1] not in reservedAdded):
                        reservedAdded.append(reservedState["placements"][reservedX - 1][reservedY])
                reservedTotal[y].append(len(reservedAdded))
            elif(y == 'HWY'):
                reservedTS = reservedHighwayCalculation(reservedPlacement , reservedX, reservedY, 1, -1) + reservedHighwayCalculation(reservedPlacement , reservedX, reservedY, 0, 1) #runs function that calculate HWY
                reservedTotal[y].append(reservedTS)
    
    # Displaying of scores
    for reserved in reservedTotal:
        reservedScores = reservedTotal[reserved]
        reservedSum = 0
        reservedString = ""
        for index , reservedScore in enumerate(reservedScores): #increases index without the need to add +=1 for index
            if(index == 0):
                reservedString += str(reservedScore)
            else:
                reservedString += " + " + str(reservedScore)
            reservedSum += reservedScore
        reservedString += " = " + str(reservedSum)
        print(f"{reserved}: {reservedString}")
        reservedTotalScore += reservedSum
    print(f"Total Score: {reservedTotalScore}")

main()
