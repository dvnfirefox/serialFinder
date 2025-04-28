import tkinter as tk
import database as db

def search(input):
    try:
        resultListBox.delete(0, tk.END)
        result = db.serialNumberSearch(input)
        if result == []:
            raise Exception
        inputBox.delete(0, tk.END)
        for row in result:
            resultListBox.insert(tk.END, 'invoice: ' + row[0] + ' Serial: ' + row[1] + ' Date: ' + row[2])
    except:
        resultListBox.insert(tk.END, 'No results found')


def mainPage():
    global resultListBox
    global inputBox
    root = tk.Tk()
    root.title('Serial Finder')
    root.geometry('400x300')
    inputFrame = tk.Frame(root)
    inputFrame.pack()

    inputBox = tk.Entry(inputFrame, width=20)
    inputBox.pack()

    inputButton = tk.Button(inputFrame, text='Find', command=lambda: search(inputBox.get()))
    inputButton.pack()

    global resultListBox
    resultListBox = tk.Listbox(root, width=80, height=10)
    resultListBox.pack()
    root.mainloop()