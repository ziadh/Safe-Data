import tkinter.filedialog
from tkinter import *
from tkinter import messagebox, Canvas, PhotoImage, Label
import tkinter as tk
from tkinter import ttk
import customtkinter as CTk

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
from src.themes import *


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
theme = settings['theme']

with open('src/languages.json', 'r', encoding='utf8') as f:
    language_data = json.load(f)
for lang in language_data['languages']:
    if lang['language'] == language:
        chosen_lang = lang
        break


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


def download_update():
    r = requests.get("https://api.github.com/repos/ziadh/Safe-Data/releases")
    json_data = r.json()
    newest_version = json_data[0]["tag_name"]
    link = "https://github.com/ziadh/Safe-Data/archive/refs/tags/"+newest_version+".zip"
    webbrowser.open(link)


def open_patch_notes(language, chosen_lang):

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
    interval = 0.0005
    for i in range(100):
        progress['value'] = i
        label['text'] = f"{i}%"
        ss.update_idletasks()
        time.sleep(interval)
    ss.destroy()


def show_or_hide():
    if show_button.cget('text') == chosen_lang['show_button']:
        toggle_password_visibility()
        show_button.configure(text=chosen_lang['hide_button'])
    else:
        toggle_password_visibility()
        show_button.configure(text=chosen_lang['show_button'])


def toggle_password_visibility():
    global is_password_visible
    is_password_visible = not is_password_visible
    password_entry.config(show=("" if is_password_visible else "*"))


def open_dev():
    pass


def dev_show_all():
    confirm_changed_dir.config(text=chosen_lang["path_set"].format(
        file_path=file_path), bg="light green", fg="blue")
    pass_check_label.config(
        text=chosen_lang["check_pass_bad"], bg="red", fg="white")
    password_saved.config(text=chosen_lang["password_saved_label"])
    version_message.config(fg="light green",
                           text=chosen_lang["version_needs_update"])
    whats_new_label.config(fg="light green",
                           text=chosen_lang["view_patch_notes"])


def randomize_password():
    global website_entry
    website = website_entry.get()
    if website == "?":
        open_dev()
    elif website == "!":
        dev_show_all()
    else:
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
            "Oops", chosen_lang["all_fields_error"])
    else:
        if data_type == "TXT":
            if file_path == None:
                is_ok = messagebox.askokcancel(
                    chosen_lang["save_data_title"],
                    chosen_lang["save_data_message"].format(website=website, email=email, password=password, data_type=data_type))

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
                    chosen_lang["save_data_title"],
                    chosen_lang["save_data_message"].format(website=website, email=email, password=password))

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
                    chosen_lang["save_data_title"],
                    chosen_lang["save_data_message"].format(website=website, email=email, password=password, data_type=data_type))

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
                    chosen_lang["save_data_title"],
                    chosen_lang["save_data_message"].format(website=website, email=email, password=password))

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
    else:
        confirm_changed_dir.config(
            text=chosen_lang["change_dir_unsuccessful"], fg="white", bg='red')


def change_data_type():
    data_type = settings['data_type']
    if data_type == "TXT":
        data_type = "JSON"
        settings['data_type'] = 'JSON'
        saving_as_button.config(
            text=chosen_lang["saving_as_button"].format(data_type=data_type))
    else:
        data_type = "TXT"
        settings['data_type'] = 'TXT'
        saving_as_button.config(
            text=chosen_lang["saving_as_button"].format(data_type=data_type))

    with open('src/settings.json', 'w') as f:
        json.dump(settings, f)


