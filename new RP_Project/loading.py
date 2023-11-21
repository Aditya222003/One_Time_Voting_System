import tkinter as tk
from tkinter import ttk
import time
import subprocess
from PIL import ImageTk, Image

def simulate_loading():
    progress["maximum"] = 100

    for i in range(101):
        progress["value"] = i
        root.update_idletasks()
        time.sleep(0.05)

def close_loading():
    root.after(2000, open_second_page)

def open_second_page():
    subprocess.run(["python3", "Register_and_Login.py"])


root = tk.Tk()
root.title("Loading Page")
root.geometry("1000x500")

# Load and set the background image
background_image = Image.open("loading.png")
background_image = background_image.resize((1000, 500), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=1000, height=500)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

label = tk.Label(root, text="PERSONALISED VOTING SYSTEM", bg="purple",fg="white" ,font=("Times New Roman", 18, "bold"))
label.place(relx=0.9, rely=0.1, anchor="se")
# Create and place the label on the background

label = tk.Label(root, text="Loading...", font=("Times New Roman", 16, "bold"),fg="white",bg="#FA06BA")
# label.configure(bg="" ,highlightthickness=0)
label.place(relx=0.2, rely=0.4, anchor="se")

label = tk.Label( root , text= " Project by : Aditya Raul & Rutuja Ingale",bg="#32174D",fg="white",font=("Times New Roman",16,"bold"))
label.place(relx=0.200, rely= 0.99, anchor="s")
# Create and place the progress bar
progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=200)
progress.place(relx=0.2, rely=0.45, anchor="n")

# Simulate loading for 5 seconds
root.after(5000, close_loading)
root.after(10, simulate_loading)
#root.after( 6000, page_destroy)

root.mainloop()
