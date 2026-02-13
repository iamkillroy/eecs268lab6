import time
class World:
    def __init__(self, file) -> None:
        """Creates a world for THE BLOB!!! to terrorize"""
        fileText = open(file, "r").read()
        fileList = fileText.split("\n")
        #constant that checks if the blob
        # can move through it or nah
        self.canMove = {"S": True, "P": True, "#": False, "@": True, "B": False}
        #let's read this format
        # line 0 is the dimensions so
        # this code will get the dimensions and then assign them to
        # the file's dimensions
        self.w, self.h = [int(dimension) for dimension in fileList[0].split(" ")] #0th line
        self.blobY, self.blobX = [int(dimension) for dimension in fileList[1].split(" ")] #0th line
        print(self.blobX)
        print(self.blobY)
        #based on this, we will make a list containing lists, organized like
        # [ [self.w * " "],
        #   [self.w * " "]] where the heigh is the nth element in the parent list
        # and the width is length of the widht
        self.world = [[" " for _ in range(self.w)] for _ in range(self.h)] #makes it like how i said before
        #now we iterate through the world list, we only care about the position
        for worldIterator, _ in enumerate(self.world):
            #the file position of x is + 2 because of the world size and blob position
            filePositionOfX = worldIterator + 2
            #set the value in self.world (the list) to the list of each char in the
            # fileList as the filePositionOfX
            self.world[worldIterator] = [a for a in list(fileList[filePositionOfX])]
        #Check for exceptions
        if self.w < 1 and self.h < 1: raise Exception("Blobfile too small")
        if self.blobX > self.w or self.blobY > self.h: raise Exception("Blob is out of the world")
        #set the people count!
        self.peopleInTummy = 0
    def get(self, x, y):
        """Get's a value in the world"""
        return self.world[y][x]
    def checkWhereICanMove(self, x ,y) -> list[bool, list[int, int]]:
        """Checks if the blob can move, and returns a list of a tuple of coords where he can"""
        iCanMoveTimeToEatPeople = False
        #the if else is bound scoping to prevent the cool but annoying
        # list attr that -1 indexes will loop to the front (and also
        # that greater list index will go all the way around)
        coordsWhereICanGo = []
        if not y == 0:
            up = self.canMove[self.world[y - 1][x]]
            if up: coordsWhereICanGo.append([x, y-1])
        else:
            up = False
        if not y == self.h-1:
            down = self.canMove[self.world[y + 1][x]]
            if down: coordsWhereICanGo.append([x, y+1])
        else:
            down = False
        if not x == 0:
            left = self.canMove[self.world[y][x-1]]
            if left: coordsWhereICanGo.append([x-1, y])
        else:
            left = False
        if not x == self.w-1:
            right = self.canMove[self.world[y][x+1]]
            if right: coordsWhereICanGo.append([x+1, y])
        else:
            right = False
        #print(f"up {up} down {down} left{left} right {right}")
        if up or down or left or right:
            iCanMoveTimeToEatPeople = True
        return [iCanMoveTimeToEatPeople, coordsWhereICanGo]
    def display(self):
        xdisplay = " ".join(str(i) for i in range(self.h )) + "\n" + "---" * self.h
        print(xdisplay)
        iy = 0
        for y in self.world:
            for x in y:
                print(x + " ", end="")
            print(str(iy) + "\n")
            iy += 1
    def set(self, x, y, value):
        self.world[y][x] = value
    def start(self):
        self.go(self.blobX, self.blobY)
    def go(self, x, y):
        time.sleep(1)
        """Moves at one step a second"""
        self.display()
        print(f"I'm a blob at {x}, {y}")
        if self.get(x,y) == "P": #increment people in tummy by 1
            self.peopleInTummy += 1
        self.set(x, y,"B")
        self.display()

        #okay we're going to move the blob from his startin coords and return a list map
        canIMove, whereICanMove = self.checkWhereICanMove(x, y)
        if canIMove:
            for positions in whereICanMove:
                self.go(positions[0], positions[1])
