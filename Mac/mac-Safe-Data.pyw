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
import textwrap

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
# with open('src/settings.json', 'w') as f:
#     json.dump(settings, f)


def version_checker():
    r = requests.get("https://api.github.com/repos/ziadh/Safe-Data/releases")
    json_data = r.json()
    newest_version = json_data[0]["tag_name"]
    if float(newest_version) > float(version):
        version_message.config(fg="light green",
                               text=chosen_lang["version_needs_update"].format(newest_version))
        #mac has its own language value because different layout 
        whats_new_label.config(fg="light green",
                               text=chosen_lang["view_patch_notes_mac"])
    else:
        version_message.config(
            text=chosen_lang["latest_version_message"].format(version), cursor="")
        whats_new_label.config(fg="light green",
                               text=chosen_lang["view_patch_notes_mac"])
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

    if settings['theme'] == 'Light':
        label = tk.Label(ss, text="", bg="light blue")
        image = PhotoImage(file='assets/logos/splash-light.png')
    if settings['theme'] == 'Dark':
        label = tk.Label(ss, text="", bg="#2A3990")
        image = PhotoImage(file='assets/logos/splash-dark.png')
    if settings['theme'] == 'Classic Light':
        label = tk.Label(ss, text="", bg="light blue")
        image = PhotoImage(file='assets/logos/classic-splash-light.png')
    if settings['theme'] == 'Classic Dark':
        label = tk.Label(ss, text="", bg="#2A3990")
        image = PhotoImage(file='assets/logos/classic-splash-dark.png')
    label.place(x=-10, y=-10)
    image_label = Label(ss, image=image)
    image_label.place(x=0, y=0)
    progress = ttk.Progressbar(ss, orient=tk.HORIZONTAL, length=300)
    progress.configure(style='orange.Horizontal.TProgressbar')
    progress.place(x=100, y=150)
    progress['value'] = 0
    interval = 0.01
    for i in range(100):
        progress['value'] = i
        label['text'] = f"{i}%"
        ss.update_idletasks()
        time.sleep(interval)
    ss.destroy()

def show_or_hide():
    if show_button.cget('text')==chosen_lang['show_button']:
        toggle_password_visibility()
        show_button.configure(text=chosen_lang['hide_button'])
    else:
        toggle_password_visibility()
        show_button.configure(text=chosen_lang['show_button'])

def toggle_password_visibility():
    global is_password_visible
    is_password_visible = not is_password_visible
    password_entry.config(show=("" if is_password_visible else "*"))


def randomize_password():
    if settings['theme'] == 'Light':
        pass_check_label.config(text="", bg="light blue", fg="light blue")
    if settings['theme'] == 'Dark':
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
    weak_pass = ["pass", "password", "123456", "123", "000", "qwerty", "1111", "2222", "qwerty123", "abc123", "password123", "!@#%^&*", "qazwsxedcrfv", "qwertyuiopasdfghjklzxcvbnm",
                 "qwertyuio", "qwerasdfzxcv", "1qaz2wsx3edc", "1q2w3e4r5t", "admin", "letmein", "welcome", "monkey", "sunshine", "superman", "666666", "121212", "123123", "abcabc", "aaa111",
                 "password"]
    is_safe = True
    for word in weak_pass:
        if word in password:
            is_safe = False
            break
    if is_safe:
        pass_check_label.config(
            text=chosen_lang["check_pass_good"], bg="light green", fg="blue")
    else:
        pass_check_label.config(
            text=chosen_lang["check_pass_bad"], bg="red", fg="white")
    if password == "":
        pass_check_label.config(
            text=chosen_lang["check_pass_missing"], bg="yellow", fg="blue")
    if len(password) < 8 and len(password) > 0:
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
        if data_type == "TXT":
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
        if data_type == "JSON":
                if file_path == None:
                    is_ok = messagebox.askokcancel(
                        title=chosen_lang["save_data_title"],
                        message=chosen_lang["save_data_message"].format(website=website, email=email, password=password))
        
                    if is_ok:
                        now = datetime.datetime.now()
                        date_string = now.strftime("%m/%d/%Y")
        
                        data = {
                            "website": website,
                            "email": email,
                            "password": password,
                            "date": date_string
                        }
                        with open(file_path or "data.json", "a") as data_file:
                            json.dump(data, data_file, indent=2)
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
        
                        data = {
                            "website": website,
                            "email": email,
                            "password": password,
                            "date": date_string
                        }
        
                        with open(file_path or "data.json", "a") as data_file:
                            json.dump(data, data_file, indent=2)
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


