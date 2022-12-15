from tkinter import *
from tkinter import messagebox, Canvas, PhotoImage, Label
from random import choice, randint, shuffle
import pyperclip


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

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="All fields are required.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Please confirm your details: \nEmail: {email} "
                                       f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            with open("data.txt", "a") as data_file:
                data_file.write(
                    f"Service/Website: {website} | Email: {email} | Password: {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_entry.delete(0, END)


def help():
    messagebox.showinfo(
        title="Help", message="Safe Data is a program that allows you to save your logins locally so you won't have to panic when a major password database gets breached through. \nWe do not store your data anywhere on our database nor do we want to. \nThe code is open-source for everyone on github.com/ziadh/Safe-Data and you can check the code yourself.")


version = "0.10"
window = Tk()
window.configure(bg="light blue")
window.title(f"Safe Data v{version} - Beta Release")
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)
window.wm_iconbitmap('media\logo.ico')

canvas = Canvas(height=150, width=275)
logo_img = PhotoImage(file="media\logo.png")
canvas.create_image(137, 75, image=logo_img, anchor="center")
canvas.grid(row=0, column=1)


website_label = Label(text="Website/Service name:", bg='light blue')
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", bg='light blue')
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", bg='light blue')
password_label.grid(row=3, column=0)

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

generate_password_button = Button(
    text="Randomize Password", command=randomize_password)
generate_password_button.grid(row=3, column=2)
save_button = Button(text="Save", width=36, command=save)
save_button.grid(row=4, column=1, columnspan=2)

privacy_button = Button(text="Is this safe?", width=15, command=help)
privacy_button.grid(row=7, column=2, columnspan=1)
exit_button = Button(text="Exit", width=15, command=exit)
exit_button.grid(row=8, column=2, columnspan=1)
window.mainloop()
