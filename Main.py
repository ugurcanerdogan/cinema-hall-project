import sys
from string import ascii_uppercase

try:
    file = sys.argv[1]
    for x in sys.argv:
        print(x)
except IndexError:
    print("Hata.Input verilmedi.")
    exit()
if len(sys.argv)>2:
    print("Lütfen bir tane input giriniz.")
    exit()

outputFile = open("output.txt","w")
hallDic = {}

def printAll(*args,**kwargs):
    global outputFile
    print(*args,**kwargs)
    print(*args,**kwargs,file=outputFile)

class Hall():
    halls={}
    def __init__(self, hallname,size):
        self.hallname = hallname
        self.rows = int(size.split("x")[0])
        self.columns = int(size.split("x")[1])

    def createHall(self):
        Hall.halls[self.hallname] = [["X" for row in range(self.columns)] for column in range(self.rows)]
        printAll("The hall '{}' having {} seats has been created.".format(self.hallname,self.rows*self.columns))

    def sellTicket(self,customer,faretype,*seats):
        for seat in seats:
            if "-" not in seat:
                try:
                    if  Hall.halls[self.hallname][ascii_uppercase.index(seat[0])][int(seat[1:])] == "X":
                        if faretype == "full":
                            Hall.halls[self.hallname][ascii_uppercase.index(seat[0])][int(seat[1:])] = "F"
                        elif faretype == "student":
                            Hall.halls[self.hallname][ascii_uppercase.index(seat[0])][int(seat[1:])] = "S"
                        printAll("Success: {} has bought {} at {}".format(customer,seat,self.hallname))
                    else:
                        printAll("Warning: The seat {} cannot be sold to {} since it was already sold!".format(seat,customer))
                except IndexError:
                    printAll("Error: The hall '{}' has less column/row than the specified index {}!".format(self.hallname,seat))
            else:
                seatNew = seat.split("-")
                try:
                    if all(seat == "X" for seat in Hall.halls[self.hallname][ascii_uppercase.index(seatNew[0][0])][int(seatNew[0][1:3]):int(seatNew[1])]):
                        if int(seatNew[1]) <= self.columns:                           # kapatmayı dene
                            for i in range(int(seatNew[0][1:3]),int(seatNew[1])):
                                Hall.halls[self.hallname][ascii_uppercase.index(seatNew[0][0])][i] = faretype[0].upper()
                            printAll("Success: {} has bought {} at {}".format(customer,seat,self.hallname))
                        else:
                            printAll("Error: The hall '{}' has less column/row than the specified index {}!".format(self.hallname,seat))
                    else:
                        printAll("Warning: The seat {} cannot be sold to {} since it was already sold!".format(seat,customer))
                except IndexError:
                    printAll("Error: The hall '{}' has less column/row than the specified index {}!".format(self.hallname,seat))

    def cancelTicket(self,*seats):
        for seat in seats:
            if "-" not in seat:
                try:
                    if  Hall.halls[self.hallname][ascii_uppercase.index(seat[0])][int(seat[1:])] != "X":
                        Hall.halls[self.hallname][ascii_uppercase.index(seat[0])][int(seat[1:])] = "X"
                        printAll("Success: The seat {} at ’{}’ has been canceled and now ready to be sold again".format(seat,self.hallname))
                    else:
                        printAll("Error: The seat {} at ’{}’ has already been free! Nothing to cancel".format(seat,self.hallname))
                except IndexError:
                    printAll("Error: The hall '{}' has less column/row than the specified index {}!".format(self.hallname,seat))
            else:
                seatNew = seat.split("-")
                try:
                    if all(seat != "X" for seat in Hall.halls[self.hallname][ascii_uppercase.index(seatNew[0][0])][int(seatNew[0][1:3]):int(seatNew[1])]):
                        for i in range(int(seatNew[0][1:3]),int(seatNew[1])):
                            Hall.halls[self.hallname][ascii_uppercase.index(seatNew[0][0])][i] = "X"
                        printAll("Success: The seats {} at ’{}’ have been canceled and now ready to be sold again".format(seat,self.hallname))
                    else:
                        for seatNumber in range(int(seatNew[0][1:3]),int(seatNew[1])):
                            if Hall.halls[self.hallname][ascii_uppercase.index(seatNew[0][0])][seatNumber] != "X":
                                Hall.halls[self.hallname][ascii_uppercase.index(seatNew[0][0])][seatNumber] = "X"   ## aşkım denicek
                                printAll("Success: The seat {} at ’{}’ has been canceled and now ready to be sold again".format(seatNew[0][0]+str(seatNumber),self.hallname))
                except IndexError:
                    printAll("Error: The hall '{}' has less column/row than the specified index {}!".format(self.hallname,seat))

    def balance(self):
        message = "Hall report of '{}'".format(self.hallname)
        printAll(message)
        printAll("-"*len(message))
        studentCounter = 0
        fullCounter = 0
        for row in Hall.halls[self.hallname]:
            for seat in row:
                if seat == "F":
                    fullCounter+=1
                elif seat == "S":
                    studentCounter+=1
                else:
                    pass
        printAll("Sum of students = {}, Sum of full fares = {}, Overall = {}".format(studentCounter*5,fullCounter*10,studentCounter*5+fullCounter*10))

    def showHall(self):
        printAll("Printing hall layout of {}".format(self.hallname))
        self.counter = -(26-self.rows)
        for row in Hall.halls[self.hallname][::-1]:
            self.counter -=1
            printAll(ascii_uppercase[self.counter],end=" ")
            for seat in row:
                printAll(seat,end="  ")
            printAll()
        printAll("  ",end="")
        for i in range(self.columns):
            if i < 9:
                printAll(i,end="  ")
            else:
                printAll(i,end=" ")
        printAll()
