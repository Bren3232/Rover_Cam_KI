
# Copyright (C) 2023 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam KI project.
# Please see the LICENSE file that should have been included as part of this package.


from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno
from subprocess import run, check_output, CalledProcessError
import time
import os
import cv2
import numpy as np
from PIL import ImageTk, Image


root = Tk()
root.geometry("880x850")
root.title("Rover Cam KI")

loaded = False

# if loaded == True:
sett = {}
a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
a6 = []
a7 = []
a8 = []
save_it = False
scr2_entered = False
scr3_entered = False


def get_crontab():
    try:
        crontab = check_output(['crontab', '-l']).decode('utf-8')
        return crontab
    except CalledProcessError:
        return ""

def set_crontab(crontab):
    with open('temp_cron', 'w') as f:
        f.write(crontab)
    run(['crontab', 'temp_cron'])
    run(['rm', 'temp_cron'])


def popup_alert_vid():
    showinfo("Error", "Video Stream failed, try another camera index")   # makes an alert "ding" noise, in windows at least


# Subtract len of file name and / to get containing directory
rc_dir = os.path.abspath(__file__)
rc_dir = rc_dir[:-len(os.path.basename(__file__)) - 1]  


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized

def load_all():
    global sett
    global a1
    global a2
    global a3
    global a4
    global a5
    global a6
    global a7
    global a8
    global aoi_img
    global compiled_overlay
    global plimg_h
    global p_list_save
    global p_list
    global ao_im
    global boot_on
    global play_audio, draw_aoi

    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []


    pr = open(rc_dir + "/support/RC_config.txt", "r")
    prog = pr.read().splitlines()
    pr.close()

    for i in prog:

        if i != "" and i[0:10] == "set_time =":
            st = i[10:].split()
            sett["yr"] = st[0]   # retrieved
            sett["mo"] = st[1]
            sett["da"] = st[2]
            sett["hr"] = st[3]
            sett["mi"] = st[4]
            sett["se"] = st[5]

        elif i != "" and i[0:20] == "run_at_system_boot =":
            if "Y" in i[20:]:
                sett["run_at_system_boot"] = "Y"
                boot_on = False
                boot_tog.config(image=tog_on)
            else:
                sett["run_at_system_boot"] = "N"
                boot_on = True
                boot_tog.config(image=tog_off)
        elif i != "" and i[0:11] == "clip_time =":
            sett["clip_time"] = i[11:].strip()
        elif i != "" and i[0:15] == "use_pi_camera =":
            if "Y" in i[15:]:
                sett["use_pi_camera"] = "Y"
                picam_on = False
                picam_tog.config(image=tog_on)
            else:
                sett["use_pi_camera"] = "N"
                picam_on = True
                picam_tog.config(image=tog_off)
        elif i != "" and i.startswith("resolution ="):
            sett["reso"] = i.split('=')[1].strip()    
        elif i != "" and i[0:5] == "fps =":
            sett["fps"] = i[5:].strip()
        elif i != "" and i[0:13] == "motion_area =":
            sett["motion_area"] = i[13:].strip()
        elif i != "" and i[0:13] == "motion_sens =":
            sett["motion_sens"] = i[13:].strip()
        elif i != "" and i[0:6] == "mode =":
            sett["mode"] = i[6:].strip()
        elif i != "" and i[0:12] == "play_audio =":
            if "Y" in i[12:]:
                sett["play_audio"] = "Y"
                play_audio = False
                audio_tog.config(image=tog_on)
            else:
                sett["play_audio"] = "N"
                play_audio = True
                audio_tog.config(image=tog_off)
        elif i != "" and i[0:13] == "delay_audio =":
            sett["delay_audio"] = i[13:].strip()

        # New for keypad version
        elif i != "" and i.startswith('pin ='):
            sett['pin'] = i.split('=')[1].strip()
        elif i != "" and i.startswith('allowable_pin_attempts ='):
            sett['allowable_pin_attempts'] = i.split('=')[1].strip()
        elif i != "" and i.startswith("failed_pin_lock_time ="):
            sett['failed_pin_lock'] = i.split('=')[1].strip()
        elif i != "" and i[0:13] == "start_delay =":
            sett["start_delay"] = i[13:].strip()
        elif i != "" and i[0:14] == "camera_index =":
            sett["camera_index"] = i[14:].strip()
        elif i != "" and i.startswith("exposure_mode ="):
            sett["picam_expo"] = i.split('=')[1].strip()
        elif i != "" and i.startswith("sensor_mode ="):
            sett["picam_sens"] = i.split('=')[1].strip()
        elif i != "" and i.startswith("awb_mode ="):
            sett["picam_awb"] = i.split('=')[1].strip()
        elif i != "" and i.startswith("brightness ="):
            sett["picam_brt"] = i.split('=')[1].strip()
        elif i != "" and i.startswith("contrast ="):
            sett["picam_con"] = i.split('=')[1].strip()
        elif i != "" and i.startswith("iso ="):
            sett["picam_iso"] = i.split('=')[1].strip()
        elif i != "" and i.startswith("shutter_speed ="):
            sett["picam_shut"] = i.split('=')[1].strip()
        elif i != "" and i[0:2] == "a1":
            a1.append(i[2:].strip())
        elif i != "" and i[0:2] == "a2":
            a2.append(i[2:].strip())
        elif i != "" and i[0:2] == "a3":
            a3.append(i[2:].strip())
        elif i != "" and i[0:2] == "a4":
            a4.append(i[2:].strip())
        elif i != "" and i[0:2] == "a5":
            a5.append(i[2:].strip())
        elif i != "" and i[0:2] == "a6":
            a6.append(i[2:].strip())
        elif i != "" and i[0:2] == "a7":
            a7.append(i[2:].strip())
        elif i != "" and i[0:2] == "a8":
            a8.append(i[2:].strip())
        elif i != "" and i.startswith("draw_aoi ="):
            if "Y" in i.split("=")[1]:
                sett["draw_aoi"] = "Y"
                draw_aoi = False
                draw_tog.config(image=tog_on)
            else:
                sett["draw_aoi"] = "N"
                draw_aoi = True
                draw_tog.config(image=tog_off)


    p = open(rc_dir + "/support/aoi_pts.txt", "r")
    p.readline()
    pts = p.read().split()
    p.close()

    plimg_h = 240
    p_list = []

    if len(pts) != 0:
        pts = list(map(float, pts))
        for idx, i in enumerate(pts):
            if idx % 4 == 0:
                p_list.append([int(pts[idx] * 480), int(pts[idx + 1] * 480), int(pts[idx + 2] * 640), int(pts[idx + 3] * 640)])

        compiled_overlay = np.zeros(shape=(480, 640, 3))
        compiled_overlay = compiled_overlay + 20
        compiled_overlay = np.uint8(compiled_overlay)
        for i in p_list:
            compiled_overlay[i[0]:i[1], i[2]:i[3]] = [1, 170, 1]
        compiled_overlay = resize(compiled_overlay, height=plimg_h)

        ao_im = ImageTk.PhotoImage(Image.fromarray(compiled_overlay))
    else:
        ao_im = ImageTk.PhotoImage(Image.open(rc_dir + "/support/aoi_sml.png"))

        compiled_overlay = np.zeros(shape=(480, 640, 3))
        compiled_overlay = np.uint8(compiled_overlay)

    aoi_img.config(image=ao_im)
    aoi_img.image = ao_im


