import tkinter.filedialog
from tkinter import *
from tkinter import messagebox, Canvas, PhotoImage, Label
import tkinter as tk
from tkinter import ttk

import json
from random import choice, randint, shuffle
import pyperclip
import time
import json
import requests
import webbrowser
import datetime
import os
import sys

file_path = None
language = None

log_folder = "errors_logged"
log_prefix = "errors_log_from_.txt"

if not os.path.exists(log_folder):
    os.makedirs(log_folder)
current_time = time.strftime("%m%d%Y-%H-%M-%S")
log_file = log_prefix + current_time + ".txt"
log_path = os.path.join(log_folder, log_file)
sys.stderr = open(log_path, "a")

with open('src/settings.json', 'r') as f:
    settings = json.load(f)
version = settings['version']
language = settings['language']


with open('src/languages.json', 'r', encoding='utf8') as f:
    language_data = json.load(f)
for lang in language_data['languages']:
    if lang['language'] == language:
        chosen_lang = lang
        break
with open('src/settings.json', 'w') as f:
    json.dump(settings, f)


def version_checker():
    r = requests.get("https://api.github.com/repos/ziadh/Safe-Data/releases")
    json_data = r.json()
    newest_version = json_data[0]["tag_name"]
    if float(newest_version) > float(version):
        version_message.config(fg="light green",
                               text=chosen_lang["version_needs_update"].format(newest_version))
        whats_new_label.config(fg="light green",
                               text=chosen_lang["view_patch_notes"])
    else:
        version_message.config(
            text=chosen_lang["latest_version_message"].format(version), cursor="")
        whats_new_label.config(fg="light green",
                               text=chosen_lang["view_patch_notes"])
        version_message.unbind("<Button-1>")


def download_update(event):
    r = requests.get("https://api.github.com/repos/ziadh/Safe-Data/releases")
    json_data = r.json()
    newest_version = json_data[0]["tag_name"]
    link = "https://github.com/ziadh/Safe-Data/archive/refs/tags/"+newest_version+".zip"
    webbrowser.open(link)


def open_patch_notes(event, language, chosen_lang):

    with open('src/languages.json', 'r', encoding='utf8') as f:
        language_data = json.load(f)

    for lang in language_data['languages']:
        if lang['language'] == language:
            chosen_lang = lang
            break

    r = requests.get("https://api.github.com/repos/ziadh/Safe-Data/releases")
    json_data = r.json()
    newest_version = json_data[0]["tag_name"]
    link = f"https://github.com/ziadh/Safe-Data/releases/tag/{newest_version}"

    if language != "EN":

        translated_link = chosen_lang['release_link'].format(
            newest_version=newest_version)
        link = translated_link

    webbrowser.open(link)


class splash():
    ss = Tk()
    ss.overrideredirect(True)
    ss.configure(bg="#453C67")
    screen_width = ss.winfo_screenwidth()
    screen_height = ss.winfo_screenheight()
    x_coord = int((screen_width / 2) - (500 / 2))
    y_coord = int((screen_height / 2) - (300 / 2))
    ss.geometry(f"500x250+{x_coord}+{y_coord}")

    with open('src/settings.json', 'r') as f:
        settings = json.load(f)

    if settings['theme'] == 'light':
        label = tk.Label(ss, text="", bg="light blue")
        image = PhotoImage(file='assets/logos/splash-light.png')
    elif settings['theme'] == 'dark':
        label = tk.Label(ss, text="", bg="#2A3990")
        image = PhotoImage(file='assets/logos/splash-dark.png')
    label.place(x=-10, y=-10)
    image_label = Label(ss, image=image)
    image_label.place(x=0, y=0)
    progress = ttk.Progressbar(ss, orient=tk.HORIZONTAL, length=300)
    progress.configure(style='orange.Horizontal.TProgressbar')
    progress.place(x=100, y=200)
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
    if settings['theme'] == 'light':
        pass_check_label.config(text="", bg="light blue", fg="light blue")
    if settings['theme'] == 'dark':
        pass_check_label.config(text="", bg="#2A3990", fg="#2A3990")
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
    password_saved.config(text=chosen_lang["password_saved_label"])
    password_saved.place(x=40, y=120)


def check_pass():
    password = password_entry.get().lower()
    username = email_entry.get()
    weak_pass = ["pass", "password", "123456",
                 "123", "000", "qwerty", "1111", "2222", "qwerty123", "abc123", "password123"]
    weak_pass.append(username)
    safe = True
    for word in weak_pass:
        if word in password:
            safe = False
            break
    if safe:
        pass_check_label.config(
            text=chosen_lang["check_pass_good"], bg="light green", fg="blue")
    else:
        pass_check_label.config(
            text=chosen_lang["check_pass_bad"], bg="red", fg="white")
    if password == "":
        pass_check_label.config(
            text=chosen_lang["check_pass_missing"], bg="yellow", fg="blue")
    if len(password) < 7 and len(password) > 0:
        pass_check_label.config(
            text=chosen_lang["check_pass_short"], bg="yellow", fg="blue")


