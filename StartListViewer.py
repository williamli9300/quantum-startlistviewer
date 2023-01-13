import os

def getFile(): # inputs: pulls './quantum.slx'; outputs: list "lines" of file split by line into list.
    if os.path.isfile('./quantum.slx') == False:
        input("File \"quantum.slx\" does not exist! Please ensure that this executable \
is in the same folder as the start list file.\nPlease press \"Enter\" to close this window.")
        sys.exit()
    fileObj = open('./quantum.slx', 'r')
    lines = fileObj.read().splitlines()
    fileObj.close()
    #print(lines)
    return lines

def getFormat():
    print("What is your pool configuration? \n \
   - 1: 1-4 \n \
   - 2: 1-6 \n \
   - 3: 1-8 \n \
   - 4: 0-9")
    poolconfig = input("Please enter a number from 1 to 4: \n")
    values = ["1", "2", "3", "4"]
    if poolconfig not in values:
        print("Error: not an acceptable value.")
        poolconfig = getFormat()
    return int(poolconfig)

def getFirst(l):
    first = int(input("What is the number of the first event you would like to see? \n"))
    firstInL = False
    firstCounter = 0
    for i in l:
        firstCounter += 1
        if first == int(i[0][0]):
            firstInL = True
            break
        
    if firstInL == False:
        print("That event is outside of the start list's range. Please try again.")
        first = getFirst(l)
    return firstCounter

def getLast(l):
    last = int(input("What is the number of the last event you would like to see? \n"))
    lastInL = False
    lastCounter = 0
    for i in l:
        lastCounter += 1
        if last == int(i[0][0]):
            lastInL = True
            break
        
    if lastInL == False:
        print("That event is outside of the start list's range. Please try again.")
        last = getLast(l)
    return lastCounter

def splitIntoEvents(l):
    outList = []
    currentEvent = []
    currentHeat = []
    currentHeatNum = "empty"
    currentEventNum = 0
    isRelay = False
    counter = 1
    relayMembers = []
    laneNum = 0
    currentLane = []
    for i in range(len(l)):
   
        if l[i][0].isnumeric(): #                           # if currently on heat/event line
            if "relay" in (l[i]).lower():
                isRelay = True
            else:
                isRelay = False
                
            currentLine = l[i].split(";") #                 # split heat/event line into 
            if currentLine[1] == "1": #                     # if currently processing first heat of event
                currentHeatNum = currentLine[1] #              # set "currentHeatNum" to current heat number
                currentEvent.append(currentHeat)
                currentHeat = []
                currentHeat.append(currentHeatNum)
                outList.append(currentEvent) #              # add current event to master list
                currentEvent = [] #                         # reset current event list
                currentEventNum = int(currentLine[0]) #     # set event number of current event
                eventHeader = [] #                          # create list for event header
                evtnum = str(currentEventNum).rjust(3, "0")
                eventHeader.append(evtnum) #                # add event number to event header
                eventHeader.append(currentLine[2]) #        # add P/F/T to event header
                eventHeader.append(currentLine[3]) #        # add event name to event header
                currentEvent.append(eventHeader) #          # add event header to first event
            else:
                currentHeatNum = currentLine[1] #              # set "currentHeatNum" to current heat number
                currentEvent.append(currentHeat)
                currentHeat = []
                currentHeat.append(currentHeatNum)
            
        else: #                                             # if current line is not header line
            if isRelay == False: #                          # if current event is not relay
                currentLine = l[i].split(";") #             # split heat/event line into list
                currentLane = []
                laneNum = currentLine[2]
                rawName = currentLine[4] + " " + currentLine[5]
                name = rawName.ljust(35)
                shortClub = currentLine[6].ljust(8)
                currentLane.append(laneNum)
                currentLane.append(name)
                currentLane.append(shortClub)
                currentHeat.append(currentLane)

            else: #                                         # if current event is a relay:
                currentLine = l[i].split(";")
                orderNum = currentLine[3]
                laneNum = currentLine[2]
                relayInfo = []
                if orderNum == "0":
                    relayMembers = []
                    currentLane = []
                    relayName = currentLine[4].ljust(8)
                    teamName = currentLine[7].ljust(35)
                    relayInfo.append(laneNum)
                    relayInfo.append(relayName)
                    relayInfo.append(teamName)
                    currentLane.append(relayInfo)
                else:
                    member = []
                    rawName = currentLine[4] + ", " + currentLine[5]
                    name = rawName.ljust(32)
                    subtract = int(orderNum)
                    relayHeadLine = l[i-subtract].split(";")
                    shortClub = relayHeadLine[6]
                    member.append(orderNum)
                    member.append(name)
                    member.append(shortClub)
                    relayMembers.append(member)
                if i < len(l) - 1:
                    splitlist = l[i+1].split(";")
                    if splitlist[2] != laneNum:
                        currentLane.append(relayMembers)
                        currentHeat.append(currentLane)
        if i == len(l) - 1:
            currentEvent.append(currentHeat)
            outList.append(currentEvent)
                
    return outList