def load_btn():
    global sett
    global a1
    global a2
    global a3
    global a4
    global a5
    global a6
    global a7
    global a8


    load_all()                      # in case of save then load
    s1_txt.delete("1.0", END)
    reso_txt.delete("1.0", END)
    fps_txt.delete("1.0", END)
    s2_txt.delete("1.0", END)
    s3_txt.delete("1.0", END)
    s4_txt.delete("1.0", END)
    s6_txt.delete("1.0", END)
    s8_txt.delete("1.0", END)
    s9_txt.delete("1.0", END)
    s10_txt.delete("1.0", END)
    s11_txt.delete("1.0", END)
    s12_txt.delete("1.0", END)
    
    
    picam_expo_txt.delete("1.0", END)
    picam_sens_txt.delete("1.0", END)
    picam_awb_txt.delete("1.0", END)
    picam_brt_txt.delete("1.0", END)
    picam_con_txt.delete("1.0", END)
    picam_iso_txt.delete("1.0", END)
    picam_shut_txt.delete("1.0", END)

    st_txtyr.delete("1.0", END)
    st_txtmo.delete("1.0", END)
    st_txtda.delete("1.0", END)
    st_txthr.delete("1.0", END)
    st_txtmi.delete("1.0", END)
    st_txtse.delete("1.0", END)

    a_txt1.delete("1.0", END)
    a_txt2.delete("1.0", END)
    a_txt3.delete("1.0", END)
    a_txt4.delete("1.0", END)
    a_txt5.delete("1.0", END)
    a_txt6.delete("1.0", END)
    a_txt7.delete("1.0", END)
    a_txt8.delete("1.0", END)
    s1_txt.insert(END, sett["clip_time"])
    reso_txt.insert(END, sett["reso"])
    fps_txt.insert(END, sett["fps"])
    s2_txt.insert(END, sett["motion_area"])
    s3_txt.insert(END, sett["motion_sens"])
    s4_txt.insert(END, sett["mode"])
    s6_txt.insert(END, sett["delay_audio"])

    # For new keypad version
    s8_txt.insert(END, sett['pin'])
    s9_txt.insert(END, sett['allowable_pin_attempts'])
    s10_txt.insert(END, sett['failed_pin_lock'])
    s11_txt.insert(END, sett["start_delay"])
    s12_txt.insert(END, sett["camera_index"])
    picam_expo_txt.insert(END, sett["picam_expo"])
    picam_sens_txt.insert(END, sett["picam_sens"])
    picam_awb_txt.insert(END, sett["picam_awb"])
    picam_brt_txt.insert(END, sett["picam_brt"])
    picam_con_txt.insert(END, sett["picam_con"])
    picam_iso_txt.insert(END, sett["picam_iso"])
    picam_shut_txt.insert(END, sett["picam_shut"])

    st_txtyr.insert(END, sett["yr"])
    st_txtmo.insert(END, sett["mo"])
    st_txtda.insert(END, sett["da"])
    st_txthr.insert(END, sett["hr"])
    st_txtmi.insert(END, sett["mi"])
    st_txtse.insert(END, sett["se"])

    for i in a1:
        a_txt1.insert(END, i  + "\n")
    for i in a2:
        a_txt2.insert(END, i  + "\n")
    for i in a3:
        a_txt3.insert(END, i  + "\n")
    for i in a4:
        a_txt4.insert(END, i  + "\n")
    for i in a5:
        a_txt5.insert(END, i  + "\n")
    for i in a6:
        a_txt6.insert(END, i  + "\n")
    for i in a7:
        a_txt7.insert(END, i  + "\n")
    for i in a8:
        a_txt8.insert(END, i  + "\n")
        
    # do crontab check here
    if sett["run_at_system_boot"] == "Y":
        path_to_check = rc_dir + "/Run-at-startup/*.py" 
        cron_line_to_add = f"@reboot sleep 40 && python3 {path_to_check} &"
        current_crontab = get_crontab()

        if path_to_check in current_crontab:
            return
        else:
            ask = askyesno("Permission Required", 'Your device is not set-up to run Rover Cam at system boot, ' +
                           'for this user, and storage device. Would you like Rover Cam to set it up for you?')
            if ask == True:
                updated_crontab = current_crontab + "\n" + cron_line_to_add + "\n"
                set_crontab(updated_crontab)