def change_data_type():
    with open('src/settings.json', 'r') as f:
        settings = json.load(f)
    data_type = settings['data_type']
    if data_type == "TXT":
        data_type = "JSON"
        settings['data_type'] = 'JSON'
        saving_as_button.config(text=chosen_lang["saving_as_button"].format(data_type=data_type))
    else:
        data_type = "TXT"
        settings['data_type'] = 'TXT'
        saving_as_button.config(text=chosen_lang["saving_as_button"].format(data_type=data_type))

    with open('src/settings.json', 'w') as f:
        json.dump(settings, f)


def clear_all():

    yes_clear = messagebox.askokcancel(
        chosen_lang["confirm_clear_title"], chosen_lang["clear_all_confirmation"])
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

        if settings['theme'] == 'Dark':
            confirm_changed_dir.config(text="", bg="#13005A", fg="#13005A")
            pass_check_label.config(text="", bg="#13005A", fg="#13005A")
            password_saved.config(text="", bg="#13005A", fg="#13005A")
            version_message.config(text="", bg="#13005A", fg="#13005A")
            whats_new_label.config(text="", bg="#13005A", fg="#13005A")

        if settings['theme'] == 'Light':
            confirm_changed_dir.config(text="", bg="#E3F6FF", fg="#E3F6FF")
            pass_check_label.config(text="", bg="#E3F6FF", fg="#E3F6FF")
            password_saved.config(text="", bg="#E3F6FF", fg="#E3F6FF")
            version_message.config(text="", bg="#E3F6FF", fg="#E3F6FF")
            whats_new_label.config(text="", bg="#E3F6FF", fg="#E3F6FF")

        if settings['theme'] == 'Classic Dark':
            confirm_changed_dir.config(text="", bg="#2A3990", fg="#2A3990")
            pass_check_label.config(text="", bg="#2A3990", fg="#2A3990")
            password_saved.config(text="", bg="#2A3990", fg="#2A3990")
            version_message.config(text="", bg="#2A3990", fg="#2A3990")
            whats_new_label.config(text="", bg="#2A3990", fg="#2A3990")

        if settings['theme'] == 'Classic Light':
            confirm_changed_dir.config(
                text="", bg="light blue", fg="light blue")
            pass_check_label.config(
                text="", bg="light blue", fg="light blue")
            password_saved.config(
                text="", bg="light blue", fg="light blue")
            version_message.config(
                text="", bg="light blue", fg="light blue")
            whats_new_label.config(
                text="", bg="light blue", fg="light blue")

def safety():
    message = chosen_lang["""privacy_message"""]
    messagebox.showinfo(title="Safety", message=message)


def Dark_Mode():
    logo_img.config(file="assets/logos/wide.png")
    window.wm_iconbitmap('assets/logos/logo-dark.ico')
    window.config(bg="#13005A")
    canvas.config(bg="#13005A")
    for button in buttons:
        button.config(bg = '#2F58CD',fg = 'white')
    for label in element_labels:
        label.config(bg="#13005A",fg = 'white')
    toggle_theme_button.config(text="\u263C")
    # HIDDEN LABELS
    pass_check_label.config(bg="#13005A", fg="light green")
    version_message.config(bg="#13005A", fg="light green")
    whats_new_label.config(bg="#13005A", fg="light green")

def Light_Mode():
    logo_img.config(file="assets/logos/wide-light.png")
    window.wm_iconbitmap('assets/logos/logo-light.ico')
    window.config(bg="#E3F6FF")
    canvas.config(bg="#E3F6FF")
    for button in buttons:
        button.config(bg ='#AED6F1', fg = 'black')
    for label in element_labels:
        label.config(bg="#E3F6FF",fg = 'black')
    # LABELS
    pass_check_label.config(bg="#E3F6FF", fg="black")
    version_message.config(bg="#E3F6FF", fg="black")
    whats_new_label.config(bg="#E3F6FF", fg="black")
    toggle_theme_button.config(text="\u263E")


