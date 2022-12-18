import tkinter.filedialog
import json
import colorsys
from tkinter import *
from tkinter import messagebox, Canvas, PhotoImage, Label
from random import choice, randint, shuffle
import pyperclip
import tkinter as tk
import time
from tkinter import ttk
import json
import requests
import webbrowser
version = "1.0"

file_path = None


def download_update(event):
    link = "https://github.com/ziadh/Safe-Data/archive/refs/tags/"+newest_version+".zip"
    webbrowser.open(link)


class splash():
    version = "1.0"
    ss = Tk()
    ss.overrideredirect(True)
    ss.configure(bg="#453C67")
    screen_width = ss.winfo_screenwidth()
    screen_height = ss.winfo_screenheight()
    x_coord = int((screen_width / 2) - (500 / 2))
    y_coord = int((screen_height / 2) - (300 / 2))
    ss.geometry(f"500x275+{x_coord}+{y_coord}")

    with open('settings.json', 'r') as f:
        settings = json.load(f)

    if settings['theme'] == 'light':
        label = tk.Label(ss, text="0%", bg="light blue")
        image = PhotoImage(file='media/splash-light.png')
    elif settings['theme'] == 'dark':
        label = tk.Label(ss, text="0%", bg="#2A3990")
        image = PhotoImage(file='media/splash-dark.png')

    label.pack()
    image_label = Label(ss, image=image)
    image_label.pack()
    progress = ttk.Progressbar(ss, orient=tk.HORIZONTAL, length=300)
    progress.pack()
    progress['value'] = 0
    interval = 0.01
    for i in range(100):
        progress['value'] = i
        label['text'] = f"{i}%"
        ss.update_idletasks()
        time.sleep(interval)
    ss.destroy()


def toggle_password_visibility():
    global is_password_visible
    is_password_visible = not is_password_visible
    password_entry.config(show=("" if is_password_visible else "*"))


def randomize_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password_entry.delete(0, END)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    password_saved.grid(row=6, column=1)


def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="All fields are required.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Please confirm your details: \n \nWebsite/Service: {website} \nEmail: {email} "
                                       f"\nPassword: {password} \n \nConfirm saving credentials?")
        if is_ok:
            with open(file_path or "data.txt", "a") as data_file:
                data_file.write(
                    f"Service/Website: {website} | Email: {email} | Password: {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_entry.delete(0, END)
                password_saved.destroy()


def change_dir():
    global file_path
    # Display a file save dialog to choose the directory
    file_path = tkinter.filedialog.asksaveasfilename(initialfile="data.txt")


def safety():
    messagebox.showinfo(
        title="Safety", message="Safe Data is a program that allows you to save your logins locally so you won't have to panic when a major password database gets breached through. \nWe do not store your data anywhere on our database nor do we want to. \nThe code is open-source for everyone on github.com/ziadh/Safe-Data and you can check the code yourself.")


def toggle_theme():
    default_settings = {
        'theme': 'dark'
    }

    try:
        with open('settings.json', 'r') as f:
            try:
                settings = json.load(f)
            except json.decoder.JSONDecodeError:
                settings = default_settings
    except FileNotFoundError:
        with open('settings.json', 'w') as f:
            json.dump(default_settings, f)
        settings = default_settings

    if 'theme' not in settings:
        settings['theme'] = default_settings['theme']
    if window.cget("bg") != "light blue":
        logo_img.config(file="media\wide-light.png")
        window.wm_iconbitmap('media\logo-light.ico')
        window.config(bg="light blue")
        canvas.config(bg="light blue")
        website_label.config(bg="light blue", fg="black")
        email_label.config(bg="light blue", fg="black")
        password_label.config(bg="light blue", fg="black")
        save_button.config(bg="#AED6F1", fg="black")
        privacy_button.config(bg="#AED6F1", fg="black")
        exit_button.config(bg="#AED6F1", fg="black")
        generate_password_button.config(bg="#AED6F1", fg="black")
        toggle_button.config(bg="#AED6F1", fg="black")
        show_button.config(bg="#AED6F1", fg="black")
        toggle_button.config(text='\u263E')
        version_message.config(bg="light blue", fg="black")
        change_dir_button.config(bg="#AED6F1", fg="black")
        settings['theme'] = 'light'
    else:
        window.config(bg="#2A3990")
        canvas.config(bg="#2A3990")
        logo_img.config(file="media\wide.png")
        window.wm_iconbitmap('media\logo-dark.ico')
        website_label.config(bg="#2A3990", fg="white")
        email_label.config(bg="#2A3990", fg="white")
        password_label.config(bg="#2A3990", fg="white")
        save_button.config(bg="#251749", fg="white")
        privacy_button.config(bg="#251749", fg="white")
        exit_button.config(bg="#251749", fg="white")
        generate_password_button.config(bg="#251749", fg="white")
        toggle_button.config(bg="#251749", fg="white")
        show_button.config(bg="#251749", fg="white")
        toggle_button.config(text='\u2600')
        version_message.config(bg="#2A3990", fg="light green")
        change_dir_button.config(bg="#251749", fg="white")
        settings['theme'] = 'dark'

    with open('settings.json', 'w') as f:
        json.dump(settings, f)


def on_exit():
    result = messagebox.askquestion(
        "Confirm", "Are you sure you want to exit?")
    if result == 'yes':
        window.destroy()


window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coord = int((screen_width / 2) - (500 / 2))
y_coord = int((screen_height / 2) - (300 / 2))

window.geometry(f"700x450+{x_coord}+{y_coord}")

with open('settings.json', 'r') as f:
    settings = json.load(f)

version_message = Label(
    text="", fg="blue", cursor="hand2", bg="#2A3990")
version_message.bind("<Button-1>", download_update)
version_message.grid(row=8, column=0, sticky="w")

r = requests.get("https://api.github.com/repos/ziadh/Safe-Data/releases")
json_data = r.json()
newest_version = json_data[0]["tag_name"]
if float(newest_version) > float(version):
    version_message.config(fg="light green")
    version_message.config(text="New version available!\nClick me to update!")


window.config(bg="#2A3990")
window.title(f"Safe Data v{version}")
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)
window.wm_iconbitmap('media\logo-dark.ico')