def clear_input():
    yes_clear = messagebox.askokcancel(
        chosen_lang["confirm_clear_input_title"], chosen_lang["clear_input_confirmation"])
    if yes_clear:
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)


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
            confirm_changed_dir.config(
                text="", bg=DEFAULT_DM_LABELS_BG_COLOR, fg=DEFAULT_DM_LABELS_BG_COLOR)
            pass_check_label.config(
                text="", bg=DEFAULT_DM_LABELS_BG_COLOR, fg=DEFAULT_DM_LABELS_BG_COLOR)
            password_saved.config(
                text="", bg=DEFAULT_DM_LABELS_BG_COLOR, fg=DEFAULT_DM_LABELS_BG_COLOR)
            version_message.config(
                text="", bg=DEFAULT_DM_LABELS_BG_COLOR, fg=DEFAULT_DM_LABELS_BG_COLOR)
            whats_new_label.config(
                text="", bg=DEFAULT_DM_LABELS_BG_COLOR, fg=DEFAULT_DM_LABELS_BG_COLOR)

        if settings['theme'] == 'Light':
            confirm_changed_dir.config(
                text="", bg=DEFAULT_LM_LABELS_BG_COLOR, fg=DEFAULT_LM_LABELS_BG_COLOR)
            pass_check_label.config(
                text="", bg=DEFAULT_LM_LABELS_BG_COLOR, fg=DEFAULT_LM_LABELS_BG_COLOR)
            password_saved.config(
                text="", bg=DEFAULT_LM_LABELS_BG_COLOR, fg=DEFAULT_LM_LABELS_BG_COLOR)
            version_message.config(
                text="", bg=DEFAULT_LM_LABELS_BG_COLOR, fg=DEFAULT_LM_LABELS_BG_COLOR)
            whats_new_label.config(
                text="", bg=DEFAULT_LM_LABELS_BG_COLOR, fg=DEFAULT_LM_LABELS_BG_COLOR)

        if settings['theme'] == 'Classic Dark':
            confirm_changed_dir.config(
                text="", bg=DEFAULT_CDM_LABELS_BG_COLOR, fg=DEFAULT_CDM_LABELS_BG_COLOR)
            pass_check_label.config(
                text="", bg=DEFAULT_CDM_LABELS_BG_COLOR, fg=DEFAULT_CDM_LABELS_BG_COLOR)
            password_saved.config(
                text="", bg=DEFAULT_CDM_LABELS_BG_COLOR, fg=DEFAULT_CDM_LABELS_BG_COLOR)
            version_message.config(
                text="", bg=DEFAULT_CDM_LABELS_BG_COLOR, fg=DEFAULT_CDM_LABELS_BG_COLOR)
            whats_new_label.config(
                text="", bg=DEFAULT_CDM_LABELS_BG_COLOR, fg=DEFAULT_CDM_LABELS_BG_COLOR)

        if settings['theme'] == 'Classic Light':
            confirm_changed_dir.config(
                text="", bg=DEFAULT_CLM_LABELS_BG_COLOR, fg=DEFAULT_CLM_LABELS_BG_COLOR)
            pass_check_label.config(
                text="", bg=DEFAULT_CLM_LABELS_BG_COLOR, fg=DEFAULT_CLM_LABELS_BG_COLOR)
            password_saved.config(
                text="", bg=DEFAULT_CLM_LABELS_BG_COLOR, fg=DEFAULT_CLM_LABELS_BG_COLOR)
            version_message.config(
                text="", bg=DEFAULT_CLM_LABELS_BG_COLOR, fg=DEFAULT_CLM_LABELS_BG_COLOR)
            whats_new_label.config(
                text="", bg=DEFAULT_CLM_LABELS_BG_COLOR, fg=DEFAULT_CLM_LABELS_BG_COLOR)


def safety():
    message = chosen_lang["""privacy_message"""]
    messagebox.showinfo(chosen_lang["privacy_title"], message)



def automatic_theme():
    global theme,current_hour
    theme = "Automatic"
    automatic_help_button.place(x=540, y=430)
    current_hour = datetime.datetime.now().hour
    if 6 <= current_hour < 18:
        Light_Mode()
    else:
        Dark_Mode()


def Dark_Mode():
    logo_img.config(file="assets/logos/wide_dark.png")
    window.wm_iconbitmap('assets/logos/logo-dark.ico')
    github_page_button.configure(image=github_logo)
    window.config(bg=DEFAULT_DM_BG_COLOR)
    canvas.config(bg=DEFAULT_DM_BG_COLOR)
    for button in buttons:
        button.config(bg=DEFAULT_DM_BUTTONS_BG_COLOR,
                      fg=DEFAULT_DM_BUTTONS_FG_COLOR)
    for label in element_labels:
        label.config(bg=DEFAULT_DM_BG_COLOR, fg=DEFAULT_DM_BUTTONS_FG_COLOR)
    # HIDDEN LABELS
    pass_check_label.config(bg=DEFAULT_DM_BG_COLOR,
                            fg=DEFAULT_DM_LABELS_FG_COLOR)
    version_message.config(bg=DEFAULT_DM_BG_COLOR,
                           fg=DEFAULT_DM_LABELS_FG_COLOR)
    whats_new_label.config(bg=DEFAULT_DM_BG_COLOR,
                           fg=DEFAULT_DM_LABELS_FG_COLOR)


