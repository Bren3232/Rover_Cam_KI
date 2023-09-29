
# Copyright (C) 2023 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam KI project.
# Please see the LICENSE file that should have been included as part of this package.


# Should put into count_img or other

# todo add a tracker bar or just bind keys to change show_time
# import sys
import cv2
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter import ttk
import os
import time
# import numpy as np
# import sys
# import cvtools_copy as cvt


# Options
from_dir = r""
mark = 'marked'                       # gets added to end of image name when "Mark Image" is invoked
show_time = 4                       # time to display each image
img_size = 1000                      # rescale image to this width

'''
Ctrl+m to Mark Image
space to toggle pause
right arrow to goto next image
left arrow to goto previous image
q to quit
'''


root = Tk()
root.geometry("300x700+5+5")   # the + part is w, h of upper left comp screen cord
root.title("Control Window")


def pause_btn(e):
    global pause_it, status_lab
    if pause_it == False:
        status_lab.pack_forget()
        status_lab = ttk.Label(frame1, text="Paused",
                               font=("Liberation Sans", 18), background=bgc, foreground="red", wraplength=670,
                               justify="left")
        status_lab.pack(side='left', padx=20, pady=50)
        
        pause_it = True
        
    else:
        status_lab.pack_forget()
        status_lab = ttk.Label(frame1, text="Running",
                               font=("Liberation Sans", 18), background=bgc, foreground=fgc, wraplength=670,
                               justify="left")
        status_lab.pack(side='left', padx=20, pady=50)
        
        pause_it = False

def quit_btn(e):
    global qu, idx, t
    sav_idx = idx
    ans = askyesno("Quit", "Are you sure?")
    if ans == True:
        qu = True
    else:
        idx = sav_idx
        t = time.time() + show_time

def mark_pic_btn(e):
    global img_list
    n, ex = img_list[current_idx + 1].split('.')
    os.rename(os.path.join(from_dir, img_list[current_idx + 1]), os.path.join(from_dir, f'{n}_{mark}.{ex}'))
    img_list = os.listdir(from_dir)
    img_list.sort(key=lambda f: int(f[:f.find('.')]))

def previous(e):
    global idx, force_load, t, show_time
    if idx - 2 >= -1:
        idx -= 2
        t = time.time() + show_time
        force_load = True

def nex_(e):
    global idx, force_load, t, show_time
    t = time.time() + show_time
    force_load = True

def inc_show_time(e):
    global show_time, main_lab
    show_time += 1
    main_lab.pack_forget()
    main_lab = ttk.Label(frame8, text=f"Display Time: {show_time}",
                         font=("Liberation Sans", 18), background=bgc, foreground=fgc, wraplength=670, justify="left")
    main_lab.pack(side='left', padx=20, pady=(20, 60))

def dec_show_time(e):
    global show_time, main_lab
    show_time -= 1
    main_lab.pack_forget()
    main_lab = ttk.Label(frame8, text=f"Display Time: {show_time}",
                         font=("Liberation Sans", 18), background=bgc, foreground=fgc, wraplength=670, justify="left")
    main_lab.pack(side='left', padx=20, pady=(20, 60))

root.bind("q", quit_btn)
root.bind("<Control-m>", mark_pic_btn)
root.bind("<space>", pause_btn)
root.bind("<Right>", nex_)
root.bind("<Left>", previous)

root.bind("<Up>", inc_show_time)
root.bind("<Down>", dec_show_time)

bgc = "#141E27"
fgc = "#EEEEEE"
btc = "#E0DDAA"
bgt = "#393E46"  # bg text

main_frame = Frame(root, bg=bgt)
main_frame.pack(fill=BOTH, expand=1)

frame1 = Frame(main_frame, bg=bgc)     # for main paragraph
frame1.pack(side=TOP, fill=BOTH)
frame2 = Frame(frame1, bg=bgc)
frame2.pack(side=BOTTOM, fill=BOTH)
frame3 = Frame(frame2, bg=bgc)
frame3.pack(side=BOTTOM, fill=BOTH)
frame4 = Frame(frame3, bg=bgc)
frame4.pack(side=BOTTOM, fill=BOTH)
frame5 = Frame(frame4, bg=bgc)
frame5.pack(side=BOTTOM, fill=BOTH)
frame6 = Frame(frame5, bg=bgc)
frame6.pack(side=BOTTOM, fill=BOTH)
frame7 = Frame(frame6, bg=bgc)
frame7.pack(side=BOTTOM, fill=BOTH)
frame8 = Frame(frame7, bg=bgc)
frame8.pack(side=BOTTOM, fill=BOTH)

