from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox 
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=BENGBENG;'
                      'Database=db_clothing_line;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

def clear():
    e_name.delete(first = 0, last = 22)
    e_desc.delete(first = 0, last = 22)
    e_size.delete(first = 0, last = 22)
    e_price.delete(first = 0, last = 22)

def insert():
    cursor = conn.cursor()

    name = e_name.get()
    desc = e_desc.get()
    size = e_size.get()
    price = e_price.get()
    
    if(name == "" or price == "" or desc == "" or size == ""):
        MessageBox.showinfo("Insert Status", "All fields are required")
    else:
        cursor.execute("insert into dbo.Products (name, details, size, price) values ('"+name+"','"+desc+"','"+size+"','"+price+"')")
        cursor.execute("commit")
        clear()
        MessageBox.showinfo("Insert Status", "Inserted Succesfully")
        cursor.close()

def delete():
    cursor = conn.cursor()

    name = e_name.get()
    if(name == ""):
        MessageBox.showinfo("Delete Status", "Name field is empty")
    else:
        cursor.execute("delete from dbo.Products where name = '"+name+"'")
        cursor.execute("commit")
        clear()
        MessageBox.showinfo("Delete Status", "Sucessfully Deleted")
        cursor.close()

def update():
    cursor = conn.cursor()

    name = e_name.get()
    desc = e_desc.get()
    size = e_size.get()
    price = e_price.get()

    if(name == ""):
        MessageBox.showinfo("Update Status", "Name field is empty")
    else:
        cursor.execute("update dbo.Products SET name = '"+name+"', details = '"+desc+"', size = '"+size+"', price = '"+price+"' WHERE name = '"+name+"'")
        cursor.execute("commit")
        clear()
        MessageBox.showinfo("Update Status", "Sucessfully Deleted")
        cursor.close()

def find():
    cursor = conn.cursor()

    name = e_name.get()
    if(name == ""):
        MessageBox.showinfo("Find Status", "Name field is empty")
    else:
        cursor.execute("select * from dbo.Products where name = '"+name+"' ")
        rows = cursor.fetchall()
        for row in rows:
            e_desc.insert(0, row[2])
            e_size.insert(0, row[3])
            e_price.insert(0, row[4])
    cursor.close()

def show():
    cursor = conn.cursor()
    cursor.execute("select * from Products")
    rows = cursor.fetchall()
    for row in rows:
        tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))



crud = Tk()
crud.geometry("800x500")
crud.title("Inventory System")
crud.resizable(0,0)

#Label
name = Label(crud, text = 'Product Name', font = ("bold", 10))
name.place(x=20, y=30)
desc = Label(crud, text = 'Description', font = ("bold", 10))
desc.place(x=20, y=60)
size = Label(crud, text = 'Size', font = ("bold", 10))
size.place(x=20, y=90)
price = Label(crud, text = 'Price', font = ("bold", 10))
price.place(x=20, y=120)

#idTxt = Label(crud, text = 'ID', font = ("bold", 10))
#idTxt.place(x=305, y=10)
#nameTxt = Label(crud, text = 'NAME', font = ("bold", 10))
#nameTxt.place(x=330, y=10)
#descTxt = Label(crud, text = 'DETAILS', font = ("bold", 10))
#descTxt.place(x=375, y=10)
#sizeTxt = Label(crud, text = 'SIZE', font = ("bold", 10))
#sizeTxt.place(x=435, y=10)
#priceTxt = Label(crud, text = 'PRICE', font = ("bold", 10))
#priceTxt.place(x=470, y=10)

#Textbox
e_name = Entry()
e_name.place(x = 150, y = 30)

e_desc = Entry()
e_desc.place(x = 150, y = 60)

e_size = Entry()
e_size.place(x = 150, y = 90)

e_price = Entry()
e_price.place(x = 150, y = 120)

#Button
insert = Button(crud, text = "insert", font = ("italic", 10), bg = "white", command = insert)
insert.place(x = 20, y = 160)

delete = Button(crud, text = "delete", font = ("italic", 10), bg = "white", command = delete)
delete.place(x = 70, y = 160)

update = Button(crud, text = "update", font = ("italic", 10), bg = "white", command = update)
update.place(x = 130, y = 160)

find = Button(crud, text = "find", font = ("italic", 10), bg = "white", command = find)
find.place(x = 190, y = 160)

frm = Frame(crud)
frm.place(x = 300, y = 30)

tv = ttk.Treeview(frm, columns = (1,2,3,4,5), selectmode="extended" ,height = "5", show = "headings")
tv.pack(expand=YES, fill=BOTH)

tv.heading(1, text = "ID")
tv.column(1 ,minwidth=0,width=30, stretch=NO, anchor = 'center')
tv.heading(2, text = "NAME")
tv.column(2 ,minwidth=0,width=100, stretch=NO, anchor = 'center')
tv.heading(3, text = "DETAILS")
tv.column(3 ,minwidth=0,width=100, stretch=NO, anchor = 'center')
tv.heading(4, text = "SIZE")
tv.column(4 ,minwidth=0,width=50, stretch=NO, anchor = 'center')
tv.heading(5, text = "PRICE")
tv.column(5 ,minwidth=0,width=80, stretch=NO, anchor = 'center')

show()

crud.mainloop()