def Classic_Light_Mode():
    logo_img.config(file="assets/logos/classic-wide-light.png")
    window.wm_iconbitmap('assets/logos/classic-logo-light.ico')
    window.config(bg="light blue")
    canvas.config(bg="light blue")
    for button in buttons:
        button.config(bg ='#AED6F1', fg = 'black')
    for label in element_labels:
        label.config(bg="light blue",fg = 'black')
    # LABELS
    pass_check_label.config(bg="#AED6F1", fg="black")
    version_message.config(bg="#AED6F1", fg="black")
    whats_new_label.config(bg="#AED6F1", fg="black")
    toggle_theme_button.config(text="\u263D")


def Classic_Dark_Mode():
    logo_img.config(file="assets/logos/classic-wide.png")
    window.wm_iconbitmap('assets/logos/classic-logo-dark.ico')
    window.config(bg="#2A3990")
    canvas.config(bg="#2A3990")
    for button in buttons:
        button.config(bg ='#251749', fg = 'white')
    for label in element_labels:
        label.config(bg="#2A3990",fg = 'white')
    # LABELS
    pass_check_label.config(bg="#2A3990", fg="light green")
    version_message.config(bg="#2A3990", fg="light green")
    whats_new_label.config(bg="#2A3990", fg="light green")
    # BUTTONS
    toggle_theme_button.config(text="\u2600")

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
    elif settings['theme'] == 'Dark':
        settings['theme'] = 'Light'
        Light_Mode()
    elif settings['theme'] == 'Light':
        Classic_Dark_Mode()
        settings['theme'] = 'Classic Dark'
    elif settings['theme'] == 'Classic Dark':
        Classic_Light_Mode()
        settings['theme'] = 'Classic Light'
    elif settings['theme'] == 'Classic Light':
        Dark_Mode()
        settings['theme'] = 'Dark'
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
    password_check_button.config(
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
    show_button.config(text=chosen_lang['show_button'])
    shortcuts_button.config(text=chosen_lang['shortcuts'])

    with open('src/settings.json', 'w') as f:
        json.dump(settings, f)

    result = tk.messagebox.askyesno(
        chosen_lang["language_switch_notice_title"], chosen_lang["language_switch_notice_text"])
    if result:
        window.destroy()


def on_exit():
    result = messagebox.askquestion(
        "Confirm", chosen_lang["confirm_exit"])
    if result == 'yes':
        window.destroy()


def on_enter(e, btn):
    with open('src/settings.json', 'r') as f:
        settings = json.load(f)
    theme = settings['theme']

    if theme == "Dark":
        btn.config(bg='#86A3B8')
    if theme == "Light":
        btn.config(bg='#E5E0FF')
    if theme == "Classic Dark":
        btn.config(bg='black')
    if theme == "Classic Light":
        btn.config(bg='#ECECEC')
        btn.config(bg='#ECECEC')


def on_leave(e, btn):
    with open('src/settings.json', 'r') as f:
        settings = json.load(f)
    theme = settings['theme']

    if theme == "Dark":
        btn.config(bg='#2F58CD')
    if theme == "Light":
        btn.config(bg='#AED6F1')
    if theme == "Classic Dark":
        btn.config(bg='#251749')
    if theme == "Classic Light":
        btn.config(bg='light blue')



def show_shortcuts():
    shortcuts_window = tk.Toplevel(window)
    shortcuts_window.withdraw()
    shortcuts_window.title("Shortcuts")
    shortcuts_window.wm_iconbitmap('assets/logos/logo-dark.ico')
    shortcuts_window_height = 650
    shortcuts_window_width = 600
    shortcuts_window.resizable(False, False)
    shortcuts_window.config(bg="#2A3990")
    main_window_x = window.winfo_x()
    main_window_y = window.winfo_y()
    main_window_width = window.winfo_width()
    main_window_height = window.winfo_height()
    x = main_window_x + main_window_width/2 - shortcuts_window_width/2
    y = main_window_y + main_window_height/2 - shortcuts_window_height/2
    shortcuts_window.geometry(
        f"{shortcuts_window_width}x{shortcuts_window_height}+{int(x)}+{int(y)}")
    shortcuts_window.deiconify()

    shortcuts_top_label = Label(
        shortcuts_window, text=chosen_lang["shortcuts"], bg="#2A3990", fg="white", font=("Arial", 25))
    shortcuts_top_label.place(x=220, y=30)

    shortcuts = chosen_lang['shortcuts_text']

    indentend_shortcuts = textwrap.indent(shortcuts, '    ')
    shortcuts_label = Label(shortcuts_window, text=indentend_shortcuts,
                            bg="#13005A", fg="white", font=("Arial", 16), pady=20)

    shortcuts_label.place(x=110, y=80)


def about():
    version_released = ''
    version_unreleased = ''
    if is_released != '':
        version_unreleased = messagebox.askokcancel(
            chosen_lang['about_title'], chosen_lang['about_unreleased'])
    else:
        version_released = messagebox.askokcancel(
            chosen_lang['about_title'], chosen_lang['about_released'].format(version=version))
    if version_unreleased:
        download_update()
    elif version_released:
        open_issues()

window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coord = int((screen_width / 2) - (500 / 2))
y_coord = int((screen_height / 2) - (300))
window.resizable(True, True)
window.geometry(f"700x480+{x_coord}+{y_coord}")

with open('src/settings.json', 'r') as f:
    settings = json.load(f)
is_released = settings['is_released?']

version_message = Label(
    text="", fg="blue", cursor="hand2", bg="#2A3990")
version_message.bind("<Button-1>", download_update)
version_message.place(x=40, y=-20)
whats_new_label = Label(text="", fg="blue", cursor="hand2", bg="#2A3990")
whats_new_label.bind(
    "<Button-1>", lambda event: open_patch_notes(event, language, chosen_lang))
whats_new_label.place(x=40, y=20)

window.config(bg="#2A3990")
window.title(chosen_lang["window_title"].format(version=version)+" - Mac")
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)
window.wm_iconbitmap('assets/logos/logo-dark.ico')