status_lab = ttk.Label(frame1, text="Paused",
                 font=("Liberation Sans", 18), background=bgc, foreground="red", wraplength=670, justify="left")
status_lab.pack(side='left', padx=20, pady=(40, 20))
pau = Button(frame2, height=2,
                width=20,
                text="Pause/Run (space)",
                font=("Liberation Sans bold", 14),
                bg=btc,
                command=lambda: pause_btn(None))
pau.pack(side='left', padx=(20, 0), pady=(0, 10))
take_pic = Button(frame3, height=2,
                  width=20,
                  text="Mark Image",
                  font=("Liberation Sans bold", 14),
                  bg=btc,
                  command=lambda: mark_pic_btn(None))
take_pic.pack(side='left', padx=(20, 0), pady=10)
prev = Button(frame4, height=2,
                width=20,
                text="Previous",
                font=("Liberation Sans bold", 14),
                bg=btc,
                command=lambda: previous(None))
prev.pack(side='left', padx=(20, 0), pady=10)
nex = Button(frame5, height=2,
                width=20,
                text="Next",
                font=("Liberation Sans bold", 14),
                bg=btc,
                command=lambda: nex_(None))
nex.pack(side='left', padx=(20, 0), pady=10)
qui = Button(frame6, height=2,
                width=20,
                text="Quit(q)",
                font=("Liberation Sans bold", 14),
                bg=btc,
                command=lambda: quit_btn(None))
qui.pack(side='left', padx=(20, 0), pady=10)
inc_st = Button(frame7, height=2,
                width=6,
                text="+",
                font=("Liberation Sans bold", 14),
                bg=btc,
                command=lambda: inc_show_time(None))
inc_st.pack(side='left', padx=(40, 0), pady=10)
dec_st = Button(frame7, height=2,
                width=6,
                text="-",
                font=("Liberation Sans bold", 14),
                bg=btc,
                command=lambda: dec_show_time(None))
dec_st.pack(side='left', padx=(50, 0), pady=(10, 0))
main_lab = ttk.Label(frame8, text=f"Display Time: {show_time}",
                 font=("Liberation Sans", 18), background=bgc, foreground=fgc, wraplength=670, justify="left")
main_lab.pack(side='left', padx=20, pady=(20, 60))
# ---------------

img_list = os.listdir(from_dir)
# img_list.sort(key=lambda f: int(re.sub('\D', '', f)))    # only works if there's just 1 num in name

img_list.sort(key=lambda f: int(f[:f.find('.')]))

# img_list.sort(key=lambda f: int(f[f.find('_', f.find('model_')) + 1:f.find('_', f.find('model_') + len('model_'))]))
print(img_list)


pause_start = 0
idx = -1
current_idx = 0
load = True
force_load = False
ep = True
sp = False
qu = False
pause_it = False
t = time.time()

while True:

    if cv2.waitKey(1) & 0xFF == ord("q") or qu == True :
        break

    if time.time() > t and load == True or force_load:
        current_idx = idx
        idx += 1
        if idx + 1 > len(img_list):
            break

        img = cv2.imread(os.path.join(from_dir, img_list[idx]))
        
        w = img.shape[1]
        h = img.shape[0]

        img = cv2.resize(img, (img_size, 820))  # h has to be determined outside of look if math
#         img = cvt.resize(img, img_size)

        cv2.putText(img, f'{img_list[idx]}', (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, [0, 200, 180])

        if force_load == False:
            t += show_time
        force_load = False

        cv2.imshow("img", img)

    if pause_it == True:
        if sp == False:
            pause_start = time.time()
            sp = True
            load = False
            ep = False

#         status_lab.pack_forget()
#         status_lab = ttk.Label(frame1, text="Paused",
#                                font=("Liberation Sans", 18), background=bgc, foreground="red", wraplength=670,
#                                justify="left")
#         status_lab.pack(side='left', padx=20, pady=50)

    if pause_it == False or qu == True:
        if ep == False:
            t = time.time() + show_time
            load = True
            sp = False
            ep = True

#         status_lab.pack_forget()
#         status_lab = ttk.Label(frame1, text="Running",
#                                font=("Liberation Sans", 18), background=bgc, foreground=fgc, wraplength=670,
#                                justify="left")
#         status_lab.pack(side='left', padx=20, pady=50)

    root.update()

cv2.destroyAllWindows()
root.destroy()