def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message=chosen_lang["all_fields_error"])
    else:
        if file_path == None:
            is_ok = messagebox.askokcancel(
                title=chosen_lang["save_data_title"],
                message=chosen_lang["save_data_message"].format(website=website, email=email, password=password))

            if is_ok:
                now = datetime.datetime.now()
                date_string = now.strftime("%m/%d/%Y")

                with open(file_path or "data.txt", "a") as data_file:
                    data_file.write(chosen_lang[f"saved_data_txt"].format(
                        website=website, email=email, password=password, date_string=date_string))
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
                    email_entry.delete(0, END)
                    password_saved.destroy()
        else:
            is_ok = messagebox.askokcancel(
                title=chosen_lang["save_data_title"],
                message=chosen_lang["save_data_message"].format(website=website, email=email, password=password))

            if is_ok:
                now = datetime.datetime.now()
                date_string = now.strftime("%m/%d/%Y")
                with open(file_path or "data.txt", "a") as data_file:
                    data_file.write(chosen_lang[f"saved_data_txt"].format(
                        website=website, email=email, password=password, date_string=date_string))

                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
                    email_entry.delete(0, END)
                    password_saved.destroy()


def change_dir():
    global file_path
    file_path = tkinter.filedialog.asksaveasfilename(initialfile="data.txt")
    if file_path:
        confirm_changed_dir.config(
            text=chosen_lang["path_set"].format(file_path=file_path), bg="light green", fg="blue")


def clear_all():
    yes_clear = messagebox.askokcancel(
        title=chosen_lang["confirm_clear_title"], message=chosen_lang["clear_all_confirmation"])
    if yes_clear:
        default_settings = {
            'theme': 'dark'
        }

        with open('src/settings.json', 'r') as f:
            try:
                settings = json.load(f)
            except json.decoder.JSONDecodeError:
                settings = default_settings
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)
        if settings['theme'] == 'dark':
            confirm_changed_dir.config(text="", bg="#2A3990", fg="#2A3990")
            pass_check_label.config(text="", bg="#2A3990", fg="#2A3990")
            password_saved.config(text="", bg="#2A3990", fg="#2A3990")
            version_message.config(text="", bg="#2A3990", fg="#2A3990")
            whats_new_label.config(text="", bg="#2A3990", fg="#2A3990")

        if settings['theme'] == 'light':
            confirm_changed_dir.config(
                text="", bg="light blue", fg="light blue")
            pass_check_label.config(text="", bg="light blue", fg="light blue")
            password_saved.config(text="", bg="light blue", fg="light blue")
            version_message.config(text="", bg="light blue", fg="light blue")
            whats_new_label.config(text="", bg="light blue", fg="light blue")


def safety():
    message = chosen_lang["""privacy_message"""]
    messagebox.showinfo(title="Safety", message=message)


def Light_Mode():
    logo_img.config(file="assets/logos/wide-light.png")
    window.wm_iconbitmap('assets/logos/logo-light.ico')
    window.config(bg="light blue")
    canvas.config(bg="light blue")
    # LABELS
    confirm_changed_dir.config(bg="#AED6F1", fg="black")
    email_label.config(bg="light blue", fg="black")
    password_check.config(bg="#AED6F1", fg="black")
    password_label.config(bg="light blue", fg="black")
    password_saved.config(bg="#AED6F1", fg="black")
    pass_check_label.config(bg="#AED6F1", fg="black")
    version_message.config(bg="#AED6F1", fg="black")
    whats_new_label.config(bg="#AED6F1", fg="black")
    website_label.config(bg="light blue", fg="black")
    # BUTTONS
    clear_all_button.config(bg="#AED6F1", fg="black")
    change_dir_button.config(bg="#AED6F1", fg="black")
    check_for_update_button.config(bg="#AED6F1", fg="black")
    exit_button.config(bg="#AED6F1", fg="black")
    generate_password_button.config(bg="#AED6F1", fg="black")
    privacy_button.config(bg="#AED6F1", fg="black")
    save_button.config(bg="#AED6F1", fg="black")
    show_button.config(bg="#AED6F1", fg="black")
    toggle_theme_button.config(text='\u263E', bg="#AED6F1", fg="black")
    help_needed_button.config(bg="#AED6F1", fg="black")
    toggle_language_button.config(bg="#AED6F1", fg="black")