def Light_Mode():
    logo_img.config(file="assets/logos/wide_light.png")
    window.wm_iconbitmap('assets/logos/logo-light.ico')
    github_page_button.configure(image=github_logo)
    window.config(bg=DEFAULT_LM_BG_COLOR)
    canvas.config(bg=DEFAULT_LM_BG_COLOR)
    for button in buttons:
        button.config(bg=DEFAULT_LM_BUTTONS_BG_COLOR,
                      fg=DEFAULT_LM_BUTTONS_FG_COLOR)
    for label in element_labels:
        label.config(bg=DEFAULT_LM_BG_COLOR, fg=DEFAULT_LM_BUTTONS_FG_COLOR)
    # LABELS
    pass_check_label.config(bg=DEFAULT_LM_BG_COLOR,
                            fg=DEFAULT_LM_BUTTONS_FG_COLOR)
    version_message.config(bg=DEFAULT_LM_BG_COLOR,
                           fg=DEFAULT_LM_BUTTONS_FG_COLOR)
    whats_new_label.config(bg=DEFAULT_LM_BG_COLOR,
                           fg=DEFAULT_LM_BUTTONS_FG_COLOR)


def Classic_Light_Mode():
    logo_img.config(file="assets/logos/wide_light.png")
    window.wm_iconbitmap('assets/logos/classic-logo-light.ico')
    window.config(bg=DEFAULT_CLM_BG_COLOR)
    canvas.config(bg=DEFAULT_CLM_BG_COLOR)
    github_page_button.configure(image=github_logo)
    for button in buttons:
        button.config(bg=DEFAULT_LM_BUTTONS_BG_COLOR,
                      fg=DEFAULT_CLM_BUTTONS_FG_COLOR)
    for label in element_labels:
        label.config(bg=DEFAULT_CLM_BG_COLOR, fg=DEFAULT_CLM_BUTTONS_FG_COLOR)
    # LABELS
    pass_check_label.config(bg=DEFAULT_CLM_LABELS_BG_COLOR,
                            fg=DEFAULT_CLM_BUTTONS_FG_COLOR)
    version_message.config(bg=DEFAULT_CLM_LABELS_BG_COLOR,
                           fg=DEFAULT_CLM_BUTTONS_FG_COLOR)
    whats_new_label.config(bg=DEFAULT_CLM_LABELS_BG_COLOR,
                           fg=DEFAULT_CLM_BUTTONS_FG_COLOR)


def Classic_Dark_Mode():
    logo_img.config(file="assets/logos/wide_dark.png")
    window.wm_iconbitmap('assets/logos/classic-logo-dark.ico')
    github_page_button.configure(image=github_white)
    window.config(bg=DEFAULT_CDM_BG_COLOR)
    canvas.config(bg=DEFAULT_CDM_BG_COLOR)
    for button in buttons:
        button.config(bg=DEFAULT_CDM_BUTTONS_BG_COLOR,
                      fg=DEFAULT_CDM_BUTTONS_FG_COLOR)
    for label in element_labels:
        label.config(bg=DEFAULT_CDM_BG_COLOR, fg=DEFAULT_CDM_BUTTONS_FG_COLOR)
    # LABELS
    pass_check_label.config(bg=DEFAULT_CDM_BG_COLOR,
                            fg=DEFAULT_CDM_LABELS_FG_COLOR)
    version_message.config(bg=DEFAULT_CDM_BG_COLOR,
                           fg=DEFAULT_CDM_LABELS_FG_COLOR)
    whats_new_label.config(bg=DEFAULT_CDM_BG_COLOR,
                           fg=DEFAULT_CDM_LABELS_FG_COLOR)


