
from tkinter import *

root = Tk()

# Load the image
img = PhotoImage(
    file="assets\logos\GitHubLogo.png")

# Create the button
button = Button(root, text="Click me", image=img, compound="center")

# Pack the button onto the window
button.pack()

root.mainloop()