def save_btn():
    global p_list
    global sett
    
    sett["clip_time"] = s1_txt.get("1.0", "end-1c")
    sett["reso"] = reso_txt.get("1.0", "end-1c")
    sett["fps"] = fps_txt.get("1.0", "end-1c")
    sett["motion_area"] = s2_txt.get("1.0", "end-1c")
    sett["motion_sens"] = s3_txt.get("1.0", "end-1c")
    sett["mode"] = s4_txt.get("1.0", "end-1c")
    sett["delay_audio"] = s6_txt.get("1.0", "end-1c")
    sett["pin"] = s8_txt.get("1.0", "end-1c")
    sett["allowable_pin_attempts"] = s9_txt.get("1.0", "end-1c")
    sett["failed_pin_lock"] = s10_txt.get("1.0", "end-1c")
    sett["start_delay"] = s11_txt.get("1.0", "end-1c")
    sett["camera_index"] = s12_txt.get("1.0", "end-1c")
    
    sett["picam_expo"] = picam_expo_txt.get("1.0", "end-1c")
    sett["picam_sens"] = picam_sens_txt.get("1.0", "end-1c")
    sett["picam_awb"] = picam_awb_txt.get("1.0", "end-1c")
    sett["picam_brt"] = picam_brt_txt.get("1.0", "end-1c")
    sett["picam_con"] = picam_con_txt.get("1.0", "end-1c")
    sett["picam_iso"] = picam_iso_txt.get("1.0", "end-1c")
    sett["picam_shut"] = picam_shut_txt.get("1.0", "end-1c")

    sett["yr"] = st_txtyr.get("1.0", "end-1c")
    sett["mo"] = st_txtmo.get("1.0", "end-1c")
    sett["da"] = st_txtda.get("1.0", "end-1c")
    sett["hr"] = st_txthr.get("1.0", "end-1c")
    sett["mi"] = st_txtmi.get("1.0", "end-1c")
    sett["se"] = st_txtse.get("1.0", "end-1c")
    
    if sett["clip_time"] == "":
        sett["clip_time"] = "0"
    if sett["reso"] == "":
        sett["reso"] = "640x480"
    if sett["fps"] == "":
        sett["fps"] = "1"
    if sett["motion_area"] == "":
        sett["motion_area"] = "20"
    if sett["motion_sens"] == "":
        sett["motion_sens"] = "4"
    if sett["mode"] == "":
        sett["mode"] = "1"
    if sett["delay_audio"] == "":
        sett["delay_audio"] = "0"
    if sett["pin"] == "":
        sett["pin"] = "0"
    if sett["allowable_pin_attempts"] == "":
        sett["allowable_pin_attempts"] = "1"
    if sett["failed_pin_lock"] == "":
        sett["failed_pin_lock"] = "0"
    if sett["start_delay"] == "":
        sett["start_delay"] = "0"
    if sett["camera_index"] == "":
        sett["camera_index"] = "-1"
    if sett["picam_expo"] == "":
        sett["picam_expo"] = "default"
    if sett["picam_sens"] == "":
        sett["picam_sens"] = "default"
    if sett["picam_awb"] == "":
        sett["picam_awb"] = "default"
    if sett["picam_brt"] == "":
        sett["picam_brt"] = "default"
    if sett["picam_con"] == "":
        sett["picam_con"] = "default"
    if sett["picam_iso"] == "":
        sett["picam_iso"] = "default"
    if sett["picam_shut"] == "":
        sett["picam_shut"] = "default"
    if sett["yr"] == "":
        sett["yr"] = "0000"
    if sett["mo"] == "":
        sett["mo"] = "00"
    if sett["da"] == "":
        sett["da"] = "00"
    if sett["hr"] == "":
        sett["hr"] = "00"
    if sett["mi"] == "":
        sett["mi"] = "00"
    if sett["se"] == "":
        sett["se"] = "00"

    a1_str = a_txt1.get("1.0", "end-1c")
    a1 = a1_str.splitlines()

    a2_str = a_txt2.get("1.0", "end-1c")
    a2 = a2_str.splitlines()

    a3_str = a_txt3.get("1.0", "end-1c")
    a3 = a3_str.splitlines()

    a4_str = a_txt4.get("1.0", "end-1c")
    a4 = a4_str.splitlines()

    a5_str = a_txt5.get("1.0", "end-1c")
    a5 = a5_str.splitlines()

    a6_str = a_txt6.get("1.0", "end-1c")
    a6 = a6_str.splitlines()

    a7_str = a_txt7.get("1.0", "end-1c")
    a7 = a7_str.splitlines()

    a8_str = a_txt8.get("1.0", "end-1c")
    a8 = a8_str.splitlines()


    f = open(rc_dir + "/support/RC_config.txt", "r")
    fl = f.read().splitlines()
    f.close()

    a1_once = True

    for idx, i in enumerate(fl):
        # get 1st idx of fl that is "a1"
        if i[:8] == "Actions:" and a1_once == True:
            a1_fl_idx = idx
            a1_once = False

        if i != "" and i[0:10] == "set_time =":
            fl[idx] = f'set_time = {sett["yr"]} {sett["mo"]} {sett["da"]} {sett["hr"]} {sett["mi"]} {sett["se"]}'
        elif i != "" and i[0:20] == "run_at_system_boot =":
            fl[idx] = "run_at_system_boot = " + sett["run_at_system_boot"].strip()
            f_check = run(["ls", rc_dir + "/Run-at-startup"], capture_output=True).stdout
            f_check = f_check.decode("utf-8").splitlines()
            if sett["run_at_system_boot"] == "Y":
                run(["cp", rc_dir + "/support/start-up.py", rc_dir + "/Run-at-startup"])
            else:
                for i in f_check:
                    if "start" in i:
                        run(["rm", rc_dir + "/Run-at-startup/start-up.py"])
        elif i != "" and i[0:11] == "clip_time =":
            fl[idx] = "clip_time = " + sett["clip_time"].strip()
        elif i != "" and i[0:15] == "use_pi_camera =":
            fl[idx] = "use_pi_camera = " + sett["use_pi_camera"].strip()               
        elif i != "" and i.startswith("resolution ="):
            fl[idx] = "resolution = " + sett["reso"].strip()
        elif i != "" and i[0:5] == "fps =":
            fl[idx] = "fps = " + sett["fps"].strip()
        elif i != "" and i[0:13] == "motion_area =":
            fl[idx] = "motion_area = " + sett["motion_area"].strip()
        elif i != "" and i[0:13] == "motion_sens =":
            fl[idx] = "motion_sens = " + sett["motion_sens"].strip()
        elif i != "" and i[0:6] == "mode =":
            fl[idx] = "mode = " + sett["mode"].strip()
        elif i != "" and i[0:12] == "play_audio =":
            fl[idx] = "play_audio = " + sett["play_audio"].strip()
        elif i != "" and i[0:13] == "delay_audio =":
            fl[idx] = "delay_audio = " + sett["delay_audio"].strip()
        elif i != "" and i.startswith('pin ='):
            fl[idx] = f'pin = {sett["pin"].strip()}'
        elif i != "" and i.startswith('allowable_pin_attempts ='):
            fl[idx] = f'allowable_pin_attempts = {sett["allowable_pin_attempts"].strip()}'
        elif i != "" and i.startswith("failed_pin_lock_time ="):
            fl[idx] = f'failed_pin_lock_time = {sett["failed_pin_lock"].strip()}'
        elif i != "" and i[0:13] == "start_delay =":
            fl[idx] = "start_delay = " + sett["start_delay"].strip()
        elif i != "" and i[0:14] == "camera_index =":
            fl[idx] = "camera_index = " + sett["camera_index"].strip()
        elif i != "" and i.startswith('exposure_mode ='):
            fl[idx] = f'exposure_mode = {sett["picam_expo"].strip()}'
        elif i != "" and i.startswith('sensor_mode ='):
            fl[idx] = f'sensor_mode = {sett["picam_sens"].strip()}'
        elif i != "" and i.startswith('awb_mode ='):
            fl[idx] = f'awb_mode = {sett["picam_awb"].strip()}'
        elif i != "" and i.startswith('brightness ='):
            fl[idx] = f'brightness = {sett["picam_brt"].strip()}'
        elif i != "" and i.startswith('contrast ='):
            fl[idx] = f'contrast = {sett["picam_con"].strip()}'
        elif i != "" and i.startswith('iso ='):
            fl[idx] = f'iso = {sett["picam_iso"].strip()}'
        elif i != "" and i.startswith('shutter_speed ='):
            fl[idx] = f'shutter_speed = {sett["picam_shut"].strip()}'
        elif i != "" and i.startswith('draw_aoi ='):
            fl[idx] = f'draw_aoi = {sett["draw_aoi"].strip()}'

    fl = fl[:a1_fl_idx + 1]
    fl.append("")

    if len(a1) > 0:
        for i in a1:
            fl.append("a1 " + i)
    fl.append("")

    if len(a2) > 0:
        for i in a2:
            fl.append("a2 " + i)
    fl.append("")

    if len(a3) > 0:
        for i in a3:
            fl.append("a3 " + i)
    fl.append("")

    if len(a4) > 0:
        for i in a4:
            fl.append("a4 " + i)
    fl.append("")

    if len(a5) > 0:
        for i in a5:
            fl.append("a5 " + i)
    fl.append("")

    if len(a6) > 0:
        for i in a6:
            fl.append("a6 " + i)
    fl.append("")

    if len(a7) > 0:
        for i in a7:
            fl.append("a7 " + i)
    fl.append("")

    if len(a8) > 0:
        for i in a8:
            fl.append("a8 " + i)

    f2 = open(rc_dir + "/support/RC_config.txt", "w")
    f2.truncate(0)
    f2.seek(0)      # stops from writting with NULs
    for i in fl:
        f2.write(str(i) + "\n")
    f2.close()

    p = open(rc_dir + "/support/aoi_pts.txt", "w")
    p.write("Aoi boxes will stretch or compress if resolutions different from 4:3 used. Format here is: start_y end_y start_x end_x, as fraction of max\n")
    for i in p_list:
        # p_list at writing is:  [[410, 476, 4, 637], [8, 219, 6, 301]]
        # So that it works on resolutions as long as they are 4:3
        i = [i[0] / 480, i[1] / 480, i[2] / 640, i[3] / 640]
        
        for j in i:
            p.write(str(j) + " ")
    p.close()