def get_current_theme():
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
    return settings.get('theme', default_settings['theme'])


def get_current_language():
    default_settings = {
        'language': 'English'
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

    return settings.get('language', default_settings['language'])


def change_theme(selected_option):
    automatic_help_button.place_forget()
    theme_selected = selected_option
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
    elif theme_selected == chosen_lang["Dark_theme"]:
        settings['theme'] = 'Dark'
        Dark_Mode()
    elif theme_selected == chosen_lang["Light_theme"]:
        Light_Mode()
        settings['theme'] = 'Light'
    elif theme_selected == chosen_lang["Classic_Dark_theme"]:
        Classic_Dark_Mode()
        settings['theme'] = 'Classic Dark'
    elif theme_selected == chosen_lang["Classic_Light_theme"]:
        Classic_Light_Mode()
        settings['theme'] = 'Classic Light'
    else:
        automatic_theme()
    with open('src/settings.json', 'w') as f:
        json.dump(settings, f)
        theme_selected = settings['theme']


def help_function():
    direct_to_issues = messagebox.askokcancel(chosen_lang["help_title"],
                                              chosen_lang["help_needed"])
    if direct_to_issues:
        open_issues()


def open_issues():
    link = "https://github.com/ziadh/Safe-Data/issues/new"
    webbrowser.open(link)


def toggle_language(selected_language):
    chosen_lang = selected_language

    default_settings = {
        'language': 'English'
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
    language = chosen_lang if chosen_lang else settings['language']

    for lang in language_data['languages']:
        if lang['language'] == language:
            chosen_lang = lang
            break

    if selected_language == "Español":
        change_dir_button.config(width=19)
        check_for_update_button.config(width=19)
        email_label.config(font=("Verdana", 8))

        settings['language'] = 'Español'
        with open('src/languages.json', 'r', encoding='utf8') as f:
            language_data = json.load(f)
        for lang in language_data['languages']:
            if lang['language'] == settings['language']:
                chosen_lang = lang
                break

    elif selected_language == "English":
        change_dir_button.config(width=17)
        check_for_update_button.config(width=17)
        email_label.config(font=("Verdana", 11))

        settings['language'] = 'English'
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
    clear_input_button.config(text=chosen_lang["clear_input_button"])
    clear_all_button.config(
        text=chosen_lang['clear_all_button'])
    generate_password_button.config(
        text=chosen_lang['generate_button'])
    save_button.config(
        text=chosen_lang['save_button'])
    saving_as_button.config(
        text=chosen_lang['saving_as_button'].format(data_type=data_type))
    privacy_button.config(
        text=chosen_lang['privacy_button'])
    change_dir_button.config(
        text=chosen_lang['change_dir_button'])
    exit_button.config(text=chosen_lang['exit_button'])
    show_button.config(text=chosen_lang['show_button'])
    shortcuts_button.config(text=chosen_lang['shortcuts'])
    about_button.config(text=chosen_lang['about_button'])
    with open('src/settings.json', 'w') as f:
        json.dump(settings, f)

    result = tk.messagebox.askyesno(
        chosen_lang["language_switch_notice_title"], chosen_lang["language_switch_notice_text"])
    if result:
        window.destroy()


def on_enter(btn):
    if theme == "Automatic":
        if 6 <= current_hour < 18:
            btn.config(bg=DEFAULT_LM_HOVER_BUTTON_COLOR)
        else:
            btn.config(bg=DEFAULT_DM_HOVER_BUTTON_COLOR)
    if theme == "Dark":
        btn.config(bg=DEFAULT_DM_HOVER_BUTTON_COLOR)
    if theme == "Light":
        btn.config(bg=DEFAULT_LM_HOVER_BUTTON_COLOR)
    if theme == "Classic Dark":
        btn.config(bg=DEFAULT_CDM_HOVER_BUTTON_COLOR)
    if theme == "Classic Light":
        btn.config(bg=DEFAULT_CLM_HOVER_BUTTON_COLOR)

def on_exit():
    result = messagebox.askquestion(
        "Confirm", chosen_lang["confirm_exit"])
    if result == 'yes':
        window.destroy()




def on_leave(btn):
    if theme == "Automatic":
        if 6 <= current_hour < 18:
            btn.config(bg=DEFAULT_LM_BUTTONS_BG_COLOR)
        else:
            btn.config(bg=DEFAULT_DM_BUTTONS_BG_COLOR)
    if theme == "Dark":
        btn.config(bg=DEFAULT_DM_BUTTONS_BG_COLOR)
    if theme == "Light":
        btn.config(bg=DEFAULT_LM_BUTTONS_BG_COLOR)
    if theme == "Classic Dark":
        btn.config(bg=DEFAULT_CDM_BUTTONS_BG_COLOR)
    if theme == "Classic Light":
        btn.config(bg=DEFAULT_LM_BUTTONS_BG_COLOR)

def show_shortcuts():
    shortcuts_window = tk.Toplevel(window)
    shortcuts_window.withdraw()
    shortcuts_window.title("Shortcuts")
    shortcuts_window.wm_iconbitmap('assets/logos/logo-dark.ico')
    shortcuts_window_height = 750
    shortcuts_window_width = 600
    shortcuts_window.resizable(False, False)
    shortcuts_window.config(bg="#13005A")
    main_window_x = window.winfo_x()
    main_window_y = window.winfo_y() + 150
    main_window_width = window.winfo_width()
    main_window_height = window.winfo_height()
    x = main_window_x + main_window_width/2 - shortcuts_window_width/2
    y = main_window_y + main_window_height/2 - shortcuts_window_height/2
    shortcuts_window.geometry(
        f"{shortcuts_window_width}x{shortcuts_window_height}+{int(x)}+{int(y)}")
    shortcuts_window.deiconify()

    global shortcuts_top_label, shortcuts_label
    shortcuts_top_label = Label(
        shortcuts_window, text=chosen_lang["shortcuts"], bg="#13005A", fg="#85CDFD", font=("Arial", 25))
    shortcuts_top_label.place(x=220, y=30)
    shortcuts = chosen_lang['shortcuts_text']
    indentend_shortcuts = textwrap.indent(shortcuts, '    ')
    shortcuts_label = Label(shortcuts_window, text=indentend_shortcuts,
                            bg="#13005A", fg="#D1FFF3", font=("Arial", 16), pady=20)

    shortcuts_label.place(x=110, y=80)


def about():
    version_released = ''
    version_unreleased = ''
    if is_released != '':
        version_unreleased = messagebox.askokcancel(
            chosen_lang['about_title'], chosen_lang['about_unreleased'].format(version=version))
    else:
        version_released = messagebox.askokcancel(
            chosen_lang['about_title'], chosen_lang['about_released'].format(version=version))
    if version_released or version_unreleased:
        open_issues()


def open_github_page():
    open_github = messagebox.askokcancel(
        chosen_lang["open_github_confirmation_title"], chosen_lang["open_github_confirmation"])
    if open_github:
        link = "https://github.com/ziadh/Safe-Data/"
        webbrowser.open(link)


def focus_next_box(event):
    event.widget.tk_focusNext().focus()
    return "break"


def show_auto_help():
    auto_help = messagebox.showinfo(chosen_lang["automatic_help_title"],chosen_lang["automatic_help_message"])
    


window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coord = int((screen_width / 2) - (500 / 2))
y_coord = int((screen_height / 2) - (300))
window.resizable(True, True)
window.geometry(f"700x510+{x_coord}+{y_coord}")
with open('src/settings.json', 'r') as f:
    settings = json.load(f)

is_released = settings['is_released?']
version_message = Label(
    text="", fg="blue", cursor="hand2", bg="#2A3990")
version_message.bind("<Button-1>", download_update)
window_title = chosen_lang["window_title"].format(version=version)+is_released

version_message.place(x=40, y=-20)
whats_new_label = Label(text="", fg="blue", cursor="hand2", bg="#2A3990")
whats_new_label.bind(
    "<Button-1>", lambda event: open_patch_notes(language, chosen_lang))
whats_new_label.place(x=40, y=20)

window.title(window_title)
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)
window.wm_iconbitmap('assets/logos/logo-dark.ico')

canvas = Canvas(height=150, width=275)
logo_img = PhotoImage(file="assets/logos/wide_dark.png")
canvas.create_image(137, 75, image=logo_img, anchor="center")
canvas.place(x=200, y=5)

#### SHORTCUTS BELOW ####

window.bind("<Control-B>", lambda _: about_button.invoke())
window.bind("<Control-b>", lambda _: about_button.invoke())
window.bind("<Control-S>", lambda _: save_button.invoke())
window.bind("<Return>", lambda _: save_button.invoke())
window.bind("<Control-s>", lambda _: save_button.invoke())
window.bind("<Control-G>", lambda _: generate_password_button.invoke())
window.bind("<Control-g>", lambda _: generate_password_button.invoke())
window.bind("<Control-J>", lambda _: show_button.invoke())
window.bind("<Control-j>", lambda _: show_button.invoke())
window.bind("<Control-U>", lambda _: check_for_update_button.invoke())
window.bind("<Control-u>", lambda _: check_for_update_button.invoke())
window.bind("<Control-/>", lambda _: clear_all_button.invoke())
window.bind("<Control-`>", lambda _: shortcuts_button.invoke())
window.bind("<Control-E>", lambda _: password_check_button.invoke())
window.bind("<Control-e>", lambda _: password_check_button.invoke())
window.bind("<Control-P>", lambda _: privacy_button.invoke())
window.bind("<Control-p>", lambda _: privacy_button.invoke())
window.bind("<Control-D>", lambda _: change_dir_button.invoke())
window.bind("<Control-d>", lambda _: change_dir_button.invoke())
window.bind("<Control-.>", lambda _: saving_as_button.invoke())


#### SHORTCUTS ABOVE ####

global website_entry
data_type = settings['data_type']
github_logo = PhotoImage(file="assets\logos\GitHubLogo.png")
github_white = PhotoImage(file="assets\logos\gitHub_white.png")

### START OF LABELS ###

confirm_changed_dir = Label(text="", bg="#2A3990", font=("Verdana", 9))
confirm_changed_dir.place(x=40, y=390)

email_label = Label(
    text=chosen_lang['email_label'], bg="#2A3990", fg="white", font=("Verdana", 11))
email_label.place(x=40, y=210)

pass_check_label = Label(text="", bg="#2A3990")
pass_check_label.place(x=485, y=240)

password_label = Label(
    text=chosen_lang["password_label"], bg="#2A3990", fg="white", font=("Verdana", 11))
password_label.place(x=40, y=240)

password_saved = Label(
    text=chosen_lang["password_saved_label"], bg="light green", fg="blue", font=("Verdana", 9))

website_label = Label(
    text=chosen_lang['website_label'], bg="#2A3990", fg="white", font=("Verdana", 11))
website_label.place(x=40, y=180)

### END OF LABELS ###

### START OF BUTTONS ###

about_button = Button(text=chosen_lang["about_button"], width=17,
                      bg="#251749", fg="white", font=("Verdana", 8), command=about)
about_button.place(x=200, y=360)

change_dir_button = Button(
    text=chosen_lang["change_dir_button"], width=17, command=change_dir, bg="#251749", fg="white", font=("Verdana", 8))
change_dir_button.place(x=353, y=330)

check_for_update_button = Button(text=chosen_lang["check_for_updates_button"],
                                 bg="#251749", fg="white", command=version_checker, width=17, font=("Verdana", 8))
check_for_update_button.place(x=40, y=300)

clear_all_button = Button(text=chosen_lang["clear_all_button"], width=17,
                          command=clear_all, bg="#251749", fg="white", font=("Verdana", 8))
clear_all_button.place(x=40, y=360)

clear_input_button = Button(text=chosen_lang["clear_input_button"], width=17,
                            command=clear_input, bg="#251749", fg="white", font=("Verdana", 8))
clear_input_button.place(x=40, y=330)
exit_button = Button(text=chosen_lang["exit_button"], width=17,
                     command=on_exit, bg="#251749", fg="white", font=("Verdana", 8))
exit_button.place(x=353, y=360)

generate_password_button = Button(
    text=chosen_lang["generate_button"], command=randomize_password, bg="#251749", fg="white", width=12, font=("Verdana", 8))
generate_password_button.place(x=390, y=240)


password_check_button = Button(
    text=chosen_lang["check_pass_button"], bg="#251749", fg="white", command=check_pass, width=17, font=("Verdana", 8))
password_check_button.place(x=40, y=270)

privacy_button = Button(text=chosen_lang["privacy_button"], width=17,
                        command=safety, bg="#251749", fg="white", font=("Verdana", 8))
privacy_button.place(x=200, y=300)

save_button = Button(text=chosen_lang["save_button"], width=39,
                     command=save, bg="#251749", fg="white", font=("Verdana", 8))
save_button.place(x=200, y=270)

saving_as_button = Button(text=chosen_lang['saving_as_button'].format(
    data_type=data_type), width=17, command=change_data_type, bg="#251749", fg="white", font=("Verdana", 8))
saving_as_button.place(x=353, y=300)

shortcuts_button = Button(text=chosen_lang["shortcuts"], width=17,
                          command=show_shortcuts, bg="#251749", fg="white", font=("Verdana", 8))
shortcuts_button.place(x=200, y=330)

show_button = Button(
    text=chosen_lang['show_button'], command=show_or_hide, bg="#251749", fg="white", font=("Verdana", 8))
show_button.bind("<Control-b>", show_or_hide)
show_button.place(x=338, y=240)

theme_label = Label(text=chosen_lang["theme_label"],
                    bg=DEFAULT_DM_LABELS_BG_COLOR, fg="white", font=("Verdana", 8))
theme_label.place(x=353, y=430)
theme_dropdown = CTk.CTkOptionMenu(window, values=[
    chosen_lang["Dark_theme"], chosen_lang["Light_theme"], chosen_lang["Classic_Dark_theme"], chosen_lang["Classic_Light_theme"], chosen_lang["Automatic_Theme"]], width=80, command=change_theme)
theme_dropdown.place(x=410, y=430)
current_theme = get_current_theme()
theme_dropdown.set(current_theme)
language_label = Label(text=chosen_lang["language_label"],
                       bg=DEFAULT_DM_LABELS_BG_COLOR, fg="white", font=("Verdana", 8))
language_label.place(x=200, y=430)

language_dropdown = CTk.CTkOptionMenu(window, values=[
    "English", "Español"], width=80, command=toggle_language)
language_dropdown.place(x=270, y=430)
current_language = get_current_language()
language_dropdown.set(current_language)
github_page_button = Button(image=github_logo, compound='center',
                            bg="#2A3990", fg="white", command=open_github_page, width=30)
github_page_button.place(x=40, y=430)

automatic_help_button = Button(text='?', command=show_auto_help, width=5)

### END OF BUTTONS ###

### START OF ENTRYBOXES ###

website_entry = Entry(width=46)
website_entry.place(x=200, y=180)
website_entry.bind("<Tab>", focus_next_box)
website_entry.focus()
email_entry = Entry(width=46)
email_entry.place(x=200, y=210)
email_entry.insert(0, "")
email_entry.bind("<Tab>", focus_next_box)
is_password_visible = False
password_entry = Entry(show="*", width=21)
password_entry.place(x=200, y=240)
password_entry.bind("<Tab>", focus_next_box)


### END OF ENTRYBOXES ###

buttons = [automatic_help_button, clear_input_button, github_page_button, generate_password_button,  clear_all_button, save_button, password_check_button, about_button, saving_as_button, show_button,
           privacy_button,  change_dir_button, exit_button, check_for_update_button, shortcuts_button]

element_labels = [website_label, password_saved,
                  password_label, email_label, confirm_changed_dir, theme_label, language_label]

for btn in buttons:
    btn.bind("<Enter>", lambda e, btn=btn: on_enter(btn))
    btn.bind("<Leave>", lambda e, btn=btn: on_leave(btn))

if settings['theme'] == 'Light':
    Light_Mode()
if settings['theme'] == 'Dark':
    Dark_Mode()
if settings['theme'] == 'Classic Dark':
    Classic_Dark_Mode()
if settings['theme'] == 'Classic Light':
    Classic_Light_Mode()


if language == 'English':
    change_dir_button.config(width=17)
    check_for_update_button.config(width=17)
    email_label.config(font=("Verdana", 11))
if language == 'Español':
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
