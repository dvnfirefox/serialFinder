import pandas as pd
import sqlite3


excelInput = '2015-2021.xlsx'

try:
    dbcon = sqlite3.connect('order.db')
    cursor = dbcon.cursor()
    dbcon.commit()
except Exception as e:
    print(f"error : {e}")

def createTables():
    create = 0
    try:
        cursor.execute("CREATE TABLE serialNumberRaw(invoice, serialNumber, buyDate)")
        cursor.execute("CREATE TABLE serialNumber(invoice, serialNumber, buyDate)")
        dbcon.commit()
        create = 1
    except Exception as e:
        print(f"error : {e}")
    return create


def rawSerialReader(sheetName):
    try:
        sheet = pd.read_excel(excelInput, sheet_name=sheetName)
        sheet['Serial #'] = sheet['Serial #'].astype(str)
        sheet['Invoice'] = sheet['Invoice'].astype(str)
        sheet['buyDate'] = sheet['buyDate'].astype(str)
        serialRaw = sheet[['Invoice', 'Serial #', 'buyDate']]
        for index, row in serialRaw.iterrows():
            invoice = row['Invoice']
            serial = row['Serial #']
            buyDate = row['buyDate']
            if "nan" not in serial:
                invoice = invoice.split('.', 1)[0]
                cursor.execute("INSERT INTO serialNumberRaw VALUES(?, ?, ?)", (invoice, serial.replace('\xa0','').replace('\n','&'), buyDate))
        dbcon.commit()
    except Exception as e:
        print(f"error : {e}")
    pass

def simpleSerial():
    serial = cursor.execute("Select * from serialNumberRaw WHERE serialNumber NOT LIKE '%/%' AND serialNumber NOT LIKE '%&%' AND serialNumber NOT LIKE '%,%' AND serialNumber NOT LIKE '-'")
    rows = serial.fetchall()
    for row in rows:
        invoice = row[0]
        serial = row[1]
        buyDate = row[2]

        if len(serial) >= 1:
            cursor.execute("INSERT INTO serialNumber VALUES(?, ?, ?)", (invoice, serial, buyDate))
    cursor.execute("DELETE FROM serialNumberRaw WHERE serialNumber NOT LIKE '%/%' AND serialNumber NOT LIKE '%&%' AND serialNumber NOT LIKE '%,%' AND serialNumber NOT LIKE '-'")
    dbcon.commit()

def multipleSerial():
    serial = cursor.execute("SELECT * FROM serialNumberRaw WHERE serialNumber Like '%&%'")
    rows = serial.fetchall()
    for row in rows:
        invoice = row[0]
        serial = row[1]
        buyDate = row[2]
        serialsplit = serial.split('&')
        for i in serialsplit:
            output = i.replace(' ', '').replace(' ', '')
            cursor.execute("INSERT INTO serialNumberRaw VALUES(?, ?, ?)", (invoice, output, buyDate))
    cursor.execute("DELETE FROM serialNumberRaw WHERE serialNumber Like '%&%'")
    dbcon.commit()

def serialSeries():
    serials = cursor.execute("SELECT * FROM serialNumberRaw WHERE serialNumber LIKE '%/%' AND serialNumber NOT LIKE '-'")
    rows = serials.fetchall()
    lastItem = 0
    for row in rows[::-1]:
        invoice = row[0]
        serial = row[1]
        buyDate = row[2]
        serialsplit = serial.split('/')
        if len(serialsplit[0]) < 5:
            lastItem = serialsplit
        if lastItem != 0:
            serialsplit = serialTabJoiner(serialsplit, lastItem)
            lastItem = 0
        else:
            completeSerial = serialSplitter(serialsplit)
            for i in completeSerial:
                cursor.execute("INSERT INTO serialNumberRaw VALUES(?, ?, ?)", (invoice, i, buyDate))
            lastItem = 0

    cursor.execute("DELETE FROM serialNumberRaw WHERE serialNumber LIKE '%/%' AND serialNumber NOT LIKE '-'")
    dbcon.commit()


def serialTabJoiner(serialEnd, serialStart):
    lastSplitEnd = len(serialStart)
    if len(serialStart[lastSplitEnd - 1]) < len(serialStart[lastSplitEnd - 2]):
        serialStart[lastSplitEnd - 1] = serialStart[lastSplitEnd - 1] + '+' + serialEnd[0]
        serialEnd.pop(0)
    output = serialStart + serialEnd
    return output

def serialSplitter(serials):
    mainSerial = serials[0]
    serials.pop(0)
    output = []
    output.append(mainSerial)
    for serial in serials:
        completeSerial = mainSerial[:-len(serial)] + serial
        output.append(completeSerial)
    return output

def serialNumberSearch(serial):
    serial = '%'+serial+'%'
    result = cursor.execute("SELECT * FROM serialNumber WHERE serialNumber LIKE ?", (serial,))
    return result.fetchall()