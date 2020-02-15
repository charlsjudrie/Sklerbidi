from tkinter import *
from tkinter import ttk
from decimal import Decimal
import tkinter.messagebox as MessageBox 
import pyodbc

#konek detabes
conn = pyodbc.connect('Driver={SQL Server}; Server=BENGBENG; Database=db_clothing_line; Trusted_Connection=yes;')
cursor = conn.cursor()

#functions
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
    
    try:
        name = e_name.get().upper()
        desc = e_desc.get().upper()
        size = e_size.get().upper()
        price = float(e_price.get())
        
        if(name == "" or price == "" or desc == "" or size == ""): 
            MessageBox.showerror("Insert Status", "All fields are required")
        else:
            cursor = conn.cursor().execute("insert into dbo.Products (name, description, size, price) values ('"+name+"','"+desc+"','"+size+"','"+price+"')")
            cursor.execute("commit")
            show() ; clear() ; cursor.close() ; e_name.focus()
            MessageBox.showinfo("Insert Status", "Succesfully Inserted")
    except ValueError: MessageBox.showerror("Error", "Price only accept numbers") ; e_price.delete(first = 0, last = 22)
    except: MessageBox.showerror("Error", "Invalid input")


def delete():
    global id_num

    try: select_item() ; idnum = id_num ; clear()
    except: print("")

    if(idnum == ""): 
        MessageBox.showerror("Delete Status", "Select an item to delete")
    else: 
        warning = MessageBox.askquestion ('Delete Product','Are you sure?',icon = 'warning')
        if (warning == 'yes'):
            cursor = conn.cursor().execute("delete from dbo.Products where id = '"+idnum+"'")
            cursor.execute("commit")
            show() ; cursor.close()

def update(): 
    global id_num
    
    name = e_name.get().upper()
    desc = e_desc.get().upper()
    size = e_size.get().upper()
    price = e_price.get()
    
    try: Item = tv.selection()[0]; check = True
    except: check = False

    if(check):
        select_item() ; e_search.delete(0,'end') ;tv.selection_remove(Item)
        insert.configure(state='disabled'); delete.configure(state='disabled')
    elif(id_num == ""): 
        MessageBox.showerror("Update Status", "Select an item to update")
    else:
        try:
            priceCheck = float(price)
            cursor = conn.cursor().execute("update dbo.Products SET name = '"+name+"', description = '"+desc+"', size = '"+size+"', price = '"+price+"' WHERE id = '"+id_num+"'")
            cursor.execute("commit")
            insert.configure(state='normal') ; delete.configure(state='normal')
            show() ; clear() ; cursor.close()
            MessageBox.showinfo("Update Status", "Sucessfully Updated")
        except ValueError: MessageBox.showerror("Error", "Price only accept numbers") ; e_price.delete(first = 0, last = 22)
        except: MessageBox.showerror("Error", "Invalid input")

def show():
    global id_num
    
    for row in tv.get_children(): tv.delete(row)
    cursor = conn.cursor().execute("select * from Products")
    rows = cursor.fetchall()
    for row in rows: tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))

def select_item(): 
    global id_num

    try:
        Item = tv.selection()[0]
        selection = tv.item(Item)
        get = str(selection)
        get = get[get.find('[')+1 : get.find(']')]
        get = get.split(',') ; clear()
        id_num = get[0].replace("'", "")
        e_name.insert(0, get[1].replace("'", "")[1:])
        e_desc.insert(0, get[2].replace("'", "")[1:])
        e_size.insert(0, get[3].replace("'", "")[1:])
        e_price.insert(0, get[4].replace("'", "")[1:])
    except:
        print("Error")

def search_bar(sb):

    for row in tv.get_children(): tv.delete(row)
        
    if(len(e_search.get()) == 0):
        cursor = conn.cursor().execute("select * from Products")
        rows = cursor.fetchall()
        for row in rows: tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))
    else:
        cursor = conn.cursor().execute("select * from Products where '"+e_search.get()+"' like concat(name,'%','%')")
        rows = cursor.fetchall()
        for row in rows: tv.insert('', 'end', text=row[0], values=(row[0],row[1], row[2], row[3], row[4]))
        cursor.close()

