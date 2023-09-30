#!/usr/bin/env python3

import sqlite3
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from datetime import datetime
import os


# base_dir = os.path.dirname(__file__)
# conn_path = os.path.join(base_dir, '')


import os
import sys

config_name = 'database.db'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
conn_path = (application_path+"/database.db")

conn = sqlite3.connect(conn_path)
c = conn.cursor() 

###### DATA BASE CODE

def main():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS shipments (
                    name text,
                    supplier text,
                    date text,
                    invoiceNumber text,
                    state integer,
                    price real,
                    units real,
                    pricepunit real,
                    storageTemp real,
                    deliveryTemp real, 
                    time integer
                    )""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS stock (
                    name text,
                    supplier text,
                    pricepunit real,
                    units real,
                    stamp real
                    )""")

main()

font1 = ("SF", 15)


### SETTING WINDOW
window = ctk.CTk()
window._set_appearance_mode("System")
window.title('Stock Management')
window.resizable(False, False)
def centreWindow(window, width, height):
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2 * frm_width
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = (window.winfo_screenheight() // 2 - win_height // 2) - 50
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
centreWindow(window, 1000, 600)
window.configure(fg_color = ("azure2", "gray16"))


def incomingShipMenu(state2=1, name="", supplier="", date2="", invoiceNumber="", price="", units="", time=0):
    window2 = ctk.CTk()
    window._set_appearance_mode("System")
    if(state2 == 1):
        title = "Add Stock"
    else:
        title = "Update Stock"
    window2.title(title)
    window2.resizable(False, False)
    centreWindow(window2, 800, 320)
    window2.configure(fg_color = ("azure2", "gray16"))

    def updateProduct(name, supplier, pricepunit, units):
        with conn:
            c.execute("""UPDATE stock SET pricepunit = ?
                    WHERE name = ? AND supplier = ?""", (float(pricepunit), name, supplier))
            c.execute("""UPDATE stock SET units = ?
                    WHERE name = ? AND supplier = ?""", (float(units), name, supplier))

    def createShipment(name, supplier, date, invoiceNumber, state, price, units, storageTemp = 99, deliveryTemp = 99):
        with conn:
            if state == 1:
                try:
                    now = datetime.now()
                    date_string = now.strftime("%Y%m%d%H%M%S")
                    date_int = int(date_string)
                    c.execute("INSERT INTO shipments (name, supplier, date, invoiceNumber, state, price, units, pricepunit, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, supplier, date, invoiceNumber, state, float(price), float(units), round(float(price)/float(units), 4), date_int))
                    c.execute("SELECT pricepunit, units FROM stock WHERE name = ? AND supplier=?", (name, supplier))
                    temp = c.fetchone()
                    updateProduct(name, supplier, (float(temp[0])), round((float(temp[1]) + float(units)), 4))
                    return True
                except:
                    messagebox.showerror(title="Error", message="This product does not exist")
                    return False
                    


    def updateShipment(name, supplier, date, invoiceNumber, price, newUnits, oldUnits):
        try:
            with conn:
                c.execute("SELECT pricepunit, units FROM stock WHERE name = ?", (name,))
                temp = c.fetchone()
                change = float(newUnits) - float(oldUnits)
                updateProduct(name, supplier, (float(temp[0])), round((float(temp[1]) + change), 4))
                c.execute("UPDATE shipments SET name = ?, supplier = ?, date = ?, invoiceNumber = ?, price = ?, units = ?, pricepunit= ? WHERE time = ?", (name, supplier, date, invoiceNumber, float(price), float(newUnits), round(float(price)/float(newUnits), 4), time))
                return True
        except:
            messagebox.showerror(title="Error", message="This product does not exist")
            return False


    def submitIncoming(e=0):
        if (name_entry.get()=="" or date_entry.get()=="" or supplier_entry.get()=="" or price_entry.get()=="" or invoice_entry.get()=="" or units_entry.get()==""):
            messagebox.showerror(title="Error", message="Please fill in all the boxes")
        elif (state2==1):
            if(createShipment(name_entry.get(), supplier_entry.get(), date_entry.get(), invoice_entry.get(), 1, price_entry.get(), units_entry.get())):
                window2.destroy()
                display_data()
        else:
            if(updateShipment(name_entry.get(), supplier_entry.get(), date_entry.get(), invoice_entry.get(), price_entry.get(), units_entry.get(), units)):
                window2.destroy()
                display_data()

    def clearIncoming():
        name_entry.delete(0,'end')
        supplier_entry.delete(0,'end')
        price_entry.delete(0,'end')
        invoice_entry.delete(0, 'end')
        units_entry.delete(0,'end')


    name_label=ctk.CTkLabel(window2, text="Product Name", font=font1)
    name_label.place(x=60, y=40)
    name_entry = ctk.CTkEntry(window2, font=font1, width=260)
    name_entry.insert(0, name)
    name_entry.place(x=170, y=40)
    date_label=ctk.CTkLabel(window2, text="Date", font=font1)
    date_label.place(x=470, y=40)
    date_entry = ctk.CTkEntry(window2, font=font1, width=180)
    if(date2==""):
        date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
    else:
        date_entry.insert(0, date2)
    date_entry.place(x=520, y=40)
    supplier_label=ctk.CTkLabel(window2, text="Supplier Name", font=font1)
    supplier_label.place(x=60, y=100)
    supplier_entry = ctk.CTkEntry(window2, font=font1, width=250)
    supplier_entry.insert(0, supplier)
    supplier_entry.place(x=180, y=100)
    price_label=ctk.CTkLabel(window2, text="Price", font=font1)
    price_label.place(x=470, y=100)
    price_entry = ctk.CTkEntry(window2, font=font1, width=180)
    price_entry.insert(0, price)
    price_entry.place(x=520, y=100)
    invoice_label=ctk.CTkLabel(window2, text="Invoice Number", font=font1)
    invoice_label.place(x=60, y=160)
    invoice_entry = ctk.CTkEntry(window2, font=font1, width=240)
    invoice_entry.insert(0, invoiceNumber)
    invoice_entry.place(x=190, y=160)
    units_label=ctk.CTkLabel(window2, text="Units", font=font1)
    units_label.place(x=470, y=160)
    units_entry = ctk.CTkEntry(window2, font=font1, width=180)
    units_entry.insert(0, units)
    units_entry.place(x=520, y=160)

    button = ctk.CTkButton(window2, text="Enter", command=submitIncoming)
    button.place(x=450, y=240)
    button2 = ctk.CTkButton(window2, text="Clear", command=clearIncoming)
    button2.place(x=210, y=240)

    window2.bind("<Return>", submitIncoming)

    window2.mainloop()

def outgoingShipMenu(state2=1, name="", supplier="", date2="", invoiceNumber="", price="", units="", time=0, tempStore="", tempShip=""):
    window2 = ctk.CTk()
    window._set_appearance_mode("System")
    if(state2 == 1):
        title = "Add Stock"
    else:
        title = "Update Stock"
    window2.title(title)
    window2.resizable(False, False)
    centreWindow(window2, 800, 380)
    window2.configure(fg_color = ("azure2", "gray16"))

    def updateProduct(name, supplier, pricepunit, units):
        with conn:
            c.execute("""UPDATE stock SET pricepunit = ?
                    WHERE name = ? AND supplier = ?""", (float(pricepunit), name, supplier))
            c.execute("""UPDATE stock SET units = ?
                    WHERE name = ? AND supplier = ?""", (float(units), name, supplier))

    def createShipment(name, supplier, date, invoiceNumber, state, price, units, storageTemp = 99, shippingTemp = 99):
        with conn:
            if state == 2:
                try:
                    now = datetime.now()
                    date_string = now.strftime("%Y%m%d%H%M%S")
                    date_int = int(date_string)
                    c.execute("INSERT INTO shipments (name, supplier, date, invoiceNumber, state, price, units, pricepunit, storageTemp, deliveryTemp, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, supplier, date, invoiceNumber, state, float(price), float(units), round(float(price)/float(units), 4), float(storageTemp), float(shippingTemp), date_int))
                    c.execute("SELECT pricepunit, units FROM stock WHERE name = ? AND supplier=?", (name, supplier))
                    temp = c.fetchone()
                    updateProduct(name, supplier, (float(temp[0])), round((float(temp[1]) - float(units)),4))
                    return True
                except:
                    messagebox.showerror(title="Error", message="This product does not exist")
                    return False
                    


    def updateShipment(name, supplier, date, invoiceNumber, price, newUnits, oldUnits, storeTemp, deliveryTemp):
        try:
            with conn:
                c.execute("SELECT pricepunit, units FROM stock WHERE name = ?", (name,))
                temp = c.fetchone()
                change = float(newUnits) - float(oldUnits)
                updateProduct(name, supplier, (float(temp[0])), round((float(temp[1]) - change),4))                
                c.execute("UPDATE shipments SET name = ?, supplier = ?, date = ?, invoiceNumber = ?, price = ?, units = ?, pricepunit= ?, storageTemp=?, deliveryTemp=? WHERE time = ?", (name, supplier, date, invoiceNumber, float(price), float(newUnits), round(float(price)/float(newUnits), 4), storeTemp, deliveryTemp, time))
                return True
        except:
            messagebox.showerror(title="Error", message="This product does not exist")
            return False


    def submitIncoming(e=0):
        if (tempStore_entry.get()=="" or tempShip_entry.get()==""):
            tempStore=99
            tempShip=99
        else:
            tempStore = tempStore_entry.get()
            tempShip = tempShip_entry.get()

        if (name_entry.get()=="" or date_entry.get()=="" or supplier_entry.get()=="" or price_entry.get()=="" or invoice_entry.get()=="" or units_entry.get()==""):
            messagebox.showerror(title="Error", message="Please fill in all the boxes")
        elif (state2==1):
            if(createShipment(name_entry.get(), supplier_entry.get(), date_entry.get(), invoice_entry.get(), 2, price_entry.get(), units_entry.get(), tempStore, tempShip)):
                window2.destroy()
                display_data2()
        else:
            if(updateShipment(name_entry.get(), supplier_entry.get(), date_entry.get(), invoice_entry.get(), price_entry.get(), units_entry.get(), units, tempStore, tempShip)):
                window2.destroy()
                display_data2()

    def clearIncoming():
        name_entry.delete(0,'end')
        supplier_entry.delete(0,'end')
        price_entry.delete(0,'end')
        invoice_entry.delete(0, 'end')
        units_entry.delete(0,'end')


    name_label=ctk.CTkLabel(window2, text="Product Name", font=font1)
    name_label.place(x=60, y=40)
    name_entry = ctk.CTkEntry(window2, font=font1, width=260)
    name_entry.insert(0, name)
    name_entry.place(x=170, y=40)
    date_label=ctk.CTkLabel(window2, text="Date", font=font1)
    date_label.place(x=470, y=40)
    date_entry = ctk.CTkEntry(window2, font=font1, width=180)
    if(date2==""):
        date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
    else:
        date_entry.insert(0, date2)
    date_entry.place(x=520, y=40)
    supplier_label=ctk.CTkLabel(window2, text="Supplier Name", font=font1)
    supplier_label.place(x=60, y=100)
    supplier_entry = ctk.CTkEntry(window2, font=font1, width=250)
    supplier_entry.insert(0, supplier)
    supplier_entry.place(x=180, y=100)
    price_label=ctk.CTkLabel(window2, text="Price", font=font1)
    price_label.place(x=470, y=100)
    price_entry = ctk.CTkEntry(window2, font=font1, width=180)
    price_entry.insert(0, price)
    price_entry.place(x=520, y=100)
    invoice_label=ctk.CTkLabel(window2, text="Invoice Number", font=font1)
    invoice_label.place(x=60, y=160)
    invoice_entry = ctk.CTkEntry(window2, font=font1, width=240)
    invoice_entry.insert(0, invoiceNumber)
    invoice_entry.place(x=190, y=160)
    units_label=ctk.CTkLabel(window2, text="Units", font=font1)
    units_label.place(x=470, y=160)
    units_entry = ctk.CTkEntry(window2, font=font1, width=180)
    units_entry.insert(0, units)
    units_entry.place(x=520, y=160)


    tempStore_label=ctk.CTkLabel(window2, text="Storage Temp", font=font1)
    tempStore_label.place(x=100, y=220)
    tempStore_entry = ctk.CTkEntry(window2, font=font1, width=100)
    tempStore_entry.insert(0, tempStore)
    tempStore_entry.place(x=250, y=220)

    tempShip_label=ctk.CTkLabel(window2, text="Shipping Temp", font=font1)
    tempShip_label.place(x=400, y=220)
    tempShip_entry = ctk.CTkEntry(window2, font=font1, width=100)
    tempShip_entry.insert(0, tempShip)
    tempShip_entry.place(x=550, y=220)

    button = ctk.CTkButton(window2, text="Enter", command=submitIncoming)
    button.place(x=450, y=300)
    button2 = ctk.CTkButton(window2, text="Clear", command=clearIncoming)
    button2.place(x=210, y=300)

    window2.bind("<Return>", submitIncoming)

    window2.mainloop()

def updateProduct(name, supplier, units, state):
    with conn:
        if (state==1):
            c.execute("SELECT units FROM stock WHERE name = ?", (name,))
            temp = c.fetchone()
            c.execute("""UPDATE stock SET units = ?
                    WHERE name = ? AND supplier = ?""", (round((temp[0] - float(units)),4), name, supplier))
        elif(state==2):
            c.execute("SELECT units FROM stock WHERE name = ?", (name,))
            temp = c.fetchone()
            c.execute("""UPDATE stock SET units = ?
                    WHERE name = ? AND supplier = ?""", (round((temp[0] + float(units)),4), name, supplier)) 
                     
def addShipIn():    
    incomingShipMenu()

def deleteShipIn():
    # try:
        curItem = tv.focus()
        name = tv.item(curItem)["values"][0]
        supplier = tv.item(curItem)["values"][1]
        date = tv.item(curItem)["values"][2]
        invoiceNumber = tv.item(curItem)["values"][3]
        units = tv.item(curItem)["values"][5]
        with conn:
            c.execute("DELETE from shipments WHERE name = ? AND date = ? AND invoiceNumber = ? AND state = 1", (name, date, invoiceNumber))
            updateProduct(name, supplier, units, 1)
            display_data()
    # except:
    #     messagebox.showerror(title="Error", message="Select a shipment to delete")


def addShipOut():
    outgoingShipMenu()

def deleteShipOut():
    try:
        curItem = tv2.focus()
        name = tv2.item(curItem)["values"][0]
        supplier = tv2.item(curItem)["values"][1]
        date = tv2.item(curItem)["values"][2]
        invoiceNumber = tv2.item(curItem)["values"][3]
        units = tv2.item(curItem)["values"][5]
        with conn:
            c.execute("DELETE from shipments WHERE name = ? AND date = ? AND invoiceNumber = ? AND state = ?", (name, date, invoiceNumber, 2))
        updateProduct(name, supplier, units, 2)
        display_data2()
    except:
        messagebox.showerror(title="Error", message="Select a shipment to delete")

def updateShipIn(event):
    currItem = tv.focus()
    with conn:
        c.execute("SELECT * FROM shipments WHERE name = ? AND supplier = ? AND date = ? AND invoiceNumber = ? AND price = ? AND units = ? AND state = ?", (tv.item(currItem)["values"][0], tv.item(currItem)["values"][1], tv.item(currItem)["values"][2], tv.item(currItem)["values"][3], tv.item(currItem)["values"][4], tv.item(currItem)["values"][5], 1))
        temp = c.fetchone()
    incomingShipMenu(2, temp[0], temp[1], temp[2], temp[3], temp[5], temp[6], temp[10])

def updateShipOut(event):
    currItem = tv2.focus()
    with conn:
        c.execute("SELECT * FROM shipments WHERE name = ? AND supplier = ? AND date = ? AND invoiceNumber = ? AND price = ? AND units = ? AND state = ?", (tv2.item(currItem)["values"][0], tv2.item(currItem)["values"][1], tv2.item(currItem)["values"][2], tv2.item(currItem)["values"][3], tv2.item(currItem)["values"][4], tv2.item(currItem)["values"][5], 2))
        temp = c.fetchone()
    outgoingShipMenu(2, temp[0], temp[1], temp[2], temp[3], temp[5], temp[6], temp[10], temp[8], temp[9])

### SETTING TABVIEW
tabview = ctk.CTkTabview(window, width=960, height = 560, fg_color=("azure2", "gray16"))
tabview._segmented_button.configure(font = ("SF", 16))
tabview.grid(column=0, row=0, padx=20, pady=20)

tabview.add("Incoming")
tabview.add("Outgoing")
tabview.add("Stock") 
tabview.add("Products")  
tabview.set("Incoming")

### SETTING TABS

button = ctk.CTkButton(tabview.tab("Incoming"), text="Add Shipment", command=addShipIn)
button.place(x=540, y=450)
button2 = ctk.CTkButton(tabview.tab("Incoming"), text="Delete Shipment", command=deleteShipIn)
button2.place(x=270, y=450)

button3 = ctk.CTkButton(tabview.tab("Outgoing"), text="Add Shipment", command=addShipOut)
button3.place(x=540, y=450)
button4 = ctk.CTkButton(tabview.tab("Outgoing"), text="Delete Shipment", command=deleteShipOut)
button4.place(x=270, y=450)



style = ttk.Style()
style.configure("mystyle.Treeview", font = ("SF", 14))
style.configure("mystle.Treeview.heading", font = ("SF", 16))

def fetch(state):
        if (state==1):
            c.execute("SELECT name, supplier, date, invoiceNumber, price, units, pricepunit FROM shipments WHERE state = ? ORDER BY time DESC", (state,))
            rows = c.fetchall()
            return rows
        elif(state==2):
            c.execute("SELECT name, supplier, date, invoiceNumber, price, units, pricepunit, storageTemp, deliveryTemp FROM shipments WHERE state = ? ORDER BY time DESC", (state,))
            rows = c.fetchall()
            return rows


def incomingStock(state2=1, name="", supplier="", price="", units="", time=0):
    window2 = ctk.CTk()
    window._set_appearance_mode("System")
    if(state2 == 1):
        title = "Add Stock"
    else:
        title = "Update Stock"
    window2.title(title)
    window2.resizable(False, False)
    centreWindow(window2, 800, 240)
    window2.configure(fg_color = ("azure2", "gray16"))


    def createProduct(name, supplier, price, units):
        with conn:
            now = datetime.now()
            date_string = now.strftime("%Y%m%d%H%M%S")
            date_int = int(date_string)
            c.execute("INSERT INTO stock (name, supplier, pricepunit, units, stamp) VALUES (?, ?, ?, ?, ?)", (name, supplier, float(price), float(units), date_int))


    def updateProduct(name, supplier, price, units):
        with conn:
            c.execute("UPDATE stock SET name = ?, supplier = ?, pricepunit = ?, units = ? WHERE stamp = ?", (name, supplier, round(float(price),4), round(float(units),4), time))

    def submitIncoming(e=0):
        if (name_entry.get()=="" or supplier_entry.get()=="" or price_entry.get()=="" or units_entry.get()==""):
            messagebox.showerror(title="Error", message="Please fill in all the boxes")
        elif (state2==1):
            createProduct(name_entry.get(), supplier_entry.get(), price_entry.get(), units_entry.get())
            window2.destroy()
            displayStock()
        else:
            updateProduct(name_entry.get(), supplier_entry.get(), price_entry.get(), units_entry.get())
            window2.destroy()
            displayStock()

    def clearIncoming():
        name_entry.delete(0,'end')
        supplier_entry.delete(0,'end')
        price_entry.delete(0,'end')
        units_entry.delete(0,'end')


    name_label=ctk.CTkLabel(window2, text="Product Name", font=font1)
    name_label.place(x=60, y=40)
    name_entry = ctk.CTkEntry(window2, font=font1, width=260)
    name_entry.insert(0, name)
    name_entry.place(x=170, y=40)
    price_label=ctk.CTkLabel(window2, text="Price", font=font1)
    price_label.place(x=470, y=40)
    price_entry = ctk.CTkEntry(window2, font=font1, width=180)
    price_entry.insert(0, price)
    price_entry.place(x=520, y=40)
    supplier_label=ctk.CTkLabel(window2, text="Supplier Name", font=font1)
    supplier_label.place(x=60, y=100)
    supplier_entry = ctk.CTkEntry(window2, font=font1, width=250)
    supplier_entry.insert(0, supplier)
    supplier_entry.place(x=180, y=100)
    units_label=ctk.CTkLabel(window2, text="Units", font=font1)
    units_label.place(x=470, y=100)
    units_entry = ctk.CTkEntry(window2, font=font1, width=180)
    units_entry.insert(0, units)
    units_entry.place(x=520, y=100)

    button = ctk.CTkButton(window2, text="Enter", command=submitIncoming)
    button.place(x=450, y=170)
    button2 = ctk.CTkButton(window2, text="Clear", command=clearIncoming)
    button2.place(x=210, y=170)

    window2.bind("<Return>", submitIncoming)

    window2.mainloop()

def addProduct():
    incomingStock()

def deleteProduct():
    try:
        curItem = tv3.focus()
        name = tv3.item(curItem)["values"][0]
        supplier = tv3.item(curItem)["values"][1]
        price = tv3.item(curItem)["values"][2]
        units = tv3.item(curItem)["values"][3]
        with conn:
            c.execute("DELETE from stock WHERE name = ? AND supplier = ? AND pricepunit = ? AND units = ?", (name, supplier, price, units))
        displayStock()
    except:
        messagebox.showerror(title="Error", message="Select a product to delete")

def updateStock(event):
    currItem = tv3.focus()
    with conn:
        c.execute("SELECT * FROM stock WHERE name = ? AND supplier = ? AND pricepunit = ? AND units = ?", (tv3.item(currItem)["values"][0], tv3.item(currItem)["values"][1], tv3.item(currItem)["values"][2], tv3.item(currItem)["values"][3]))
        temp = c.fetchone()
    incomingStock(2, temp[0], temp[1], temp[2], temp[3], temp[4])

def fetchStock():
    c.execute("SELECT name, supplier, pricepunit, units FROM stock ORDER BY name ASC")
    rows = c.fetchall()
    return rows

def displayStock():
    tv3.delete(*tv3.get_children())
    for row in fetchStock():
        row = row + (row[2]*row[3],)
        tv3.insert("", 'end', values=row)

def stockTree():
    global tv3
    tv3 = ttk.Treeview(tabview.tab("Stock"), columns=(1,2,3,4,5), show="headings", style="mystyle.Treeview", height=21)
    tv3.heading("1", text="Product Name")
    tv3.column("1", width=230)
    tv3.heading("2", text="Supplier")
    tv3.column("2", width=230)
    tv3.heading("3", text="Price per Unit")
    tv3.column("3", width=160)
    tv3.heading("4", text="Units")
    tv3.column("4", width=160)
    tv3.heading("5", text="Total Stock")
    tv3.column("5", width=160)
    tv3.place(x=10, y=15)
    tv3.bind("<Double-1>", updateStock)
    scrollbar = ttk.Scrollbar(tabview.tab("Stock"), orient="vertical", command=tv3.yview)
    tv3.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(x=930, y=39, height=382)
    displayStock()
stockTree()

def display_data():
    tv.delete(*tv.get_children())
    for row in fetch(1):
        tv.insert("", 'end', values=row)
    displayStock()

def display_data2():
    tv2.delete(*tv2.get_children())
    for row in fetch(2):
        tv2.insert("", 'end', values=row)
    displayStock()

def incomingTree():
    global tv
    tv = ttk.Treeview(tabview.tab("Incoming"), columns=(1,2,3,4,5,6,7), show="headings", style="mystyle.Treeview", height=21)
    tv.heading("1", text="Product Name")
    tv.column("1", width=180)
    tv.heading("2", text="Supplier")
    tv.column("2", width=180)
    tv.heading("3", text="Date")
    tv.column("3", width=100)
    tv.heading("4", text="Invoice Number")
    tv.column("4", width=160)
    tv.heading("5", text="Price")
    tv.column("5", width=100)
    tv.heading("6", text="Units")
    tv.column("6", width=100)
    tv.heading("7", text="Price per Units")
    tv.column("7", width=115)
    tv.place(x=10, y=15)
    tv.bind("<Double-1>", updateShipIn)
    scrollbar = ttk.Scrollbar(tabview.tab("Incoming"), orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(x=930, y=39, height=382)
    display_data()
incomingTree()

def outgoingTree():
    global tv2
    tv2 = ttk.Treeview(tabview.tab("Outgoing"), columns=(1,2,3,4,5,6,7,8,9), show="headings", style="mystyle.Treeview", height=21)
    tv2.heading("1", text="Product Name")
    tv2.column("1", width=170)
    tv2.heading("2", text="Supplier")
    tv2.column("2", width=160)
    tv2.heading("3", text="Date")
    tv2.column("3", width=90)
    tv2.heading("4", text="Invoice Number")
    tv2.column("4", width=130)
    tv2.heading("5", text="Price")
    tv2.column("5", width=70)
    tv2.heading("6", text="Units")
    tv2.column("6", width=70)
    tv2.heading("7", text="Price per Units")
    tv2.column("7", width=90)
    tv2.heading("8", text="Temp Store")
    tv2.column("8", width=80)
    tv2.heading("9", text="Temp Ship")
    tv2.column("9", width=80)
    tv2.place(x=10, y=15)
    tv2.bind("<Double-1>", updateShipOut)
    scrollbar = ttk.Scrollbar(tabview.tab("Outgoing"), orient="vertical", command=tv.yview)
    tv2.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(x=930, y=39, height=382)
    display_data2()
outgoingTree()

button5 = ctk.CTkButton(tabview.tab("Stock"), text="Add Product", command=addProduct)
button5.place(x=540, y=450)
button6 = ctk.CTkButton(tabview.tab("Stock"), text="Delete Product", command=deleteProduct)
button6.place(x=270, y=450)

window.mainloop()
c.close()
conn.close()