# Start of my selectAOI, maybe add to cvtools     --------------------
p1x = 0
p1y = 0
p2x = 0
p2y = 0
p_list = []
down = False
start_aoi = False
end_aoi = False
brk_loop = False

# To always save an aoi.png, if this not changed then aoi is not used, sum would be 235008000.0
# ...can use sum an aoi'd img could only have slightest possibility of matching if cam img is taller
# final_aoi = np.ones((480, 640, 3), dtype=np.uint8) * 255
final_aoi = np.zeros((11, 2, 3), dtype=np.uint8)

def select_aoi():
    # import cv2
    global end_aoi
    global compiled_overlay
    global final_aoi
    global img2
    global p_list
    global plimg_h
    global brk_loop

    cap = cv2.VideoCapture(int(sett["camera_index"]))

    if not cap.isOpened():  # works and pauses code until window is closed
        brk_loop = True
        popup_alert_vid()

    def click_event(event, x, y, flags, param):
        global p1x
        global p1y
        global p2x
        global p2y
        global p_list
        global down
        global start_aoi  # just for play
        global end_aoi
        global brk_loop


        if event == cv2.EVENT_RBUTTONDOWN:
            brk_loop = True

        if event == cv2.EVENT_LBUTTONDOWN:
            start_aoi = True
            down = True

            p1x = x
            p1y = y
            p2x = x
            p2y = y

        if event == cv2.EVENT_MOUSEMOVE and down == True:  # Is current mouse location

            if x < 0:  # Stop from going negative
                x = 0
            if y < 0:  # minus border / plus border - cv2.copyMakeBorder  not using
                y = 0

            if x > img.shape[1]:  # Stop from going over img size
                x = img.shape[1]
            if y > img.shape[0]:
                y = img.shape[0]
            p2x = x
            p2y = y

        if event == cv2.EVENT_LBUTTONUP:  # param prints None, flags 0
            down = False
            end_aoi = True

    alpha = 0.4

    try:
        compiled_overlay = resize(compiled_overlay, height=480)
    except:
        pass
    while cap.isOpened():
        time.sleep(0.02)
        ret, img = cap.read()

        if ret == True:
            img = resize(img, 640)     # will have to save this or do calculations if having different res options
                                                # would resize the mask to frame size, easiest way
            overlay = img.copy()
            try:
                overlay = cv2.addWeighted(overlay, alpha, compiled_overlay, 1 - alpha, 0)
            except:
                pass

            if down == True or end_aoi == True:
                cv2.rectangle(overlay, (p1x, p1y), (p2x, p2y), (0, 255, 0), -1)  # save overlay to add to final, or use cords
                img2 = img.copy()
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            else:
                img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            cv2.imshow('Select AOI - Right Click To Cancel', img)
            cv2.setMouseCallback('Select AOI - Right Click To Cancel', click_event)  # does not stop code, has to be after imshow

            if end_aoi == True:
                end_aoi = False
                break
            if brk_loop == True:
                break
            cv2.waitKey(1)

        else:
            break

    if brk_loop == False:

        # My AOI    --------------------------
        pminy = min(p1y, p2y)
        pmaxy = max(p1y, p2y)
        pminx = min(p1x, p2x)
        pmaxx = max(p1x, p2x)

        p_list.append([pminy, pmaxy, pminx, pmaxx])

        compiled_overlay = np.zeros_like(img)
        for i in p_list:
            compiled_overlay[i[0]:i[1], i[2]:i[3]] = [1, 254, 1]

        final_aoi = compiled_overlay.copy()
        final_aoi[final_aoi == 0] = 255
        final_aoi[final_aoi != 255] = 0

        img2 = cv2.addWeighted(compiled_overlay, alpha, img2, 1 - alpha, 0)

        img2 = resize(img2, height=plimg_h)         # does stop added white space, but resizes

        aoiImg = ImageTk.PhotoImage(Image.fromarray(img2))
        aoi_img.configure(image=aoiImg)
        aoi_img.image = aoiImg


    # ----------------------------

    brk_loop = False

    cap.release()
    cv2.destroyAllWindows()

def clear_aoi():
    global aoi_img
    global p_list
    global img2
    global final_aoi
    global compiled_overlay
    global p_list_save
    aoiImg = ImageTk.PhotoImage(Image.open(rc_dir + "/support/aoi_sml.png"))
    aoi_img.configure(image=aoiImg)
    aoi_img.image = aoiImg
    p_list_save = p_list
    img2 = []
    final_aoi = []
    compiled_overlay = []
    p_list = []
    final_aoi = np.zeros((11, 2, 3), dtype=np.uint8)

def popup_about():
    pop = Toplevel()
    pop.geometry("600x600")
    pop.wm_title("About")
    frame1 = Frame(pop, bg=bgc)
    frame1.pack(fill=BOTH, expand=1)

    about_lab1 = ttk.Label(frame1, text="About",
                   font=("Liberation Sans", 26), background=bgc, foreground=fgc)
    about_lab1.pack(side=TOP, pady=40)

    about_lab2 = ttk.Label(frame1, text='Rover Cam KI 0.1.0\n\n'
                           'Copyright (C) 2023 Brendan Murphy - All Rights Reserved'
                        '\nThis file is part of the Rover Cam project.\n\nSee Rover_Cam_KI_Manual.pdf',
                           font=("Liberation Sans", 12), wraplength=500, background=bgc, foreground=fgc)

    about_lab2.pack()

    about_btn = Button(frame1, height=1,
                width=10,
                text="Close",
                font=("Liberation Sans", 12),
                bg=btc, command=pop.destroy)
    about_btn.pack(side=BOTTOM, pady=(0, 40))

# ------------------------------