#MainWindows
crud = Tk() ; crud.title("Inventory") ; crud.resizable(False, False) 
window_width = 800 ; window_height = 430
screen_width = crud.winfo_screenwidth() ; screen_height = crud.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2)) ; y_cordinate = int((screen_height/2) - (window_height/2))
crud.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
crud["bg"] = "#212121"

#Mga Sulat
name = Label(crud, text = 'PRODUCT NAME', font = ("Century Gothic", 11), bg = "#212121", fg = "#bdc3c7")
name.place(x=20, y=46)
desc = Label(crud, text = 'DESCRIPTION', font = ("Century Gothic", 11), bg = "#212121", fg = "#bdc3c7")
desc.place(x=20, y=76)
size = Label(crud, text = 'SIZE', font = ("Century Gothic", 11), bg = "#212121", fg = "#bdc3c7")
size.place(x=20, y=106)
price = Label(crud, text = 'PRICE', font = ("Century Gothic", 11), bg = "#212121", fg = "#bdc3c7")
price.place(x=20, y=136)
search = Label(crud, text = 'SEARCH', font = ("Century Gothic", 11), bg = "#212121", fg = "#bdc3c7")
search.place(x=540, y=15)

#Mga Sulatan
e_name = Entry(bg = "#BDBDBD", fg = "#212121", font = ("Bahnschrift", 10))
e_name.place(x = 150, y = 49)
e_desc = Entry(bg = "#BDBDBD", fg = "#212121", font = ("Bahnschrift", 10))
e_desc.place(x = 150, y = 79)
e_size = Entry(bg = "#BDBDBD", fg = "#212121", font = ("Bahnschrift", 10))
e_size.place(x = 150, y = 109)
e_price = Entry(bg = "#BDBDBD", fg = "#212121", font = ("Bahnschrift", 10))
e_price.place(x = 150, y = 139)
sb = StringVar()
sb.trace("w", lambda name, index, mode, sb=sb: search_bar(sb))
e_search = Entry(textvariable=sb)
e_search.place(x = 609, y = 18)

#Mga Pindutan
insert = Button(crud, text = "INSERT", font = ("Bahnschrift SemiBold", 11), bg = "#27ae60", fg = "#bdc3c7", command = insert, height = "2")
insert.place(x = 150, y = 169, width = 145, height= 40)
update = Button(crud, text = "UPDATE", font = ("Bahnschrift SemiBold", 11), bg = "#2980b9", fg = "#bdc3c7", command = update, height = "2")
update.place(x = 150, y = 214, width = 145, height= 40)
delete = Button(crud, text = "DELETE", font = ("Bahnschrift SemiBold", 11), bg = "#c0392b", fg = "#bdc3c7",command = delete, height = "2")
delete.place(x = 150, y = 259, width = 145, height= 40)

#Tabla
frm = Frame(crud)
frm.place(x = 300, y = 49, )
tv = ttk.Treeview(frm, columns = (1,2,3,4,5), selectmode="extended" ,height = "15", show = "headings")
tv.pack(expand=YES, fill=BOTH)
tv.heading(1, text = "ID")
tv.column(1 ,minwidth=0,width=30, stretch=NO, anchor = 'center')
tv.heading(2, text = "NAME")
tv.column(2 ,minwidth=0,width=120, stretch=NO, anchor = 'center')
tv.heading(3, text = "DESCRIPTION")
tv.column(3 ,minwidth=0,width=150, stretch=NO, anchor = 'center')
tv.heading(4, text = "SIZE")
tv.column(4 ,minwidth=0,width=50, stretch=NO, anchor = 'center')
tv.heading(5, text = "PRICE")
tv.column(5 ,minwidth=0,width=80, stretch=NO, anchor = 'center')

show()
clear()
crud.mainloop()
