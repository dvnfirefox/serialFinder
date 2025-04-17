import pandas as pd
import sqlite3

excelInput = '2015-2021.xlsx'
try:
    dbcon = sqlite3.connect('order.db')
    cursor = dbcon.cursor()
    cursor.execute("CREATE TABLE serialNumberRaw(invoice, serialNumber)")
    cursor.execute("CREATE TABLE serialNumber(invoice, serialNumber)")
except Exception as e:
    print(f"error : {e}")



try:
    sheet2020 = pd.read_excel(excelInput, sheet_name='2020')
    sheet2020['Serial #'] = sheet2020['Serial #'].astype(str)
    sheet2020['Invoice'] = sheet2020['Invoice'].astype(str)
    serialRaw = sheet2020[['Invoice', 'Serial #']]
    for index, row in serialRaw.iterrows():
        invoice = row['Invoice']
        serial = row['Serial #']
        if ("nan" not in invoice and "nan" not in serial
        ):
            invoice = invoice.split('.', 1)[0]
            print(invoice, serial)
            cursor.execute("INSERT INTO serialNumberRaw VALUES(?, ?)", (invoice, serial))
    dbcon.commit()
except Exception as e:
    print(f"error : {e}")