# Create A Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame, highlightthickness=0)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


# Make scrollable with mouse wheel
def scroll_up(event):
#     my_canvas.yview_scroll(-1*(event.delta//120), "units")   # for windows, //higher num make small scroll steps.. messes up
    my_canvas.yview_scroll(-1, "units")

def scroll_down(event):
    my_canvas.yview_scroll(1, "units")

my_canvas.bind_all("<Button-4>", scroll_up)
my_canvas.bind_all("<Button-5>", scroll_down)  # Button-5 and 4 for linux scroll


# -------- Menu Bar ---------

menubar = Menu(root)
# menubar.configure(bg="red")
filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=donothing)
# filemenu.add_command(label="Open", command=select_file)
filemenu.add_command(label="Load", command=load_btn)
filemenu.add_command(label="Save", command=save_btn)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About", command=popup_about)
menubar.add_cascade(label="About", menu=helpmenu)

root.config(menu=menubar)

bgc = "#141E27"
btc = "#E0DDAA"
bgt = "#393E46"  # bg text
fgc = "#EEEEEE"


# Create ANOTHER Frame INSIDE the Canvas
second_frame = Frame(my_canvas, bg=bgc)
below1 = Frame(second_frame, bg=bgc)
below1.pack(side=BOTTOM, fill=BOTH)
below1b = Frame(below1, bg=bgc)
below1b.pack(side=BOTTOM, fill=BOTH)
below1c = Frame(below1b, bg=bgc)
below1c.pack(side=BOTTOM, fill=BOTH)
below1d = Frame(below1c, bg=bgc)
below1d.pack(side=BOTTOM, fill=BOTH)
below1e = Frame(below1d, bg=bgc)
below1e.pack(side=BOTTOM, fill=BOTH)
below1f = Frame(below1e, bg=bgc)
below1f.pack(side=BOTTOM, fill=BOTH)
below2 = Frame(below1f, bg=bgc)
below2.pack(side=BOTTOM, fill=BOTH)
below3 = Frame(below2, bg=bgc)
below3.pack(side=BOTTOM, fill=BOTH)

# picam
below3b = Frame(below3, bg=bgc)
below3b.pack(side=BOTTOM, fill=BOTH)
below3c = Frame(below3b, bg=bgc)
below3c.pack(side=BOTTOM, fill=BOTH)

# reso_
below3ca = Frame(below3c, bg=bgc)
below3ca.pack(side=BOTTOM, fill=BOTH)
below3cb = Frame(below3ca, bg=bgc)
below3cb.pack(side=BOTTOM, fill=BOTH)

below3d = Frame(below3cb, bg=bgc)
below3d.pack(side=BOTTOM, fill=BOTH)
below3e = Frame(below3d, bg=bgc)
below3e.pack(side=BOTTOM, fill=BOTH)
below4 = Frame(below3e, bg=bgc)
below4.pack(side=BOTTOM, fill=BOTH)
below5 = Frame(below4, bg=bgc)
below5.pack(side=BOTTOM, fill=BOTH)
below6 = Frame(below5, bg=bgc)
below6.pack(side=BOTTOM, fill=BOTH)
below7 = Frame(below6, bg=bgc)
below7.pack(side=BOTTOM, fill=BOTH)
below8 = Frame(below7, bg=bgc)
below8.pack(side=BOTTOM, fill=BOTH)
below9 = Frame(below8, bg=bgc)
below9.pack(side=BOTTOM, fill=BOTH)
below10 = Frame(below9, bg=bgc)
below10.pack(side=BOTTOM, fill=BOTH)
below11 = Frame(below10, bg=bgc)
below11.pack(side=BOTTOM, fill=BOTH)
below12 = Frame(below11, bg=bgc)
below12.pack(side=BOTTOM, fill=BOTH)
below13 = Frame(below12, bg=bgc)
below13.pack(side=BOTTOM, fill=BOTH)
below14 = Frame(below13, bg=bgc)
below14.pack(side=BOTTOM, fill=BOTH)
below15 = Frame(below14, bg=bgc)
below15.pack(side=BOTTOM, fill=BOTH)
below16 = Frame(below15, bg=bgc)
below16.pack(side=BOTTOM, fill=BOTH)
below17 = Frame(below16, bg=bgc)
below17.pack(side=BOTTOM, fill=BOTH)
below20 = Frame(below17, bg=bgc)
below20.pack(side=BOTTOM, fill=BOTH)
below21 = Frame(below20, bg=bgc)
below21.pack(side=BOTTOM, fill=BOTH)
below22 = Frame(below21, bg=bgc)
below22.pack(side=BOTTOM, fill=BOTH)
below23 = Frame(below22, bg=bgc)
below23.pack(side=BOTTOM, fill=BOTH)
below24 = Frame(below23, bg=bgc)
below24.pack(side=BOTTOM, fill=BOTH)
below25 = Frame(below24, bg=bgc)
below25.pack(side=BOTTOM, fill=BOTH)
below26 = Frame(below25, bg=bgc)
below26.pack(side=BOTTOM, fill=BOTH)
below27 = Frame(below26, bg=bgc)
below27.pack(side=BOTTOM, fill=BOTH)
below28 = Frame(below27, bg=bgc)
below28.pack(side=BOTTOM, fill=BOTH)
below28b = Frame(below28, bg=bgc)
below28b.pack(side=BOTTOM, fill=BOTH)
below28c = Frame(below28b, bg=bgc)
below28c.pack(side=BOTTOM, fill=BOTH)
below29 = Frame(below28c, bg=bgc)
below29.pack(side=BOTTOM, fill=BOTH)
below29b = Frame(below29, bg=bgc)
below29b.pack(side=BOTTOM, fill=BOTH)
below30 = Frame(below29b, bg=bgc)
below30.pack(side=BOTTOM, fill=BOTH)
below31 = Frame(below30, bg=bgc)
below31.pack(side=BOTTOM, fill=BOTH)
drawp_f = Frame(below31, bg=bgc)
drawp_f.pack(side=BOTTOM, fill=BOTH)
drawl_f = Frame(drawp_f, bg=bgc)
drawl_f.pack(side=BOTTOM, fill=BOTH)
pi_f1 = Frame(drawl_f, bg=bgc)
pi_f1.pack(side=BOTTOM, fill=BOTH)
pi_f2 = Frame(pi_f1, bg=bgc)
pi_f2.pack(side=BOTTOM, fill=BOTH)
pi_f3 = Frame(pi_f2, bg=bgc)
pi_f3.pack(side=BOTTOM, fill=BOTH)
pi_f4 = Frame(pi_f3, bg=bgc)
pi_f4.pack(side=BOTTOM, fill=BOTH)
pi_f5 = Frame(pi_f4, bg=bgc)
pi_f5.pack(side=BOTTOM, fill=BOTH)
pi_f6 = Frame(pi_f5, bg=bgc)
pi_f6.pack(side=BOTTOM, fill=BOTH)
pi_f7 = Frame(pi_f6, bg=bgc)
pi_f7.pack(side=BOTTOM, fill=BOTH)
pi_f8 = Frame(pi_f7, bg=bgc)
pi_f8.pack(side=BOTTOM, fill=BOTH)


# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

# ------------------------------
'''
Pack
padx, pady, ipadx and ipadx.
buttonE.pack(side='right', ipadx=20, padx=30)    ipadx is inside padding
buttonX.pack(fill='x')
listboxA.pack(fill='both', expand=1)

Grid
resultButton.grid(column=0, row=2, pady=10, sticky=tk.W)    sticky N W S or E

Place, by cords or 0-1
labelD.place(relx=0.5, rely=0.5)          labelA.place(x=0, y=0)

Getting and setting text input values must be in this order
func
button, and text input
packing

'''

# Setting name font
# s_font = tkFont.Font(family="Liberation Sans", size=12, weight="bold")

tog_on = ImageTk.PhotoImage(Image.open(rc_dir + "/support/tog_on4.png"))
tog_off = ImageTk.PhotoImage(Image.open(rc_dir + "/support/tog_off4.png"))

title = ttk.Label(second_frame, text="Rover Cam KI", font=("Liberation Sans", 24), background=bgc, foreground=fgc, wraplength=670, justify="center")

main_lab = ttk.Label(below1, text="Welcome to Rover Cam, change settings here. Refer to manual for instructions. All time "
                     "based settings are in seconds.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

load1 = Button(below1b, height=1,
                width=10,
                text="Load",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: load_btn())

save1 = Button(below1b, height=1,
                width=10,
                text="Save",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: save_btn())    # relief="flat",

st_par = ttk.Label(below1c, text="Rover Cam is designed to run without an internet connection, if accurate date stamps "
                    "are desired, the time will have to be set for each time the program starts. "
                    "Note: Will lose accuracy over long periods of time. Does not compensate for leap years, or "
                    "day light savings. "
                    "Aim for the time that the pi will be booted, plus about 1 minute, for boot and program start. "
                                       ,
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

st_lab = Label(below1d, text="Set Time", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_txtyr = Text(below1d, height=1, width=4, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtmo = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtda = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txthr = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtmi = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
st_txtse = Text(below1d, height=1, width=2, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

st_labyr = Label(below1e, text="year", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labmo = Label(below1e, text="mo", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labda = Label(below1e, text="da", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labhr = Label(below1e, text="hr", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labmi = Label(below1e, text="mi", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
st_labse = Label(below1e, text="se", font=("Liberation Sans", 12), bg=bgc, fg=fgc)


boot_on = True
def boot_tog_event(e):
    global boot_on
    global sett
    if boot_on == False:
        boot_tog.config(image=tog_off, relief=FLAT)
        sett["run_at_system_boot"] = "N"
        boot_on = True
    else:
        boot_tog.config(image=tog_on, relief=FLAT)
        sett["run_at_system_boot"] = "Y"
        boot_on = False
        
        # do crontab check here 2/2  These lines may accumulate if different storage devices are used
        path_to_check = rc_dir + "/Run-at-startup/*.py" 
        cron_line_to_add = f"@reboot sleep 40 && python3 {path_to_check} &"  # Replace this with the full cron line to add

        current_crontab = get_crontab()

        if path_to_check in current_crontab:
            return
        else:
            ask = askyesno("Permission Required", 'Your device is not set-up to run Rover Cam at system boot, ' +
                           'for this user, and storage device. Would you like Rover Cam to set it up for you?')
            if ask == True:
                updated_crontab = current_crontab + "\n" + cron_line_to_add + "\n"
                set_crontab(updated_crontab)

picam_on = True
def picam_tog_event(e):
    global picam_on
    global sett
    if picam_on == False:
        picam_tog.config(image=tog_off, relief=FLAT)
        sett["use_pi_camera"] = "N"
        picam_on = True
    else:
        picam_tog.config(image=tog_on, relief=FLAT)
        sett["use_pi_camera"] = "Y"
        picam_on = False

boot_lab = Label(below1f, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
boot_tog = Label(below1f, bg=bgc, fg=fgc)
boot_tog.bind("<Button-1>", boot_tog_event)


picam_par = ttk.Label(below3b, text='''To use a UBS camera leave this setting off.''',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")
picam_lab = Label(below3c, text="Use Pi Camera", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_tog = Label(below3c, bg=bgc, fg=fgc)
picam_tog.bind("<Button-1>", picam_tog_event)


s1_par = ttk.Label(below2, text="When motion is detected, how long should video be recorded for? "
                   "If set to 3 or less seconds, then images will be saved instead. If set to 0 every motion "
                   "frame will be saved. If set to 0.5 then one motion frame per half second will be saved, "
                   "while motion is detected.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s1_lab = Label(below3, text="Clip Time", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s1_txt = Text(below3, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)   # undo=True, wrap=NONE


reso_par = ttk.Label(below3ca, text='''Camera software may adjust this to one of it's nearest capability. Default 640x480.''',
                    font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

reso_lab = Label(below3cb, text="Resolution", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
reso_txt = Text(below3cb, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


fps_par = ttk.Label(below3d, text='''Set the max frames per second. This is limited by processing power so actual FPS maybe
lower. If using a pi camera and clips are playing fast with shorter clip times then 
set "Clip Time", try a lower FPS.''',
                    font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

fps_lab = Label(below3e, text="FPS", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
fps_txt = Text(below3e, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s2_par = ttk.Label(below4, text="Motion area size: a lower number here may cause false detections. "
                   "A higher number will only detect larger moving objects, or closer small objects. "
                   "Recommended 65 or higher, default 130.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s2_lab = Label(below5, text="Motion Area", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s2_txt = Text(below5, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s3_par = ttk.Label(below6, text="Motion sensitivity baseline: a lower number here will increase sensitivity. "
                            "Is simular to motion area, but is effected more by brightly lite environments. "
                            "If false detections are a problem, then motion area should be experimented with first. "
                            "4 is a good number here.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s3_lab = Label(below7, text="Motion Sens", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s3_txt = Text(below7, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s4_par = ttk.Label(below8, text="Mode 1 just records on motion.\n"
                                "Mode 2 records and preforms actions/audio on motion.\n"
                                "Mode 3 just preforms actions/audio on motion.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s4_lab = Label(below9, text="Mode", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s4_txt = Text(below9, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s8_par = ttk.Label(below10, text="A numerical code, of any length, used access menu.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")
s8_lab = Label(below11, text="PIN", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s8_txt = Text(below11, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

s9_par = ttk.Label(below12, text='Number the failed PIN attempts before key input will be locked for '
                                '"Failed PIN Lock Time"',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")
s9_lab = Label(below13, text="Allowable PIN Attempts", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s9_txt = Text(below13, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

s10_par = ttk.Label(below14, text='Time to lock any key input after a failed PIN attempt, in seconds. Enter "inf" '
                    'to lock until pi, or program is restarted.',
                    font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")
s10_lab = Label(below15, text="Failed PIN Lock Time", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s10_txt = Text(below15, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

s5_par = ttk.Label(below16, text='Optionally play audio or python3 files on motion. '
            'Will play any and all .wav or .py files in "audio" folder '
            'one after another in alphabetical order '
            '(can be left on, will not fault out even if no files in location).',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")
s5_lab = Label(below17, text="Play Audio", font=("Liberation Sans", 12), bg=bgc, fg=fgc)

play_audio = True
def audio_tog_event(e):
    global play_audio
    global sett
    if play_audio == False:
        audio_tog.config(image=tog_off, relief=FLAT)
        sett["play_audio"] = "N"
        play_audio = True
    else:
        audio_tog.config(image=tog_on, relief=FLAT)
        sett["play_audio"] = "Y"
        play_audio = False

# audio_lab = Label(below1f, text="Run At System Boot", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
audio_tog = Label(below17, bg=bgc, fg=fgc)
audio_tog.bind("<Button-1>", audio_tog_event)


s6_par = ttk.Label(below20, text="Delay Audio will delay the running of files, in the audio folder. "
                   "A correct PIN entry in this time frame will cancel the audio.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s6_lab = Label(below21, text="Delay Audio", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s6_txt = Text(below21, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s11_par = ttk.Label(below22, text='Activation delay will add a time delay from boot up, and disabled state. '
                    'Is useful if operator is physically inside the camera view, while using key inputs, '
                    'or will pass through the camera view when leaving the area. (in seconds)',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s11_lab = Label(below23, text="Activation Delay", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s11_txt = Text(below23, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


s12_par = ttk.Label(below24, text="Setting camera index to -1 is recommended, since the camera indexes on "
                    "the pi could change. -1 will find any camera attached by lowest index number.",
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

s12_lab = Label(below25, text="Camera Index", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
s12_txt = Text(below25, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


a_par = ttk.Label(below26, text='Here you can write your custom program that turns GPIO pins on and off. '
                  'These are referred to as "Actions", each Action controls a separate pin. '
                  'The number that comes after "on" or "off" is the time in seconds that it will remain in that state. '
                  'Enter "on" or "off", followed by a number of seconds to remain in that state, repeat on a new line. '
                  'Alternate state with each new line. Always start in "off" state, even if for zero seconds. '
                  'A correct PIN entry will cancel all actions if entered within the first "off" time frame. '
                  'Decimal numbers accepted. Uses BCM numbering mode. Pin number is in brackets.',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

a_lab1 = Label(below27, text="Action 1 (12)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab2 = Label(below27, text="Action 2 (16)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab3 = Label(below27, text="Action 3 (20)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab4 = Label(below27, text="Action 4 (21)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)

a_txt1 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt2 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt3 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt4 = Text(below28, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


a_lab5 = Label(below28b, text="Action 5 (23)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab6 = Label(below28b, text="Action 6 (24)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab7 = Label(below28b, text="Action 7 (13)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
a_lab8 = Label(below28b, text="Action 8 (19)", font=("Liberation Sans", 12), bg=bgc, fg=fgc)

a_txt5 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt6 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt7 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)
a_txt8 = Text(below28c, height=12, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)


load2 = Button(below29, height=1,
                width=10,
                text="Load",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: load_btn())

save2 = Button(below29, height=1,
                width=10,
                text="Save",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: save_btn())

# aoi ---------

aoi_par = ttk.Label(below29b, text='Select Area Of Interest (AOI). Click the "Select/Add To AOI" button to set. '
                    'Another window will pop-up where you can click and drag. A green rectangle will indicate the '
                    'area that will be the AOI. Have a camera plugged in with the proper index setting. If an AOI is '
                    'set then only motion that is detected inside the AOI, will trigger '
                    'actions, clip recording, or audio. To remove the AOI effect, just clear, and save. '
                    'Will only work properly on 4:3 resolution ratios, otherwise AOI boxes will be warped.',
                 font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

aoi_img = Label(below30, bg=bgc, fg=fgc)

aoi_btn = Button(below31, height=1,
                width=18,
                text="Select/Add To AOI",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: select_aoi())

aoi_clear_btn = Button(below31, height=1,
                width=18,
                text="Clear AOI",
                font=("Liberation Sans", 12),
                bg=btc,
                command=lambda: clear_aoi())


draw_par = ttk.Label(drawp_f, text='''Draw AOIs on saved clips and images.''',
                    font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

draw_lab = Label(drawl_f, text="Draw AOI", font=("Liberation Sans", 12), bg=bgc, fg=fgc)

draw_aoi = True
def draw_tog_event(e):
    global draw_aoi
    global sett
    if draw_aoi == False:
        draw_tog.config(image=tog_off, relief=FLAT)
        sett["draw_aoi"] = "N"
        draw_aoi = True
    else:
        draw_tog.config(image=tog_on, relief=FLAT)
        sett["draw_aoi"] = "Y"
        draw_aoi = False

draw_tog = Label(drawl_f, bg=bgc, fg=fgc)
draw_tog.bind("<Button-1>", draw_tog_event)


picam_sett_par = ttk.Label(pi_f1, text='''PiCamera spacific settings. May have different effects depending on type and
version of pi camera used. See PiCamera documentation.''',
                    font=("Liberation Sans", 12), background=bgc, foreground=fgc, wraplength=670, justify="left")

picam_expo_lab = Label(pi_f2, text="Exposure Mode", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_expo_txt = Text(pi_f2, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

picam_sens_lab = Label(pi_f3, text="Sensor Mode", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_sens_txt = Text(pi_f3, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

picam_awb_lab = Label(pi_f4, text="AWB Mode", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_awb_txt = Text(pi_f4, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

picam_brt_lab = Label(pi_f5, text="Brightness", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_brt_txt = Text(pi_f5, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

picam_con_lab = Label(pi_f6, text="Contrast", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_con_txt = Text(pi_f6, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

picam_iso_lab = Label(pi_f7, text="ISO", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_iso_txt = Text(pi_f7, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

picam_shut_lab = Label(pi_f8, text="Shutter Speed", font=("Liberation Sans", 12), bg=bgc, fg=fgc)
picam_shut_txt = Text(pi_f8, height=1, width=12, font=("Liberation Sans", 12), bg=bgt, fg=fgc)

aoi_par.pack(side='left', padx=100, pady=10)
aoi_img.pack(side="top", fill="both", expand=1, pady=20)
aoi_btn.pack(side='left', padx=(190, 50), pady=(20, 30))
aoi_clear_btn.pack(side='left', padx=(50, 50), pady=(20, 30))
# ---------

# title.pack(side='left', padx=340, pady=(50, 20))
title.pack(fill="none", expand=True, pady=(60, 20))     # to center
main_lab.pack(side='left', padx=100, pady=10)

load1.pack(side='left', padx=(200, 0), pady=20)
save1.pack(side='right', padx=(0, 200), pady=20)

st_par.pack(side='left', padx=100, pady=10)
st_lab.pack(side='left', padx=(140, 0), pady=(10, 0))
st_txtyr.pack(side='left', padx=(110, 10), pady=(10, 0))
st_txtmo.pack(side='left', padx=10, pady=(10, 0))
st_txtda.pack(side='left', padx=10, pady=(10, 0))
st_txthr.pack(side='left', padx=10, pady=(10, 0))
st_txtmi.pack(side='left', padx=10, pady=(10, 0))
st_txtse.pack(side='left', padx=10, pady=(10, 0))

st_labyr.pack(side='left', padx=(320, 10), pady=(0, 10))
st_labmo.pack(side='left', padx=(15, 10), pady=(0, 10))
st_labda.pack(side='left', padx=10, pady=(0, 10))
st_labhr.pack(side='left', padx=(13, 16), pady=(0, 10))
st_labmi.pack(side='left', padx=(9, 14), pady=(0, 10))
st_labse.pack(side='left', padx=10, pady=(0, 10))

boot_lab.pack(side='left', padx=(140, 0), pady=10)
boot_tog.config(image=tog_off)
# tog_on_img.image = tog_on
boot_tog.pack(side='right', padx=(0, 500), pady=10)

picam_par.pack(side='left', padx=100, pady=10)
picam_lab.pack(side='left', padx=(140, 0), pady=10)
picam_tog.config(image=tog_off)
picam_tog.pack(side='right', padx=(0, 500), pady=10)

s1_par.pack(side='left', padx=100, pady=10)
s1_lab.pack(side='left', padx=(140, 0), pady=10)
s1_txt.pack(side='right', padx=(0, 440), pady=10)

reso_par.pack(side='left', padx=100, pady=10)
reso_lab.pack(side='left', padx=(140, 0), pady=10)
reso_txt.pack(side='right', padx=(0, 440), pady=10)

fps_par.pack(side='left', padx=100, pady=10)
fps_lab.pack(side='left', padx=(140, 0), pady=10)
fps_txt.pack(side='right', padx=(0, 440), pady=10)

s2_par.pack(side='left', padx=100, pady=10)
s2_lab.pack(side='left', padx=(140, 0), pady=10)
s2_txt.pack(side='right', padx=(0, 440), pady=10)

s3_par.pack(side='left', padx=100, pady=10)
s3_lab.pack(side='left', padx=(140, 0), pady=10)
s3_txt.pack(side='right', padx=(0, 440), pady=10)

s4_par.pack(side='left', padx=100, pady=10)
s4_lab.pack(side='left', padx=(140, 0), pady=10)
s4_txt.pack(side='right', padx=(0, 440), pady=10)

s5_par.pack(side='left', padx=100, pady=10)
s5_lab.pack(side='left', padx=(140, 0), pady=10)
# s5_txt.pack(side='right', padx=(0, 440), pady=10)

# audio_lab.pack(side='left', padx=(140, 0), pady=10)
audio_tog.config(image=tog_off)
audio_tog.pack(side='right', padx=(0, 500), pady=10)

s6_par.pack(side='left', padx=100, pady=10)
s6_lab.pack(side='left', padx=(140, 0), pady=10)
s6_txt.pack(side='right', padx=(0, 440), pady=10)

s8_par.pack(side='left', padx=100, pady=10)
s8_lab.pack(side='left', padx=(140, 0), pady=10)   # special cause long label
s8_txt.pack(side='right', padx=(0, 440), pady=10)

s9_par.pack(side='left', padx=100, pady=10)
s9_lab.pack(side='left', padx=(140, 0), pady=10)    # special cause long label
s9_txt.pack(side='right', padx=(0, 440), pady=10)

s10_par.pack(side='left', padx=100, pady=10)
s10_lab.pack(side='left', padx=(140, 0), pady=10)
s10_txt.pack(side='right', padx=(0, 440), pady=10)

s11_par.pack(side='left', padx=100, pady=10)
s11_lab.pack(side='left', padx=(140, 0), pady=10)
s11_txt.pack(side='right', padx=(0, 440), pady=10)

s12_par.pack(side='left', padx=100, pady=10)
s12_lab.pack(side='left', padx=(140, 0), pady=10)
s12_txt.pack(side='right', padx=(0, 440), pady=10)

a_par.pack(side='left', padx=100, pady=(10, 20))

a_lab1.pack(side='left', padx=(170, 0), pady=0)
a_lab2.pack(side='left', padx=(50, 0), pady=0)
a_lab3.pack(side='left', padx=(50, 0), pady=0)
a_lab4.pack(side='left', padx=(50, 0), pady=0)

a_txt1.pack(side='left', padx=(160, 15), pady=10)
a_txt2.pack(side='left', padx=15, pady=10)
a_txt3.pack(side='left', padx=15, pady=10)
a_txt4.pack(side='left', padx=15, pady=10)

a_lab5.pack(side='left', padx=(170, 0), pady=(10,0))
a_lab6.pack(side='left', padx=(50, 0), pady=(10,0))
a_lab7.pack(side='left', padx=(50, 0), pady=(10,0))
a_lab8.pack(side='left', padx=(50, 0), pady=(10,0))

a_txt5.pack(side='left', padx=(160, 15), pady=10)
a_txt6.pack(side='left', padx=15, pady=10)
a_txt7.pack(side='left', padx=15, pady=10)
a_txt8.pack(side='left', padx=15, pady=10)

draw_par.pack(side='left', padx=100, pady=10)
draw_lab.pack(side='left', padx=(140, 0), pady=(10, 50))
draw_tog.config(image=tog_off)
draw_tog.pack(side='right', padx=(0, 500), pady=(10, 50))

picam_sett_par.pack(side='left', padx=100, pady=10)
picam_expo_lab.pack(side='left', padx=(140, 0), pady=10)
picam_expo_txt.pack(side='right', padx=(0, 440), pady=10)

picam_sens_lab.pack(side='left', padx=(140, 0), pady=10)
picam_sens_txt.pack(side='right', padx=(0, 440), pady=10)

picam_awb_lab.pack(side='left', padx=(140, 0), pady=10)
picam_awb_txt.pack(side='right', padx=(0, 440), pady=10)

picam_brt_lab.pack(side='left', padx=(140, 0), pady=10)
picam_brt_txt.pack(side='right', padx=(0, 440), pady=10)

picam_con_lab.pack(side='left', padx=(140, 0), pady=10)
picam_con_txt.pack(side='right', padx=(0, 440), pady=10)

picam_iso_lab.pack(side='left', padx=(140, 0), pady=10)
picam_iso_txt.pack(side='right', padx=(0, 440), pady=10)

picam_shut_lab.pack(side='left', padx=(140, 0), pady=(10, 100))
picam_shut_txt.pack(side='right', padx=(0, 440), pady=(10, 100))


load2.pack(side='left', padx=(200, 0), pady=(20, 35))
save2.pack(side='right', padx=(0, 200), pady=(20, 35))

load_btn()      # start with all loaded


root.mainloop()