def Dark_Mode():
    logo_img.config(file="assets/logos/wide.png")
    window.wm_iconbitmap('assets/logos/logo-dark.ico')
    window.config(bg="#2A3990")
    canvas.config(bg="#2A3990")
    # LABELS
    confirm_changed_dir.config(bg="#2A3990", fg="white")
    email_label.config(bg="#2A3990", fg="white")
    password_check.config(bg="#251749", fg="white")
    password_label.config(bg="#2A3990", fg="white")
    password_saved.config(bg="#2A3990", fg="white")
    pass_check_label.config(bg="#2A3990", fg="light green")
    version_message.config(bg="#2A3990", fg="light green")
    whats_new_label.config(bg="#2A3990", fg="light green")
    website_label.config(bg="#2A3990", fg="white")
    # BUTTONS
    clear_all_button.config(bg="#251749", fg="white")
    change_dir_button.config(bg="#251749", fg="white")
    check_for_update_button.config(bg="#251749", fg="white")
    exit_button.config(bg="#251749", fg="white")
    generate_password_button.config(bg="#251749", fg="white")
    privacy_button.config(bg="#251749", fg="white")
    save_button.config(bg="#251749", fg="white")
    show_button.config(bg="#251749", fg="white")
    toggle_theme_button.config(text='\u2600', bg="#251749", fg="white")
    help_needed_button.config(bg="#251749", fg="white")
    toggle_language_button.config(bg="#251749", fg="white")


def toggle_theme():
    default_settings = {
        'theme': 'dark'
    }

    try:
        with open('src/settings.json', 'r') as f:
            try:
                settings = json.load(f)
            except json.decoder.JSONDecodeError:
                settings = default_settings
    except FileNotFoundError:
        with open('src/settings.json', 'w') as f:
            json.dump(default_settings, f)
        settings = default_settings

    if 'theme' not in settings:
        settings['theme'] = default_settings['theme']
    if toggle_theme_button.cget("text") == "\u2600":  # if button has sun symbol
        Light_Mode()
        settings['theme'] = 'light'

    # if button has moon symbol
    elif toggle_theme_button.cget("text") == "\u263E":
        Dark_Mode()
        settings['theme'] = 'dark'

    with open('src/settings.json', 'w') as f:
        json.dump(settings, f)


def help_function():
    direct_to_issues = messagebox.askokcancel(title=chosen_lang["help_title"],
                                              message=chosen_lang["help_needed"])
    if direct_to_issues:
        open_issues()


def open_issues():
    link = "https://github.com/ziadh/Safe-Data/issues/new"
    webbrowser.open(link)


def toggle_language():

    default_settings = {
        'language': 'EN'
    }
    try:
        with open('src/settings.json', 'r') as f:
            try:
                settings = json.load(f)
            except json.decoder.JSONDecodeError:
                settings = default_settings
    except FileNotFoundError:
        with open('src/settings.json', 'w') as f:
            json.dump(default_settings, f)
        settings = default_settings

    if 'language' not in settings:
        settings['language'] = default_settings['language']
    with open('src/languages.json', 'r', encoding='utf8') as f:
        language_data = json.load(f)
    language = settings['language']

    for lang in language_data['languages']:
        if lang['language'] == language:
            chosen_lang = lang
            break

    if toggle_language_button.cget("text") == "ES":  # switches lang to EN
        toggle_language_button.config(text='EN')
        settings['language'] = 'ES'
        with open('src/languages.json', 'r', encoding='utf8') as f:
            language_data = json.load(f)
        for lang in language_data['languages']:
            if lang['language'] == settings['language']:
                chosen_lang = lang
                break

    elif toggle_language_button.cget("text") == "EN":  # switches lang to ES
        toggle_language_button.config(text='ES')
        settings['language'] = 'EN'
        with open('src/languages.json', 'r', encoding='utf8') as f:
            language_data = json.load(f)
        for lang in language_data['languages']:
            if lang['language'] == settings['language']:
                chosen_lang = lang
                break
    website_label.config(
        text=chosen_lang['website_label'])
    email_label.config(
        text=chosen_lang['email_label'])
    password_label.config(
        text=chosen_lang['password_label'])
    password_check.config(
        text=chosen_lang['check_pass_button'])
    check_for_update_button.config(
        text=chosen_lang['check_for_updates_button'])
    clear_all_button.config(
        text=chosen_lang['clear_all_button'])
    generate_password_button.config(
        text=chosen_lang['generate_button'])
    save_button.config(
        text=chosen_lang['save_button'])
    privacy_button.config(
        text=chosen_lang['privacy_button'])
    change_dir_button.config(
        text=chosen_lang['change_dir_button'])
    exit_button.config(
        text=chosen_lang['exit_button'])

    with open('src/settings.json', 'w') as f:
        json.dump(settings, f)

    result = tk.messagebox.askyesno(
        "Language Switch Notice", "A restart is highly recommended for the app to work properly. Would you like to restart now?")
    if result:
        window.destroy()