canvas = Canvas(height=150, width=275)
logo_img = PhotoImage(file="assets/logos/wide.png")
canvas.create_image(137, 75, image=logo_img, anchor="center")
canvas.place(x=200, y=5)


#### SHORTCUTS BELOW ####
window.bind("<Command-A>", lambda _: about_button.invoke())
window.bind("<Command-a>", lambda _: about_button.invoke())
window.bind("<Command-S>", lambda _: save_button.invoke())
window.bind("<Command-s>", lambda _: save_button.invoke())
window.bind("<Return>", lambda _: save_button.invoke())
window.bind("<Command-G>", lambda _: generate_password_button.invoke())
window.bind("<Command-g>", lambda _: generate_password_button.invoke())
window.bind("<Command-U>", lambda _: check_for_update_button.invoke())
window.bind("<Command-u>", lambda _: check_for_update_button.invoke())
window.bind("<Command-X>", lambda _: clear_all_button.invoke())
window.bind("<Command-x>", lambda _: clear_all_button.invoke())
window.bind("<Command-`>", lambda _: shortcuts_button.invoke())
window.bind("<Command-E>", lambda _: password_check_button.invoke())
window.bind("<Command-e>", lambda _: password_check_button.invoke())
window.bind("<Command-P>", lambda _: privacy_button.invoke())
window.bind("<Command-p>", lambda _: privacy_button.invoke())
window.bind("<Command-2>", lambda _: change_dir_button.invoke())
window.bind("<Command-T>", lambda _: toggle_theme_button.invoke())
window.bind("<Command-t>", lambda _: toggle_theme_button.invoke())
window.bind("<Command-L>", lambda _: toggle_language_button.invoke())
window.bind("<Command-l>", lambda _: toggle_language_button.invoke())
window.bind("<Command-.>", lambda _: saving_as_button.invoke())

#### SHORTCUTS ABOVE ####

website_label = Label(
    text=chosen_lang['website_label'], bg="#2A3990", fg="white", font=("Verdana", 11))
website_label.place(x=40, y=180)
website_entry = Entry(width=46)
website_entry.place(x=200, y=180)
website_entry.focus()

email_label = Label(text=chosen_lang['email_label'], bg="#2A3990", fg="white", font=("Verdana", 11))
email_label.place(x=40, y=210)
email_entry = Entry(width=46)
email_entry.place(x=200, y=210)
email_entry.insert(0, "")

is_password_visible = False
password_label = Label(
    text=chosen_lang["password_label"], bg="#2A3990", fg="white", font=("Verdana", 11))
password_label.place(x=40, y=240)
password_entry = Entry(show="*", width=21)
password_entry.place(x=200, y=240)

password_saved = Label(
    text=chosen_lang["password_saved_label"], bg="light green", fg="blue")

show_button = tk.Button(window, text="Show",
                        command=show_or_hide, bg="#251749", fg="white")
