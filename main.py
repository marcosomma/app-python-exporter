from Tkinter import *

import appCore as Core
import courseGenerator as CG
import topicGenerator as TG
import assessmentGenerator as AG
import helper as help

global p_counter
p_counter = 0

# INTERFACE
root = Tk()
rtitle = root.title("Coursify to Synergy")
root.minsize(410,350)
root.maxsize(410,350)
root.configure(background='#fcfcfc')
root.iconbitmap(default='data/img/icon.ico')

label = Label(root, text="Coursify to Synergy",  font="Helvetica 20 bold ", background='#0f3e62', foreground="#fcfcfc")
label.config( width = 100)
label.pack( side ='top')

img = PhotoImage(file=("data/img/background.gif"))
img_label = Label(root, background='#fcfcfc', image = img)
img_label.pack( side ='top', fill = "both", expand = "yes")

botton_lable = Label(root, background='#0f3e62')
botton_lable.config( width = 100)
botton_lable.pack( side ='top', fill='both',)

exit_btn = Button(botton_lable, text="Exit", font="Helvetica 10 bold", background='#fcfcfc', foreground="#0f3e62", cursor="hand2", command=Core.exit)
exit_btn.config( height = 1, width = 15)
exit_btn.pack(side=RIGHT, fill='both', expand=False, padx=35, pady=10)

open_btn = Button(botton_lable, text="Export", font="Helvetica 10 bold", background='#fcfcfc', foreground="#0f3e62", cursor="hand2", command=Core.open_file_system)
open_btn.config( height = 1, width = 15)
open_btn.pack(side=LEFT, fill='both', expand=False, padx=35, pady=10)

label_copyright = Label(root, font="Helvetica 8", text='Skillsoft R&D', foreground="#fcfcfc", background='#333',  width = 100, height = 1 )
label_copyright.pack(side ='bottom', pady=1)

label_response = Label(img_label, font="Helvetica 20 bold")

root.mainloop()