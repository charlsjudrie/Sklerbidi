from tkinter import *
from tkinter import ttk
from decimal import Decimal
import tkinter.messagebox as MessageBox 
import pyodbc

#konek detabes
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=BENGBENG;'
                      'Database=db_clothing_line;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

def clear():
    global id_num
    e_name.delete(first = 0, last = 22)
    e_desc.delete(first = 0, last = 22)
    e_size.delete(first = 0, last = 22)
    e_price.delete(first = 0, last = 22)
    e_search.delete(0,'end')
    id_num = ""

def insert():
    global id_num
    name = e_name.get().upper()
    desc = e_desc.get().upper()
    size = e_size.get().upper()
    price = e_price.get()

    e_search.delete(0,'end')
    
    if(name == "" or price == "" or desc == "" or size == ""):
        MessageBox.showerror("Insert Status", "All fields are required")
    else:
        cursor = conn.cursor().execute("insert into dbo.Products (name, details, size, price) values ('"+name+"','"+desc+"','"+size+"','"+price+"')")
        cursor.execute("commit")
        show()
        MessageBox.showinfo("Insert Status", "Succesfully Inserted")
        cursor.close()

def delete():
    global id_num

    try: select_item() ; idnum = id_num ;clear()
    except: print("")

    if(idnum == ""):
        MessageBox.showerror("Delete Status", "Select an item to delete")
    else:
        warning = MessageBox.askquestion ('Delete Product','Are you sure?',icon = 'warning')
        if (warning == 'yes'):
            cursor = conn.cursor().execute("delete from dbo.Products where id = '"+idnum+"'")
            cursor.execute("commit")
            show()
            MessageBox.showinfo("Delete Status", "Sucessfully Deleted")
            cursor.close()
 
def update(): 
    global id_num

    name = e_name.get()
    desc = e_desc.get()
    size = e_size.get()
    price = e_price.get()
    
    try: Item = tv.selection()[0]; check = True
    except: check = False

    if(check):
        select_item() ; e_search.delete(0,'end') ;tv.selection_remove(Item)
        insert.configure(state='disabled'); delete.configure(state='disabled')
    elif(id_num == ""):
        MessageBox.showerror("Update Status", "Select an item to update")
    else:
        cursor = conn.cursor().execute("update dbo.Products SET name = '"+name.upper()+"', details = '"+desc.upper()+"', size = '"+size.upper()+"', price = '"+price+"' WHERE id = '"+id_num+"'")
        cursor.execute("commit")
        insert.configure(state='normal') ; delete.configure(state='normal')
        show()
        MessageBox.showinfo("Update Status", "Sucessfully Updated")
        cursor.close()

def show():
    global id_num
    
    for row in tv.get_children():
        tv.delete(row)
    cursor = conn.cursor().execute("select * from Products")
    rows = cursor.fetchall()
    for row in rows:
        tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))
    clear()

def select_item(): 
    global id_num
    try:
        Item = tv.selection()[0]
        selection = tv.item(Item)
        get = str(selection)
        get = get[get.find('[')+1 : get.find(']')]
        get = get.split(',')
        clear()
        id_num = get[0].replace("'", "")
        e_name.insert(0, get[1].replace("'", "")[1:])
        e_desc.insert(0, get[2].replace("'", "")[1:])
        e_size.insert(0, get[3].replace("'", "")[1:])
        e_price.insert(0, get[4][1:])
    except:
        print("")

def search_bar(sb):
    for row in tv.get_children():
        tv.delete(row)
        
    if(len(e_search.get()) == 0):
        cursor = conn.cursor().execute("select * from Products")
        rows = cursor.fetchall()
        for row in rows:
            tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))
        print("nah")
    else:
        cursor = conn.cursor().execute("select * from Products where '"+e_search.get()+"' like concat('%',name,'%')")
        rows = cursor.fetchall()
        for row in rows:
            tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))
        cursor.close()

crud = Tk()
crud.geometry("800x400")
crud.title("CRUD")
crud.resizable(0,0)

sb = StringVar()
sb.trace("w", lambda name, index, mode, sb=sb: search_bar(sb))

name = Label(crud, text = 'Product Name', font = ("bold", 10))
name.place(x=20, y=30)
desc = Label(crud, text = 'Description', font = ("bold", 10))
desc.place(x=20, y=60)
size = Label(crud, text = 'Size', font = ("bold", 10))
size.place(x=20, y=90)
price = Label(crud, text = 'Price', font = ("bold", 10))
price.place(x=20, y=120)
search = Label(crud, text = 'Search', font = ("bold", 10))
search.place(x=560, y=5)

e_name = Entry()
e_name.place(x = 150, y = 30)
e_desc = Entry()
e_desc.place(x = 150, y = 60)
e_size = Entry()
e_size.place(x = 150, y = 90)
e_price = Entry()
e_price.place(x = 150, y = 120)
e_search = Entry(textvariable=sb)
e_search.place(x = 609, y = 5)

insert = Button(crud, text = "Insert", font = ("italic", 10), bg = "white", command = insert)
insert.place(x = 150, y = 180, width = 125)
delete = Button(crud, text = "Delete", font = ("italic", 10), bg = "white",command = delete)
delete.place(x = 150, y = 240, width = 125)
update = Button(crud, text = "Update", font = ("italic", 10), bg = "white", command = update)
update.place(x = 150, y = 210, width = 125)

frm = Frame(crud)
frm.place(x = 300, y = 30)
tv = ttk.Treeview(frm, columns = (1,2,3,4,5), selectmode="extended" ,height = "15", show = "headings")
tv.pack(expand=YES, fill=BOTH)
tv.heading(1, text = "ID")
tv.column(1 ,minwidth=0,width=30, stretch=NO, anchor = 'center')
tv.heading(2, text = "NAME")
tv.column(2 ,minwidth=0,width=120, stretch=NO, anchor = 'center')
tv.heading(3, text = "DETAILS")
tv.column(3 ,minwidth=0,width=150, stretch=NO, anchor = 'center')
tv.heading(4, text = "SIZE")
tv.column(4 ,minwidth=0,width=50, stretch=NO, anchor = 'center')
tv.heading(5, text = "PRICE")
tv.column(5 ,minwidth=0,width=80, stretch=NO, anchor = 'center')

show()
clear()
crud.mainloop()