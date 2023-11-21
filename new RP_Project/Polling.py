import tkinter as tk
import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
from PIL import ImageTk, Image
# import PIL.Image
import sqlite3 as sqltor
import matplotlib.pyplot as plt

REGISTER_FILE = 'registered_users.csv'
conn=sqltor.connect('main.db') #main database
cursor=conn.cursor() #main cursor
cursor.execute("""CREATE TABLE IF NOT EXISTS poll (name)""")

def create_register_file():
    with open(REGISTER_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Password'])

def pollpage(): #page for polling

     def proceed():
        chose=choose.get()
        print(chose)
        command='update polling set votes=votes+1 where name=?'
        pd.execute(command,(chose,))
        pd.commit()
        messagebox.showinfo('Success!','You have voted')
        
     choose=StringVar()
     names=[]
     pd=sqltor.connect(plname+'.db') #poll database
     pcursor=pd.cursor() #poll cursor
     pcursor.execute('select name from polling')
     data=pcursor.fetchall()
     
     for i in range(len(data)):
         data1=data[i]
         ndata=data1[0]
         names.append(ndata)
         
     print(names)
     ppage=Toplevel()
     ppage.geometry('700x700')
     ppage.title('Poll')


     Label(ppage,text='Vote for any one person!').grid(row=1,column=3)
     for i in range(len(names)):
         Radiobutton(ppage,text=names[i],value=names[i],variable=choose).grid(row=2+i,column=1)
     Button(ppage,text='Vote',command=proceed).grid(row=2+i+1,column=2)


def polls(): #mypolls
    def proceed():
        global plname
        plname=psel.get()
        if plname=='-select-':
            return messagebox.showerror('Error','select poll')
        else:
            mpolls.destroy()
            pollpage()
    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-select-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    psel=StringVar()
    mpolls=Toplevel()
    mpolls.geometry('270x200')
    mpolls.title('Voting Program')
    Label(mpolls,text='Select Poll',font='Helvetica 16 bold').grid(row=1,column=3)
    select=ttk.Combobox(mpolls,values=pollnames,state='readonly',textvariable=psel)
    select.grid(row=2,column=3)
    select.current(0)
    Button(mpolls,text='Proceed',command=proceed).grid(row=2,column=4)



def create():
    def proceed():
        global pcursor
        pname=name.get() #pollname
        can=cname.get()   #candidatename
        if pname=='':
            return messagebox.showerror('Error','Enter poll name',relx=5.5, rely=5.5, anchor="se")
        elif can=='':
            return messagebox.showerror('Error','Enter candidates',relx=5.5, rely=5.5, anchor="se")
        else:
            candidates=can.split(',') #candidate list
            command='insert into poll (name) values (?);'
            cursor.execute(command,(pname,))
            conn.commit()
            pd=sqltor.connect(pname+'.db') #poll database
            pcursor=pd.cursor() #poll cursor
            pcursor.execute("""CREATE TABLE IF NOT EXISTS polling
                 (name TEXT,votes INTEGER)""")
            for i in range(len(candidates)):
                command='insert into polling (name,votes) values (?, ?)'
                data=(candidates[i],0)
                pcursor.execute(command,data)
                pd.commit()
            pd.close()
            messagebox.showinfo('Success!','Poll Created')
            cr.destroy()

    name=StringVar()
    cname=StringVar()
    cr=Toplevel()
    cr.geometry('1000x600')
    cr.title('Create a new poll')

    background_image = Image.open("MyPollbck.jpg")
    background_image = background_image.resize((1000, 600), Image.ANTIALIAS)
    background_photo = ImageTk.PhotoImage(background_image)
    
    canvas = tk.Canvas(home, width=1000, height=600)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

    label1 = tk.Label(cr, text="Enter Details", font=("Times New Roman", 14, "bold"))
    label1.place(relx=0.5, rely=0.1, anchor="se")

    label1 = tk.Label(cr, text="Enter Poll Name :", font=("Times New Roman", 12, "bold"))
    label1.place(relx=0.2, rely=0.2, anchor="se")
    
    entry = tk.Entry(cr, width=30,textvariable=name , font=("Times New Roman", 12, "bold"))
    entry.place(relx=0.5, rely=0.2, anchor="se")

    label1 = tk.Label(cr, text="eg : captains elections :", font=("Times New Roman", 12, "bold"))
    label1.place(relx=0.7, rely=0.2, anchor="se")
    
    label1 = tk.Label(cr, text="Enter Candidates :", font=("Times New Roman", 12, "bold"))
    label1.place(relx=0.21, rely=0.3, anchor="se")

    entry = tk.Entry(cr, width=30,textvariable=cname , font=("Times New Roman", 12, "bold"))
    entry.place(relx=0.5, rely=0.3, anchor="se")

    label1 = tk.Label(cr, text="NOTE : Note: Enter the candidate names one by one by putting commas", font=("Times New Roman", 12, "bold"))
    label1.place(relx=1.0, rely=0.3, anchor="se")

    button1 = tk.Button(cr, text="Create New Poll",bg="gray", font=("Times New Roman", 18), relief="flat",command=proceed)
    button1.place(relx=0.5, rely=0.4, anchor="se")
    button1.bind("<Enter>", on_enter)
    button1.bind("<Leave>", on_leave)

def selpl(): #pollresults
    def results():
        sel=sele.get()  #selected option
        if sel=='-select-':
            return messagebox.showerror('Error','Select Poll')
        else:
            pl.destroy()
            def project():
                names=[]
                votes=[]
                for i in range(len(r)):
                    data=r[i]
                    names.append(data[0])
                    votes.append(data[1])
                    plt.title('Poll Result')
                plt.pie(votes,labels=names,autopct='%1.1f%%',shadow=True,startangle=140)
                plt.axis('equal')
                plt.show()

            res=Toplevel() #result-page
            res.geometry('300x300')
            res.title('Results!')
            Label(res,text='Here is the Result!',font='Helvetica 12 bold').grid(row=1,column=2)
            con=sqltor.connect(sel+'.db')
            pcursor=con.cursor()
            pcursor.execute('select * from polling')
            r=pcursor.fetchall() #data-raw
            for i in range(len(r)):
                data=r[i]
                Label(res,text=data[0]+': '+str(data[1])+' votes').grid(row=2+i,column=1)
            Button(res,text='Project Results',command=project).grid(row=2+i+1,column=2)


    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-select-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    sele=StringVar()
    pl=Toplevel()
    pl.geometry('300x200')
    pl.title('Voting System')
    Label(pl,text='Select Poll',font='Helvetica 12 bold').grid(row=1,column=1)
    sel=ttk.Combobox(pl,values=pollnames,state='readonly',textvariable=sele)
    sel.grid(row=2,column=1)
    sel.current(0)
    Button(pl,text='Get Results',command=results).grid(row=2,column=2)
    
def about():
    messagebox.showinfo('About','Developed by Aditya and Rutuja')
def exit_program():
    answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if answer:
        home.destroy()

home=tk.Tk()
home.geometry('700x500')
home.title('Voting Program')

background_image = Image.open("voating.jpg")
background_image = background_image.resize((700, 500), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(home, width=700, height=500)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

label = tk.Label(home, text="Voating Program", font=("Times New Roman", 18, "bold"),bg="white")
label.place(relx=0.5, rely=0.1, anchor="se")


def on_enter(event):
    event.widget.config(bg="gray")

def on_leave(event):
    event.widget.config(bg="gray")

button2 = tk.Button(home, text="Caste Vote", font=("Times New Roman", 18), relief="flat",command=polls)
button3 = tk.Button(home, text="Exit", font=("Times New Roman", 18), relief="flat",command=exit_program)

button2.bind("<Enter>", on_enter)
button2.bind("<Leave>", on_leave)

button3.bind("<Enter>", on_enter)
button3.bind("<Leave>", on_leave)

button2.place(relx=0.27, rely=0.50, anchor="se")
button3.place(relx=0.20, rely=0.70, anchor="se")

label = tk.Label( home , text= " project by : Aditya Raul & Rutuja Ingale",font=("Times New Roman",12,"bold"),fg="white",bg="#00008B")
label.place(relx=0.2, rely= 0.99, anchor="s")

home.mainloop()