def on_exit():
    result = messagebox.askquestion(
        "Confirm", chosen_lang["confirm_exit"])
    if result == 'yes':
        window.destroy()


window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coord = int((screen_width / 2) - (500 / 2))
y_coord = int((screen_height / 2) - (300))
window.resizable(True, True)
window.geometry(f"700x450+{x_coord}+{y_coord}")

with open('src/settings.json', 'r') as f:
    settings = json.load(f)

version_message = Label(
    text="", fg="blue", cursor="hand2", bg="#2A3990")
version_message.bind("<Button-1>", download_update)
version_message.place(x=40, y=-20)
whats_new_label = Label(text="", fg="blue", cursor="hand2", bg="#2A3990")
whats_new_label.bind(
    "<Button-1>", lambda event: open_patch_notes(event, language, chosen_lang))
whats_new_label.place(x=40, y=20)

window.config(bg="#2A3990")
window.title(chosen_lang["window_title"].format(version=version))
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)
window.wm_iconbitmap('assets/logos/logo-dark.ico')

canvas = Canvas(height=150, width=275)
logo_img = PhotoImage(file="assets/logos/wide.png")
canvas.create_image(137, 75, image=logo_img, anchor="center")
canvas.place(x=200, y=5)

website_label = Label(
    text=chosen_lang['website_label'], bg="#2A3990", fg="white")
website_label.place(x=40, y=180)
website_entry = Entry(width=46)
website_entry.place(x=200, y=180)
website_entry.focus()

email_label = Label(text=chosen_lang['email_label'], bg="#2A3990", fg="white")
email_label.place(x=40, y=210)
email_entry = Entry(width=46)
email_entry.place(x=200, y=210)
email_entry.insert(0, "")

is_password_visible = False
password_label = Label(
    text=chosen_lang["password_label"], bg="#2A3990", fg="white")
password_label.place(x=40, y=240)
password_entry = Entry(show="*", width=21)
password_entry.place(x=200, y=240)

password_saved = Label(
    text=chosen_lang["password_saved_label"], bg="light green", fg="blue")

show_button = tk.Button(window, text="\U0001F441",
                        command=toggle_password_visibility, bg="#251749", fg="white")
show_button.place(x=350, y=240)

generate_password_button = Button(
    text=chosen_lang["generate_button"], command=randomize_password, bg="#251749", fg="white", width=12)
generate_password_button.place(x=390, y=240)

password_check = Button(text=chosen_lang["check_pass_button"],
                        bg="#251749", fg="white", command=check_pass, width=17)
password_check.place(x=40, y=270)

check_for_update_button = Button(text=chosen_lang["check_for_updates_button"], bg="#251749",
                                 fg="white", command=version_checker, width=17)
check_for_update_button.place(x=40, y=300)
save_button = Button(text=chosen_lang["save_button"], width=39, command=save,
                     bg="#251749", fg="white")
save_button.place(x=200, y=270)

privacy_button = Button(text=chosen_lang["privacy_button"], width=15,
                        command=safety, bg="#251749", fg="white")
privacy_button.place(x=200, y=300)

change_dir_button = Button(
    text=chosen_lang["change_dir_button"], width=17, command=change_dir, bg="#251749", fg="white")
change_dir_button.place(x=353, y=300)

exit_button = Button(text=chosen_lang["exit_button"], width=17,
                     command=on_exit, bg="#251749", fg="white")
exit_button.place(x=353, y=330)

toggle_theme_button = Button(text="\u263E", width=3,
                             command=toggle_theme, bg="#251749", fg="white")
toggle_theme_button.place(x=200, y=330)
help_needed_button = Button(text="?", width=3,
                            command=help_function, bg="#251749", fg="white")
help_needed_button.place(x=243, y=330)
toggle_language_button = Button(text="ES", width=3,
                                command=toggle_language, bg="#251749", fg="white")
toggle_language_button.place(x=285, y=330)
password_saved = Label(
    text=chosen_lang["password_saved_label"], bg="light green", fg="blue")

clear_all_button = Button(text=chosen_lang["clear_all_button"], width=17,
                          command=clear_all, bg="#251749", fg="white")
clear_all_button.place(x=40, y=330)

pass_check_label = Label(text="", bg="#2A3990")
pass_check_label.place(x=485, y=240)

confirm_changed_dir = Label(text="", bg="#2A3990")
confirm_changed_dir.place(x=40, y=360)

if settings['theme'] == 'light':
    Light_Mode()
else:
    Dark_Mode()

window.mainloop()


sys.stderr.close()
if os.path.getsize(log_path) == 0:
    os.remove(log_path)
    os.rmdir(log_folder)
