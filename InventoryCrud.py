from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox 
import pyodbc


#konek detabes
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
    e_id.configure(state='normal')
    e_id.delete(first = 0, last = 22)
    e_id.configure(state='disabled')

def insert():
    cursor = conn.cursor()
    name = e_name.get().upper()
    desc = e_desc.get().upper()
    size = e_size.get().upper()
    price = e_price.get()
    
    if(name == "" or price == "" or desc == "" or size == ""):
        MessageBox.showinfo("Insert Status", "All fields are required")
    else:
        cursor.execute("insert into dbo.Products (name, details, size, price) values ('"+name+"','"+desc+"','"+size+"','"+price+"')")
        cursor.execute("commit")
        clear()
        show()
        MessageBox.showinfo("Insert Status", "Succesfully Inserted")
        cursor.close()

def delete():
    cursor = conn.cursor()
    id_num = e_id.get()

    if(id_num == ""):
        MessageBox.showinfo("Delete Status", "Select an item to delete")
    else:
        cursor.execute("delete from dbo.Products where id = '"+id_num+"'")
        cursor.execute("commit")
        clear()
        show()
        MessageBox.showinfo("Delete Status", "Sucessfully Deleted")
        cursor.close()

def update(): 
    wat = None
    cursor = conn.cursor()
    name = e_name.get()
    desc = e_desc.get()
    size = e_size.get()
    price = e_price.get()
    id_num = e_id.get()

    try:
        Item = tv.selection()[0]
        wat = True
    except:
        wat = False
    if(wat):
        select_item()
        tv.selection_remove(Item)
    elif(id_num == ""):
        MessageBox.showinfo("Update Status", "Select an item to update")
    else:
        cursor.execute("update dbo.Products SET name = '"+name.upper()+"', details = '"+desc.upper()+"', size = '"+size.upper()+"', price = '"+price+"' WHERE id = '"+id_num+"'")
        cursor.execute("commit")
        clear()
        show()
        MessageBox.showinfo("Update Status", "Sucessfully Updated")
        cursor.close()

def show():
    for row in tv.get_children():
        tv.delete(row)
    cursor = conn.cursor()
    cursor.execute("select * from Products")
    rows = cursor.fetchall()
    for row in rows:
        tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))

def select_item():
    try:
        Item = tv.selection()[0]
        selection = tv.item(Item)
        get = str(selection)
        get = get[get.find('[')+1 : get.find(']')]
        get = get.split(',')
        clear()
        e_id.configure(state='normal')
        e_id.insert(0, get[0])
        e_id.configure(state='disabled')
        e_name.insert(0, get[1].replace("'", "")[1:])
        e_desc.insert(0, get[2].replace("'", "")[1:])
        e_size.insert(0, get[3].replace("'", "")[1:])
        e_price.insert(0, get[4][1:])
    except:
        print("An exception occurred")

#Main Window
crud = Tk()
crud.geometry("800x400")
crud.title("Inventory System")
crud.resizable(0,0)

#Disenyo
s = ttk.Style(crud)
s.theme_use('clam')
s.configure('flat.TButton', borderwidth=0)


#Sulat
idtxt = Label(crud, text = 'ID', font = ("bold", 10))
idtxt.place(x=20, y=30)
name = Label(crud, text = 'Product Name', font = ("bold", 10))
name.place(x=20, y=60)
desc = Label(crud, text = 'Description', font = ("bold", 10))
desc.place(x=20, y=90)
size = Label(crud, text = 'Size', font = ("bold", 10))
size.place(x=20, y=120)
price = Label(crud, text = 'Price', font = ("bold", 10))
price.place(x=20, y=150)

#Sulatan
e_id = Entry(state = 'disabled')
e_id.place(x = 150, y = 30)
e_name = Entry()
e_name.place(x = 150, y = 60)
e_desc = Entry()
e_desc.place(x = 150, y = 90)
e_size = Entry()
e_size.place(x = 150, y = 120)
e_price = Entry()
e_price.place(x = 150, y = 150)

#Pinipindot
insert = Button(crud, text = "insert", font = ("italic", 10), bg = "white", command = insert)
insert.place(x = 150, y = 180, width = 125)
delete = Button(crud, text = "delete", font = ("italic", 10), bg = "white",command = delete)
delete.place(x = 150, y = 240, width = 125)
update = Button(crud, text = "update", font = ("italic", 10), bg = "white", command = update)
update.place(x = 150, y = 210, width = 125)

#Tabla
frm = Frame(crud)
frm.place(x = 300, y = 30)
tv = ttk.Treeview(frm, columns = (1,2,3,4,5), selectmode="extended" ,height = "15", show = "headings")
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
#tv.bind('<ButtonRelease-1>', select_item)

show()
crud.mainloop()