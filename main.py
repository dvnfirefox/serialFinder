import database as db
import MainPage as mp



if db.createTables():
    db.rawSerialReader('2020')
    db.rawSerialReader('2021')
    db.rawSerialReader('2022')
    db.multipleSerial()
    db.serialSeries()
    db.simpleSerial()

mp.mainPage()


while 1:
    print('enter serial number')
    userInput = input()
    result = db.serialNumberSearch(userInput)
    for row in result:
        print('invoice: ' + row[0] + ' serial number: ' + row[1] + ' date: ' + row[2])