show_button.bind("<Control-b>", show_or_hide)
show_button.place(x=410, y=240)

generate_password_button = Button(
    text=chosen_lang["generate_button"], command=randomize_password, bg="#251749", fg="white", width=12, font=("Verdana", 8))
generate_password_button.place(x=475, y=240)

password_check_button = Button(text=chosen_lang["check_pass_button"],
                               bg="#251749", fg="white", command=check_pass, width=17, font=("Verdana", 8))
password_check_button.place(x=40, y=270)

check_for_update_button = Button(text=chosen_lang["check_for_updates_button"], bg="#251749",
                                 fg="white", command=version_checker, width=17, font=("Verdana", 8))
check_for_update_button.place(x=40, y=300)
save_button = Button(text=chosen_lang["save_button"], width=39, command=save,
                     bg="#251749", fg="white", font=("Verdana", 8))
save_button.place(x=240, y=270)

toggle_theme_button = Button(text="\u263E", width=3,
                             command=toggle_theme, bg="#251749", fg="white", font=("Verdana", 8))
toggle_theme_button.place(x=230, y=330)

toggle_language_button = Button(text="ES", width=3,
                                command=toggle_language, bg="#251749", fg="white", font=("Verdana", 8))
toggle_language_button.place(x=350, y=330)

privacy_button = Button(text=chosen_lang["privacy_button"], width=17,
                        command=safety, bg="#251749", fg="white", font=("Verdana", 8))
privacy_button.place(x=230, y=300)
data_type = settings['data_type']

saving_as_button = Button(text=chosen_lang['saving_as_button'].format(data_type=data_type), width=17,
                          command=change_data_type, bg="#251749", fg="white", font=("Verdana", 8))

saving_as_button.place(x=423, y=330)

change_dir_button = Button(
    text=chosen_lang["change_dir_button"],font=("Verdana", 8), width=17, command=change_dir, bg="#251749", fg="white")
change_dir_button.place(x=423, y=300)

exit_button = Button(text=chosen_lang["exit_button"], width=17,
                     command=on_exit, bg="#251749", fg="white", font=("Verdana", 8))
exit_button.place(x=373, y=360)

password_saved = Label(
    text=chosen_lang["password_saved_label"], bg="light green", fg="blue")

clear_all_button = Button(text=chosen_lang["clear_all_button"], width=17,
                          command=clear_all, bg="#251749", fg="white", font=("Verdana", 8))
clear_all_button.place(x=40, y=360)

pass_check_label = Label(text="", bg="#2A3990")
pass_check_label.place(x=470, y=10)

confirm_changed_dir = Label(text="", bg="#2A3990")
confirm_changed_dir.place(x=40, y=390)

shortcuts_button = Button(text=chosen_lang["shortcuts"], width=17,
                          command=show_shortcuts, bg="#251749", fg="white", font=("Verdana", 8))
shortcuts_button.place(x=230, y=360)

about_button = Button(text=chosen_lang["about_button"], width=17,
                      bg="#251749", fg="white", font=("Verdana", 8), command=about)
about_button.place(x=40, y=330)

buttons = [generate_password_button,  clear_all_button, save_button, password_check_button, about_button, saving_as_button, show_button,
           privacy_button,  change_dir_button, exit_button, check_for_update_button, toggle_language_button, toggle_theme_button, shortcuts_button]
element_labels = [website_label,password_saved,password_label,email_label,confirm_changed_dir]
for btn in buttons:
    btn.bind("<Enter>", lambda e, btn=btn: on_enter(e, btn))
    btn.bind("<Leave>", lambda e, btn=btn: on_leave(e, btn))

if settings['theme'] == 'Light':
    Light_Mode()
if settings['theme'] == 'Dark':
    Dark_Mode()
if settings['theme'] == 'Classic Dark':
    Classic_Dark_Mode()
if settings['theme'] == 'Classic Light':
    Classic_Light_Mode()
if language == 'EN':
    change_dir_button.config(width=17)
    check_for_update_button.config(width=17)
    email_label.config(font=("Verdana", 11))
if language == 'ES':
    change_dir_button.config(width=19)
    check_for_update_button.config(width=19)
    email_label.config(font=("Verdana", 8))
with open('src/settings.json', 'w') as f:
    json.dump(settings, f)
window.mainloop()


sys.stderr.close()
if os.path.getsize(log_path) == 0:
    os.remove(log_path)
    os.rmdir(log_folder)