def format_(l):
    
    l.pop(0)

    t = ""

    a = 0
    b = 0

    n = getFormat()

    if n == 1:
        a = 1
        b = 5
    elif n == 2:
        a = 1
        b = 7
    elif n == 3:
        a = 1
        b = 9
    elif n == 4:
        a = 0
        b = 10

    first = getFirst(l) -1
    last = getLast(l)
    print("".ljust(100, "="))
    print("".ljust(100, "+"))
    print("".ljust(100, "="))
    for i in range(first, last):

        if "relay" not in l[i][0][2].lower():
            name = "".ljust(35)
            club = "".ljust(8)

            for heatNumber in range(1, len(l[i])):
                #print(l)
                event = l[i][0][0]
                if l[i][0][1] == "P":
                    t = "Prelim"
                elif l[i][0][1] == "T":
                    t = "Timed Final"
                elif l[i][0][1] == "F":
                    t = "Final"
                evtType = t.ljust(12)
                evtName = l[i][0][2].ljust(29)
                heatNumInt = l[i][heatNumber][0]
                heatNumStr = heatNumInt.rjust(3, "0")
                spacer = "".ljust(70, "-")
                evtHead = spacer + "\n" + "Event " + event + " | Heat " + heatNumStr + " | " + evtName + " | " + evtType + "\n" + spacer
                print(evtHead)
                for poolLane in range(a, b):
                    for laneNumber in range(1, len(l[i][heatNumber])):
                        if l[i][heatNumber][laneNumber][0] == str(poolLane):
                            name = l[i][heatNumber][laneNumber][1]
                            club = l[i][heatNumber][laneNumber][2]
                    laneText = "| " + str(poolLane) + " | " + name + " | " + club + " |"
                    name = "".ljust(35)
                    club = "".ljust(8)
                    print(laneText)
        else:
            club = "".ljust(35)
            relay = "".ljust(8)
            swimmerName = "".ljust(32)
            shortClub = "".ljust(8)
            names = ""
            swimmers = []
            for heatNumber in range(1, len(l[i])):
                evtType = t.ljust(12)
                evtName = l[i][0][2].ljust(28)
                heatNumInt = l[i][heatNumber][0]
                heatNumStr = heatNumInt.rjust(3, "0")
                spacer = "".ljust(70, "-")
                evtHead = spacer + "\n" + "Event " + event + " | Heat " + heatNumStr + " | " + evtName + " | " + evtType + "\n" + spacer
                print(evtHead)
                for poolLane in range(a, b):
                    for laneNumber in range(1, len(l[i][heatNumber])):
                        if l[i][heatNumber][laneNumber][0][0]  == str(poolLane):
                            club = l[i][heatNumber][laneNumber][0][2]
                            relay = l[i][heatNumber][laneNumber][0][1]
                            for swimmer in range (0, 4):
                                swimmerName = l[i][heatNumber][laneNumber][1][swimmer][1]
                                shortClub = l[i][heatNumber][laneNumber][1][swimmer][2].ljust(6)
                                addRow = "\n|   | " + str(swimmer) + ") " + swimmerName + "   - " + shortClub + " |"
                                swimmers.append(addRow)
                            names = "".join(swimmers)
                    laneText = "| " + str(poolLane) + " | " + club + " | " + relay + " |" + names
                    print(laneText)
                    club = "".ljust(35)
                    relay = "".ljust(8)
                    swimmerName = "".ljust(32)
                    shortClub = "".ljust(8)
                    names = ""
                    swimmers = []
                        
                        
            
        
lines = getFile()
events = splitIntoEvents(lines)
format_(events)
input("Press \"Enter\" to close window. \n")
