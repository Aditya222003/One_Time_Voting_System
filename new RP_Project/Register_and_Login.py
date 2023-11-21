import tkinter as tk
import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import subprocess
import sqlite3 as sqltor
import matplotlib.pyplot as plt

REGISTER_FILE = 'registered_users.csv'

conn = sqltor.connect('main.db')  # main database
cursor = conn.cursor()  # main cursor
cursor.execute("""CREATE TABLE IF NOT EXISTS poll (name)""")

def create_register_file():
    try:
        with open(REGISTER_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password'])
    except FileExistsError:
        pass
    
def register():
    username = reg_username.get()
    password = reg_password.get()


    # Check if the username is already registered
    with open(REGISTER_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                messagebox.showerror('Error', 'Username already exists.')
                return

    # Register the user
    with open(REGISTER_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

    messagebox.showinfo('Success', 'Registration successful.')
    open_login_page()

login_window = None  # Declare login_window as a global variable

def open_pollings_page():
    global login_window  
    login_window.destroy() 
    subprocess.Popen(['python3', 'Polling.py'])
def login():
    username = login_username.get()
    password = login_password.get()

    # Check if the username and password match
    with open(REGISTER_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username and row[1] == password:
                messagebox.showinfo('Success', 'Login successful.')
                # # Allow the user to proceed with voting
                # polls()
                open_pollings_page()
                return

    messagebox.showerror('Error', 'Invalid username or password.')


def open_login_page():
    global login_username
    global login_password
    global login_window
    root.destroy()

    login_window = tk.Tk()
    login_window.geometry('1000x600')
    login_window.title('Login System')
    login_window.configure(bg="#2874A6")

    # Add background image
    bg_image = Image.open("voating_bckg.jpg")
    bg_image = bg_image.resize((1000, 600), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(login_window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_frame = tk.Frame(login_window, bg="#2874A6")
    login_frame.pack(pady=20)

    tk.Label(login_frame, text='Username:', font=('', 22), bg="#2874A6").grid(row=0, column=0, padx=5, pady=5)
    login_username = tk.Entry(login_frame, font=('', 22))
    login_username.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text='Password:', font=('', 22), bg="#2874A6").grid(row=1, column=0, padx=5, pady=5)
    login_password = tk.Entry(login_frame, show='*', font=('', 22))
    login_password.grid(row=1, column=1, padx=5, pady=5)

    login_button = tk.Button(login_frame, text='Login', command=login, font=('', 22))
    login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    login_window.mainloop()

# open_login_page()
def pollpage():
    def proceed():
        chosen = choose.get()
        print(chosen)
        command = 'UPDATE polling SET votes = votes + 1 WHERE name = ?'
        pd.execute(command, (chosen,))
        pd.commit()
        messagebox.showinfo('Success!', 'You have voted')

    choose = StringVar()
    names = []
    pd = sqltor.connect(plname + '.db')  # poll database
    pcursor = pd.cursor()  # poll cursor
    pcursor.execute('SELECT name FROM polling')
    data = pcursor.fetchall()

    for i in range(len(data)):
        data1 = data[i]
        ndata = data1[0]
        names.append(ndata)

    print(names)
    ppage = Toplevel()
    ppage.geometry('700x700')
    ppage.title('Poll')

    Label(ppage, text='Vote for any one person!').grid(row=1, column=3)
    for i in range(len(names)):
        Radiobutton(ppage, text=names[i], value=names[i], variable=choose).grid(row=2 + i, column=1)
    Button(ppage, text='Vote', command=proceed).grid(row=2 + i + 1, column=2)
 

def polls():
    def proceed():
        global plname
        plname = psel.get()
        if plname == '-select-':
            return messagebox.showerror('Error', 'select poll')
        else:
            mpolls.destroy()
            pollpage()

    cursor.execute('SELECT name FROM poll')
    data = cursor.fetchall()
    pollnames = ['-select-']
    for i in range(len(data)):
        data1 = data[i]
        ndata = data1[0]
        pollnames.append(ndata)

    mpolls = Toplevel()
    mpolls.geometry('400x400')
    mpolls.title('Polls')
    psel = StringVar()
    Label(mpolls, text='My polls', font=('Arial Bold', 20)).grid(row=0, column=2)
    Label(mpolls, text='').grid(row=1)
    Label(mpolls, text='').grid(row=2)
    Label(mpolls, text='Select poll').grid(row=3, column=1)
    poll = ttk.Combobox(mpolls, values=pollnames, textvariable=psel)
    poll.current(0)
    poll.grid(row=3, column=2)
    Button(mpolls, text='Proceed', command=proceed).grid(row=4, column=2)

def create():
    def add():
        cname = ctext.get()
        if not cname:
            messagebox.showerror('Error', 'Enter candidate name')
            return

        cursor.execute('INSERT INTO polling (name, votes) VALUES (?, ?)', (cname, 0))
        cursor.connection.commit()

        ctext.delete(0, END)
        messagebox.showinfo('Success', 'Candidate added successfully.')

    cwin = Toplevel()
    cwin.geometry('400x400')
    cwin.title('Create Poll')
    Label(cwin, text='Create Poll', font=('Arial Bold', 20)).grid(row=0, column=1)
    Label(cwin, text='').grid(row=1)
    Label(cwin, text='').grid(row=2)
    Label(cwin, text='Enter poll name').grid(row=3, column=0)
    pname = Entry(cwin)
    pname.grid(row=3, column=1)
    Button(cwin, text='Create', command=create_poll).grid(row=4, column=1)

    # Declare ctext variable here
    ctext = Entry(cwin)

    def create_poll():
        poll_name = pname.get()
        if not poll_name:
            messagebox.showerror('Error', 'Enter poll name')
            return

        cursor.execute('INSERT INTO poll (name) VALUES (?)', (poll_name,))
        cursor.connection.commit()

        cursor.execute('CREATE TABLE IF NOT EXISTS polling (name, votes)')
        cursor.connection.commit()

        add()
        Label(cwin, text='').grid(row=5)
        Label(cwin, text='').grid(row=6)
        Label(cwin, text='Enter candidate name').grid(row=7, column=0)
        ctext.grid(row=7, column=1)
        Button(cwin, text='Add candidate', command=add).grid(row=8, column=1)

def open_admin_login_page():
    global admin_login_username
    global admin_login_password
    admin_login_window = tk.Tk()
    admin_login_window.geometry('400x200')
    admin_login_window.title('Admin Login')

    admin_login_frame = tk.Frame(admin_login_window)
    admin_login_frame.pack(pady=20)

    tk.Label(admin_login_frame, text='Username:').grid(row=0, column=0, padx=5, pady=5)
    admin_login_username = tk.Entry(admin_login_frame)
    admin_login_username.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(admin_login_frame, text='Password:').grid(row=1, column=0, padx=5, pady=5)
    admin_login_password = tk.Entry(admin_login_frame, show='*')
    admin_login_password.grid(row=1, column=1, padx=5, pady=5)

    admin_login_button = tk.Button(admin_login_frame, text='Login', command=admin_login)
    admin_login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    admin_login_window.mainloop()
def admin_login():
    username = admin_login_username.get()
    password = admin_login_password.get()

    # Check if the username and password match the admin credentials
    if username == 'admin' and password == 'admin123':
        messagebox.showinfo('Success', 'Admin login successful.')
        subprocess.Popen(['python3', 'admin.py'])
        
    else:
        messagebox.showerror('Error', 'Invalid username or password.')

def selpl():
    global selplval
    plt.close()
    plname = selplval.get()
    if plname == '-select-':
        return messagebox.showerror('Error', 'Select a poll')
    else:
        fig = plt.figure(figsize=(8, 4))
        ax = fig.add_axes([0, 0, 1, 1])
        candidates = []
        votes = []
        pcursor = conn.cursor()
        pcursor.execute(f'SELECT name, votes FROM {plname}')
        pdata = pcursor.fetchall()
        for i in range(len(pdata)):
            pdata1 = pdata[i]
            cdata = pdata1[0]
            vdata = pdata1[1]
            candidates.append(cdata)
            votes.append(vdata)

        ax.bar(candidates, votes)
        ax.set_xlabel('Candidates')
        ax.set_ylabel('Votes')
        ax.set_title(f'Poll: {plname} - Results')
        plt.show()

def about():
    messagebox.showinfo('About', 'This is a voting system application.')

def exit_app():
    conn.close()
    exit()

root = tk.Tk()
root.geometry('1000x600')  # Update the form size here
root.title('Voting System')

bg_image = Image.open("main_voating.jpg")
bg_image = bg_image.resize((1000, 600), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

register_frame = tk.Frame(root, bg="#566573")  # Set background color to blue
register_frame.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

tk.Label(register_frame, text='Username:', font=('', 22), bg="#566573").grid(row=0, column=0, padx=5, pady=5)
reg_username = tk.Entry(register_frame, font=('', 22))  # Increase font size to 22
reg_username.grid(row=0, column=1, padx=5, pady=5)

tk.Label(register_frame, text='Password:', font=('', 22), bg="#566573").grid(row=1, column=0, padx=5, pady=5)
reg_password = tk.Entry(register_frame, show='*', font=('', 22))  # Increase font size to 22
reg_password.grid(row=1, column=1, padx=5, pady=5)

register_button = tk.Button(register_frame, text='Register', font=('', 22), command=register)  # Increase font size to 22
register_button.grid(row=2, column=0, padx=5, pady=5)

# Add Login Button
login_button = tk.Button(register_frame, text='Login', font=('', 22), command=open_login_page)  # Increase font size to 22
login_button.grid(row=2, column=1, padx=5, pady=5)

admin_login_button = tk.Button(root, text='Admin Login', font=('', 22), command=open_admin_login_page)  # Increase font size to 22
admin_login_button.grid(row=12, column=2, padx=5, pady=5)

root.mainloop()