canvas = Canvas(height=150, width=275)
logo_img = PhotoImage(file="media\wide.png")
canvas.create_image(137, 75, image=logo_img, anchor="center")
canvas.grid(row=0, column=1, columnspan=2)

website_label = Label(text="Website/Service name", bg="#2A3990", fg="white")
website_label.grid(row=1, column=0)
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_label = Label(text="Email/Username", bg="#2A3990", fg="white")
email_label.grid(row=2, column=0)
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "")

is_password_visible = False
password_label = Label(text="Password", bg="#2A3990", fg="white")
password_label.grid(row=3, column=0)
password_entry = Entry(show="*", width=21)
password_entry.grid(row=3, column=1, sticky='e')
show_button = tk.Button(window, text="\U0001F441",
                        command=toggle_password_visibility, bg="#251749", fg="white")
show_button.grid(row=3, column=2, sticky='w')

generate_password_button = Button(
    text="Randomize Password", command=randomize_password, bg="#251749", fg="white")
generate_password_button.grid(row=3, column=3)

save_button = Button(text="Save", width=36, command=save,
                     bg="#251749", fg="white")
save_button.grid(row=4, column=1, columnspan=2)

privacy_button = Button(text="Is this safe?", width=15,
                        command=safety, bg="#251749", fg="white")
privacy_button.grid(row=5, column=1, padx=50)

exit_button = Button(text="Exit", width=15,
                     command=on_exit, bg="#251749", fg="white")
exit_button.grid(row=7, column=2, padx=15)
change_dir_button = Button(
    text="Change Directory", width=15, command=change_dir, bg="#251749", fg="white")
change_dir_button.grid(row=5, column=2, padx=15)
password_saved = Label(
    text="Randomized password added\nto clipboard.", bg="light green", fg="blue")
toggle_button = Button(text="\u2600", width=15,
                       command=toggle_theme, bg="#251749", fg="white")
toggle_button.grid(row=7, column=1)
if settings['theme'] == 'light':
    logo_img.config(file="media\wide-light.png")
    window.wm_iconbitmap('media\logo-light.ico')
    window.config(bg="light blue")
    canvas.config(bg="light blue")
    website_label.config(bg="light blue", fg="black")
    email_label.config(bg="light blue", fg="black")
    password_label.config(bg="light blue", fg="black")
    save_button.config(bg="#AED6F1", fg="black")
    privacy_button.config(bg="#AED6F1", fg="black")
    exit_button.config(bg="#AED6F1", fg="black")
    generate_password_button.config(bg="#AED6F1", fg="black")
    toggle_button.config(bg="#AED6F1", fg="black")
    show_button.config(bg="#AED6F1", fg="black")
    toggle_button.config(text='\u263E')
    version_message.config(bg="light blue", fg="black")
    change_dir_button.config(bg="#AED6F1", fg="black")

else:
    window.config(bg="#2A3990")
    canvas.config(bg="#2A3990")
    logo_img.config(file="media\wide.png")
    window.wm_iconbitmap('media\logo-dark.ico')
    website_label.config(bg="#2A3990", fg="white")
    email_label.config(bg="#2A3990", fg="white")
    password_label.config(bg="#2A3990", fg="white")
    save_button.config(bg="#251749", fg="white")
    privacy_button.config(bg="#251749", fg="white")
    exit_button.config(bg="#251749", fg="white")
    generate_password_button.config(bg="#251749", fg="white")
    toggle_button.config(bg="#251749", fg="white")
    show_button.config(bg="#251749", fg="white")
    toggle_button.config(text='\u2600')
    version_message.config(bg="#2A3990", fg="light green")
    change_dir_button.config(bg="#251749", fg="white")
window.mainloop()