def operations(file):
    with open(file,"r") as m:
        for command in m.readlines():
            if command.split()[0] == "CREATEHALL":
                if len(command.split()) == 3:
                    if command.split()[1] not in hallDic.keys():
                        if int(command.split()[2].split("x")[0]) < 27:
                            hallDic[command.split()[1]]= Hall(command.split()[1],command.split()[2])
                            hallDic[command.split()[1]].createHall()
                        else:
                            printAll("Error: Number of rows cannot be greater than 26!")
                    else:
                        printAll("Warning: Cannot create the hall for the second time. The cinema has already {}".format(command.split()[1]))
                else:
                    printAll("Error: Amount of parameters for creating a hall is not valid!")

            elif command.split()[0] == "SELLTICKET":
                if command.split()[3] in hallDic.keys():
                    if len(command.split()) < 5:
                        printAll("Error: Not enough parameters for selling ticket!")
                    else:
                        if command.split()[2] == "full" or command.split()[2] == "student":
                            hallDic[command.split()[3]].sellTicket(command.split()[1],command.split()[2],*command.split()[4:])
                        else:
                            printAll("Error: {} is not a valid fare type!".format(command.split()[2]))
                else:
                    printAll("Error: There is no such hall that specified with name {} !".format(command.split()[3]))

            elif command.split()[0] == "CANCELTICKET":
                if command.split()[1] in hallDic.keys():
                    if len(command.split()) < 3:
                        printAll("Error: Not enough parameters for cancelling ticket!")
                    else:
                        hallDic[command.split()[1]].cancelTicket(*command.split()[2:])
                else: printAll("Error: There is no such hall that specified with name {} !".format(command.split()[1]))

            elif command.split()[0] == "BALANCE":
                for hall in command.split()[1:]:
                    if hall in hallDic.keys():
                        hallDic[hall].balance()
                    else: printAll("Error: There is no such hall that specified with name {} !".format(hall))

            elif command.split()[0] == "SHOWHALL":
                if len(command.split()) == 2:
                    if command.split()[1] in hallDic.keys():
                        hallDic[command.split()[1]].showHall()
                    else: printAll("Error: There is no such hall that specified with name {} !".format(command.split()[1]))

            else: printAll("UNDEFINED COMMAND")

operations(file)
outputFile.close()




