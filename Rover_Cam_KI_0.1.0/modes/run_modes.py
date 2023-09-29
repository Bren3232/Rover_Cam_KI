
# Copyright (C) 2023 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam KI project.
# Please see the LICENSE file that should have been included as part of this package.

# If running this file for testing to have date correct run by running "/support/start-up.py".

import os

rc_dir = os.path.abspath(__file__)
rc_dir = rc_dir[:rc_dir.find('modes') - 1]
# print(rc_dir)


try:

    import cv2
    import numpy as np
    import random
    from subprocess import run
    from threading import Thread
    import RPi.GPIO as GPIO    
    from tkinter import *
    import variables as sett
    import time

    time.sleep(1)

    red_led = 22
    green_led = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(red_led, GPIO.OUT)
    GPIO.setup(green_led, GPIO.OUT)
    GPIO.output(red_led, GPIO.LOW)
    GPIO.output(green_led, GPIO.LOW)

    def shutdown():          
        sett.switch.ex = True
        run(['python3', rc_dir + '/support/shutdown.py'])

    def reboot():
        sett.switch.ex = True
        run(['python3', rc_dir + '/support/reboot.py'])
            

    def red_led_thread(on_off_seq):
        global red_led
        n = 1
        for s in on_off_seq:

            if n % 2 != 0:
                if s != 0:
                    GPIO.output(red_led, GPIO.HIGH)
                    time.sleep(s)
            else:
                if s != 0:
                    GPIO.output(red_led, GPIO.LOW)
                    time.sleep(s)
            n += 1
        GPIO.output(red_led, GPIO.LOW)


    def green_led_thread(on_off_seq):
        global green_led
        n = 1
        for s in on_off_seq:
            if n % 2 != 0:
                if s != 0:
                    GPIO.output(green_led, GPIO.HIGH)
                    time.sleep(s)
            else:
                if s != 0:
                    GPIO.output(green_led, GPIO.LOW)
                    time.sleep(s)
            n += 1
        GPIO.output(green_led, GPIO.LOW)


    pr = open(rc_dir + "/support/RC_config.txt", "r")
    prog = pr.read().splitlines()
    pr.close()

    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []

    for i in prog:
        if i != "" and i[0:2] == "a1":
            a1.append(i)
        elif i != "" and i[0:2] == "a2":
            a2.append(i)  
        elif i != "" and i[0:2] == "a3":
            a3.append(i)
        elif i != "" and i[0:2] == "a4":
            a4.append(i)
        elif i != "" and i[0:2] == "a5":
            a5.append(i)
        elif i != "" and i[0:2] == "a6":
            a6.append(i)
        elif i != "" and i[0:2] == "a7":
            a7.append(i)
        elif i != "" and i[0:2] == "a8":
            a8.append(i)
        # Note date relys on start-up.py to be correct
        elif i != "" and i[0:10] == "set_time =":
            st = i[10:].split()
            sett.dates.yr = int(st[0].strip())  # retrieved
            sett.dates.mo = int(st[1].strip())
            sett.dates.da = int(st[2].strip())
            sett.dates.hr = int(st[3].strip())
            sett.dates.mi = int(st[4].strip())
            sett.dates.se = int(st[5].strip())
        elif i != "" and i[0:12] == "play_audio =":
            if "y" in i[10:].lower():
                sett.switch.play = True
                audio = run(['ls', rc_dir + '/audio'], capture_output=True).stdout
                audio = audio.decode("utf-8").splitlines()
            else:
                audio = []
        elif i != "" and i[0:13] == "delay_audio =":
            delay_audio = float(i[13:].strip())
        elif i != "" and i[0:13] == "start_delay =":
            sett.times.start_delay = float(i[13:].strip())
        elif i != "" and i[0:14] == "camera_index =":
            camera_index = int(i[14:].strip())
        elif i != "" and i[0:11] == "clip_time =":
            clip_time = float(i[11:].strip())   
        elif i != "" and i[0:15] == "use_pi_camera =":
            if "y" in i[15:].lower():
                use_pi_camera = True
            else:
                use_pi_camera = False   
        elif i != "" and i[0:5] == "fps =":
            fps = float(i[5:].strip())         
        elif i != "" and i[0:13] == "motion_area =":
            ma = float(i[13:].strip())  
        elif i != "" and i[0:13] == "motion_sens =":
            motion_sens = float(i[13:].strip())

            # New for keypad version
        elif i != "" and i.startswith('pin ='):
            [sett.lists.pin.append(int(x)) for x in i.split('=')[1].strip()]
        elif i != "" and i.startswith('allowable_pin_attempts ='):
            sett.nums.allowable_pin_attempts = int(i.split('=')[1].strip())
        elif i != "" and i.startswith("failed_pin_lock_time ="):
            if "inf" in i.split('=')[1]:
                sett.times.failed_pin_lock = np.inf    # should now be called
            else:
                sett.times.failed_pin_lock = float(i.split('=')[1].strip())
        elif i != "" and i.startswith('mode ='):
            sett.nums.mode = int(i.split('=')[1].strip())
        elif i != "" and i.startswith('resolution ='):
            reso = i.split('=')[1]
            sett.lists.resolution = (int(reso.split('x')[0].strip()), int(reso.split('x')[1].strip()))
        elif i != "" and i.startswith('draw_aoi ='):
            if 'y' in i.split('=')[1].lower():
                sett.switch.draw_aoi = True
        elif i != "" and i.startswith('exposure_mode ='):
            sett.strings.exposure_mode = i.split('=')[1].strip()
        elif i != "" and i.startswith('sensor_mode ='):
            sett.strings.sensor_mode = i.split('=')[1].strip()
        elif i != "" and i.startswith('awb_mode ='):
            sett.strings.awb_mode = i.split('=')[1].strip()
        elif i != "" and i.startswith('brightness ='):
            if 'e' not in i.split('=')[1]:
                sett.nums.brightness = int(i.split('=')[1])
        elif i != "" and i.startswith('contrast ='):
            if 'e' not in i.split('=')[1]:
                sett.nums.contrast = int(i.split('=')[1])
        elif i != "" and i.startswith('iso ='):
            if 'e' not in i.split('=')[1]:
                sett.nums.iso = int(i.split('=')[1])
        elif i != "" and i.startswith('shutter_speed ='):
            if 'e' not in i.split('=')[1]:
                sett.nums.shutter_speed = int(i.split('=')[1])

    motion_area = int(ma / 1000000 * (sett.lists.resolution[0] * sett.lists.resolution[1]))

    if len(audio) == 0:
        sett.switch.play = False

    a1h = []                    # list of a1 HIGH's
    a1o = []                      # list of a1 LOW's
    for i in a1:
        if "on" in i.lower():
            a1h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a1o.append(float(i.split()[-1]))
    a1h.append(0)
    a1o.append(0)

    # Action 2
    a2h = []
    a2o = []
    for i in a2:
        if "on" in i.lower():
            a2h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a2o.append(float(i.split()[-1]))
    a2h.append(0)
    a2o.append(0)

    # Action 3
    a3h = []
    a3o = []
    for i in a3:
        if "on" in i.lower():
            a3h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a3o.append(float(i.split()[-1]))
    a3h.append(0)
    a3o.append(0)

    # Action 4
    a4h = []
    a4o = []
    for i in a4:
        if "on" in i.lower():
            a4h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a4o.append(float(i.split()[-1]))
    a4h.append(0)
    a4o.append(0)

    # Action 5
    a5h = []
    a5o = []
    for i in a5:
        if "on" in i.lower():
            a5h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a5o.append(float(i.split()[-1]))
    a5h.append(0)
    a5o.append(0)

    # Action 6
    a6h = []
    a6o = []
    for i in a6:
        if "on" in i.lower():
            a6h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a6o.append(float(i.split()[-1]))
    a6h.append(0)
    a6o.append(0)

    # Action 7
    a7h = []
    a7o = []
    for i in a7:
        if "on" in i.lower():
            a7h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a7o.append(float(i.split()[-1]))
    a7h.append(0)
    a7o.append(0)

    # Action 8
    a8h = []
    a8o = []
    for i in a8:
        if "on" in i.lower():
            a8h.append(float(i.split()[-1]))
        elif "off" in i.lower():
            a8o.append(float(i.split()[-1]))
    a8h.append(0)
    a8o.append(0)


    # Load aoi pts list if any -----------------------------
    p = open(rc_dir + "/support/aoi_pts.txt", "r")
    p.readline()
    pts = p.read().split()
    p.close()


    def runAction(on_list, off_list, pin):
        GPIO.setup(pin, GPIO.OUT)
        time.sleep(0.01)

        on_list_idx = 0
        off_list_idx = 0
        for i in range(max(len(on_list), len(off_list))):

            if sett.switch.ex or sett.switch.pin_correct:
                break

            GPIO.output(pin, GPIO.LOW)
            
            if off_list_idx == 0:
                at = time.time()
                while time.time() < at + off_list[0]:  # allow correct pin to cancel actions
                    time.sleep(0.01)
                    if sett.switch.pin_correct:
                        return
            else:
                time.sleep(off_list[off_list_idx])

            GPIO.output(pin, GPIO.HIGH)

            time.sleep(on_list[on_list_idx])   # a zero is appends to on off off lists

            if on_list_idx < len(on_list) - 1:
                on_list_idx += 1

            if off_list_idx < len(off_list) - 1:
                off_list_idx += 1
        GPIO.output(pin, GPIO.LOW)


    def play_audio(aud, delay_aud):    # try with mp3 files
        sett.switch.is_playing = True
        
        at = time.time()
        while time.time() < at + delay_aud:  # make cancelable with pin
            time.sleep(0.01)
            if sett.switch.pin_correct:
                sett.switch.is_playing = False
                return

        for i in aud:      # plays one after other, all .wav and .py files in folder in alphabetical order
            if ".wav" in i:  # mp3, flac did not play well, only use .wav
    #             run(['omxplayer', f'{rc_dir}/audio/{i}'])  # works but depriciated
                run(['aplay', f'{rc_dir}/audio/{i}'])
    #             run(['vlc', 'path to vid clip'])  # does not work here
    #             run(['cvlc', f'{rc_dir}/audio/{i}']) # only plays once per file run

            if ".py" in i:
                run(['python3', f'{rc_dir}/audio/{i}'])

        sett.switch.is_playing = False


    def check_mode():
        global red_led, green_led
        if sett.switch.is_disabled:  # use green led if state is in disabled
            led_used = green_led
        else:
            led_used = red_led

        for i in range(sett.nums.mode):
            if sett.switch.stop_check_mode or sett.switch.ex:
                break

            GPIO.output(led_used, GPIO.HIGH)  # new way  not using gpio zero
            time.sleep(1)
            GPIO.output(led_used, GPIO.LOW)
            time.sleep(1)
        time.sleep(1)

        count = os.listdir(sett.dates.sdate)
        for f in count:

            if sett.switch.stop_check_mode or sett.switch.ex:
                break

            GPIO.output(led_used, GPIO.HIGH)
            time.sleep(0.26)
            GPIO.output(led_used, GPIO.LOW)
            time.sleep(0.26)


    def get_code(k):

        if k.keycode == 23:
            return 'tab'
        elif k.keycode == 106 or k.keycode == 61:
            return '/'
        elif k.keycode == 63 or k.keycode == 65:
            return '*'
        elif k.keycode == 22:
            return 'back'
        elif k.keycode == 79 or k.keycode == 16:
            return 7
        elif k.keycode == 80 or k.keycode == 17:
            return 8
        elif k.keycode == 81 or k.keycode == 18:
            return 9
        elif k.keycode == 82 or k.keycode == 20:
            return '-'
        elif k.keycode == 83 or k.keycode == 13:
            return 4
        elif k.keycode == 84 or k.keycode == 14:
            return 5
        elif k.keycode == 85 or k.keycode == 15:
            return 6
        elif k.keycode == 86 or k.keycode == 21:
            return '+'
        elif k.keycode == 87 or k.keycode == 10:
            return 1
        elif k.keycode == 88 or k.keycode == 11:
            return 2
        elif k.keycode == 89 or k.keycode == 12:
            return 3
        elif k.keycode == 104 or k.keycode == 36:
            return 'enter'
        elif k.keycode == 90 or k.keycode == 19:
            return 0
        elif k.keycode == 91 or k.keycode == 65:  # 65 is period on keyboard
            return 'del'


    def pin_timer_thread():
        sett.times.pin_timer = time.time()
        while True:
            time.sleep(0.2)
            if sett.switch.pin_correct:   # Or this, no because "back" will set pin_correct False
                while sett.switch.pin_correct:
                    time.sleep(0.2)

                    if time.time() - sett.times.pin_timer > 300:  # leave menus if idle for 5 mins
                        sett.lists.b_list = []
                        sett.lists.after_pin = []
                        sett.lists.after_after = []
                        sett.switch.in_option = False
                        sett.switch.pin_correct = False
                        sett.dates.set_date_list = []
                        sett.switch.set_d = False
                        sett.switch.select_mode = False
                        break
                break

            if time.time() - sett.times.pin_timer > sett.times.pin_time_frame:   # pin_time_frame is hard set at 30s
                if len(sett.lists.b_list) != 0:
                    rlt = Thread(target=red_led_thread, args=((0.3, 0.3),))
                    rlt.daemon = True
                    rlt.start()
                    sett.nums.fa_num += 1
                    sett.nums.fa_n += 1
                    date_ = f"{sett.dates.yr}-{sett.dates.mo}-{sett.dates.da}  {sett.dates.hr}:{sett.dates.mi}:" \
                           f"{sett.dates.se}"
                    fa = open(rc_dir + f"/Clips/failed_pin_logg.txt", "a")
                    fa.write(f'PIN attempt failed in mode: {sett.nums.mode}, on run: {sett.dates._sdate}, at time: {date_}\n')
                    fa.close()

                    if sett.nums.fa_n >= sett.nums.allowable_pin_attempts:
                        sett.times.lock_t = time.time() + sett.times.failed_pin_lock
                        sett.switch.lock = True
                        sett.nums.fa_n = 0

                    sett.lists.b_list = []
                    sett.lists.after_pin = []
                    sett.switch.in_option = False
                    sett.switch.pin_correct = False
                    sett.dates.set_date_list = []
                    sett.switch.set_d = False
                break


    def start_delay_thread():  # to use start delay without freezing the key input
        global m
        time.sleep(2)  # Camera sensor warm up
        for_t = int(sett.times.start_delay)
        expo = np.linspace(2, 0, for_t)
        sdrlt = Thread(target=red_led_thread, args=(expo,))
        sdrlt.daemon = True
        sdrlt.start()

        t = time.time()
        while time.time() < t + sett.times.start_delay:
            time.sleep(0.1)
            root_sec = int(time.time() - sett.times.start)
            root_mi = root_sec // 60
            sett.dates.mi = root_mi % 60
            sett.dates.se = int(root_sec % 60)
            if root_mi >= m:
                sett.dates.hr += 1
                m += 60
                sett.dates.mi = 0
                if sett.dates.hr >= 24:
                    sett.dates.hr = 0
                    sett.dates.da += 1
                    if sett.dates.mo == 1 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 2 and sett.dates.da > 28:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 3 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 4 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 5 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 6 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 7 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 8 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 9 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 10 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 11 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 12 and sett.dates.da > 31:
                        sett.dates.mo = 1
                        sett.dates.da = 1
                        sett.dates.yr += 1
        sett.switch.is_disabled = False

    sdt = Thread(target=start_delay_thread, daemon=True)  # need this in 2 spots for if is alive


    def key_up(key):
        global ca, sdt

        sett.strings.final_key = get_code(key)
        sett.switch.stop_check_mode = True      # stops check mode if any key is pressed

        if not sett.switch.pin_correct:
            if sett.strings.final_key == "back":       # back does nothing in pin enter mode
                return
            if len(sett.lists.b_list) == 0:
                ptt = Thread(target=pin_timer_thread, daemon=True)
                ptt.start()
            sett.lists.b_list.append(sett.strings.final_key)
        else:
            sett.lists.after_pin = [sett.strings.final_key]
            if sett.lists.after_pin == ['back']:    # exit any option like set date, mode select, but not disable
                sett.switch.pin_correct = False
                sett.switch.in_option = False
                sett.lists.b_list = []
                sett.lists.after_pin = []
                sett.lists.after_after = []
                sett.dates.set_date_list = []
                sett.switch.set_d = False
                sett.switch.select_mode = False


        if sett.switch.in_option:

            if sett.lists.after_pin == ['back']:    # exit any option like set date, mode select, but not disable
                sett.switch.pin_correct = False
                sett.switch.in_option = False
                sett.lists.b_list = []
                sett.lists.after_pin = []
                sett.lists.after_after = []
                sett.dates.set_date_list = []

                sett.switch.set_d = False
                sett.switch.select_mode = False

    # ---------- Select Mode "tab" ----------
            if sett.switch.select_mode:

                if sett.strings.final_key in range(1, 4):
                    sett.nums.mode = sett.strings.final_key

                    f = open(rc_dir + "/support/RC_config.txt", "r+")
                    fl = f.read().splitlines()
                    for idx, i in enumerate(fl):
                        if i != "" and i.startswith('mode ='):
                            fl[idx] = f'mode = {sett.nums.mode}'

                    f.truncate(0)
                    f.seek(0)  # stops from writting with NULs
                    for i in fl:
                        f.write(str(i) + "\n")
                    f.close()
                    
                    green_led7 = Thread(target=green_led_thread, args=((0.3, 0.3, 0.3, 0.3, 0.3),))
                    green_led7.daemon = True
                    green_led7.start()

                    # Reset vars
                    sett.times.start = time.time() - (sett.dates.mi * 60) - sett.dates.se 
                    sett.lists.after_pin = []
                    sett.lists.after_after = []
                    sett.dates.set_date_list = []
                    sett.switch.in_option = False
                    sett.switch.pin_correct = False
                    sett.dates.set_date_list = []
                    sett.switch.set_d = False
                    sett.switch.select_mode = False

    #  end ---------- Select Mode "tab" ----------


    # --------- Set Date "enter" ----------------
            if sett.switch.set_d:

                if type(sett.strings.final_key) == int:
                    sett.lists.after_after.append(int(sett.strings.final_key))

                    if len(sett.lists.after_after) == 4 and len(sett.dates.set_date_list) == 0:
                        sett.dates.set_date_list.append(int(''.join(str(x) for x in sett.lists.after_after)))
                        sett.lists.after_after = []
                        green_led1 = Thread(target=green_led_thread, args=((0.3,),))
                        green_led1.daemon = True
                        green_led1.start()
                    elif len(sett.lists.after_after) == 2 and len(sett.dates.set_date_list) == 1:
                        sett.dates.set_date_list.append(int(''.join(str(x) for x in sett.lists.after_after)))
                        sett.lists.after_after = []
                        green_led2 = Thread(target=green_led_thread, args=((0.3,),))
                        green_led2.daemon = True
                        green_led2.start()
                    elif len(sett.lists.after_after) == 2 and len(sett.dates.set_date_list) == 2:
                        sett.dates.set_date_list.append(int(''.join(str(x) for x in sett.lists.after_after)))
                        sett.lists.after_after = []
                        green_led3 = Thread(target=green_led_thread, args=((0.3,),))
                        green_led3.daemon = True
                        green_led3.start()
                    elif len(sett.lists.after_after) == 2 and len(sett.dates.set_date_list) == 3:
                        sett.dates.set_date_list.append(int(''.join(str(x) for x in sett.lists.after_after)))
                        sett.lists.after_after = []
                        green_led4 = Thread(target=green_led_thread, args=((0.3,),))
                        green_led4.daemon = True
                        green_led4.start()
                    elif len(sett.lists.after_after) == 2 and len(sett.dates.set_date_list) == 4:
                        sett.dates.set_date_list.append(int(''.join(str(x) for x in sett.lists.after_after)))
                        sett.lists.after_after = []
                        green_led5 = Thread(target=green_led_thread, args=((0.3,),))
                        green_led5.daemon = True
                        green_led5.start()
                    elif len(sett.lists.after_after) == 2 and len(sett.dates.set_date_list) == 5:
                        sett.dates.set_date_list.append(int(''.join(str(x) for x in sett.lists.after_after)))
                        sett.lists.after_after = []
                        green_led6 = Thread(target=green_led_thread, args=((0.3, 0.3, 0.3, 0.3, 0.3),))
                        green_led6.daemon = True
                        green_led6.start()

                    if len(sett.dates.set_date_list) == 6:
                        sett.dates._sdate = f"{sett.dates.set_date_list[0]:04}-{sett.dates.set_date_list[1]:02}-{sett.dates.set_date_list[2]:02}-" \
                               f"{sett.dates.set_date_list[3]:02}-{sett.dates.set_date_list[4]:02}-{sett.dates.set_date_list[5]:02}"
                        sett.dates.sdate = rc_dir + "/Clips/" + sett.dates._sdate + "_" + str(ran)
                        run(['mkdir', sett.dates.sdate]) 


                        sett.dates.yr = sett.dates.set_date_list[0]
                        sett.dates.mo = sett.dates.set_date_list[1]
                        sett.dates.da = sett.dates.set_date_list[2]
                        sett.dates.hr = sett.dates.set_date_list[3]
                        sett.dates.mi = sett.dates.set_date_list[4]     # fixme mi is always 0 even before this, try start at startup.py
                        sett.dates.se = sett.dates.set_date_list[5]

                        f = open(rc_dir + "/support/RC_config.txt", "r+")
                        fl = f.read().splitlines()
                        for idx, i in enumerate(fl):
                            if i != "" and i[0:10] == "set_time =":
                                fl[idx] = f'set_time = {sett.dates.yr:04} {sett.dates.mo:02} {sett.dates.da:02} {sett.dates.hr:02} ' \
                                          f'{sett.dates.mi:02} {sett.dates.se:02}'
                        f.truncate(0)
                        f.seek(0)                    # stops from writting with NULs
                        for i in fl:
                            f.write(str(i) + "\n")
                        f.close()

                        # Reset vars
                        sett.times.start = time.time() - (sett.dates.mi * 60) - sett.dates.se 
                        sett.nums.out_num = 0
                        sett.lists.after_pin = []
                        sett.lists.after_after = []
                        sett.dates.set_date_list = []
                        sett.switch.in_option = False
                        sett.switch.set_d = False

            return
    # End --------- Set Date "enter" ----------------


        if sett.switch.lock:
            if time.time() <= sett.times.lock_t:
                sett.lists.b_list = []

                lrlt = Thread(target=red_led_thread, args=((0.5,),))
                lrlt.daemon = True
                lrlt.start()
                return
            else:
                sett.switch.lock = False


        if len(sett.lists.b_list) >= len(sett.lists.pin):
            if sett.lists.b_list == sett.lists.pin and not sett.switch.pin_correct:
                green_led = Thread(target=green_led_thread, args=((0.5,),))
                green_led.daemon = True
                green_led.start()
                sett.switch.pin_correct = True
                sett.nums.fa_n = 0
            
            if sett.switch.pin_correct:      # new on pi
                if sett.lists.after_pin == ['tab'] or sett.lists.after_pin == ['del']:
                    sett.lists.b_list = []
                    sett.lists.after_pin = []
                    sett.switch.lock = False
                    sett.times.lock_t = 0
                    sett.switch.in_option = True
                    sett.switch.select_mode = True

                elif sett.lists.after_pin == ['/']:    # xx seems working  needs testing on pi
                    sett.lists.b_list = []
                    sett.lists.after_pin = []
                    sett.switch.pin_correct = False
                    sett.switch.lock = False
                    sett.times.lock_t = 0

                    if not use_pi_camera:
                        if sett.switch.is_disabled:
                            if not sdt.is_alive():
                                ca = cv2.VideoCapture(camera_index)
                                ca.set(cv2.CAP_PROP_FRAME_WIDTH, sett.lists.resolution[0])
                                ca.set(cv2.CAP_PROP_FRAME_HEIGHT, sett.lists.resolution[1])
                                sdt = Thread(target=start_delay_thread, daemon=True)
                                sdt.start()
                                green_led_d = Thread(target=green_led_thread, args=((1.5,),))
                                green_led_d.daemon = True
                                green_led_d.start()
                                red_led_d = Thread(target=red_led_thread, args=((3,),))
                                red_led_d.daemon = True
                                red_led_d.start()
                                
                        else:
                            sett.switch.is_disabled = True
                            time.sleep(0.1)
                            ca.release()
                            
                            red_led_d = Thread(target=red_led_thread, args=((1.5,),))
                            red_led_d.daemon = True
                            red_led_d.start()
                            green_led_d = Thread(target=green_led_thread, args=((3,),))
                            green_led_d.daemon = True
                            green_led_d.start()
                    else:
                        if sett.switch.is_disabled:
                            if not sdt.is_alive():
                                sdt = Thread(target=start_delay_thread, daemon=True)
                                sdt.start()
                                green_led_d = Thread(target=green_led_thread, args=((1.5,),))
                                green_led_d.daemon = True
                                green_led_d.start()
                                red_led_d = Thread(target=red_led_thread, args=((3,),))
                                red_led_d.daemon = True
                                red_led_d.start()
                                
                        else:
                            sett.switch.is_disabled = True
                            time.sleep(0.01)
                            red_led_d = Thread(target=red_led_thread, args=((1.5,),))
                            red_led_d.daemon = True
                            red_led_d.start()
                            green_led_d = Thread(target=green_led_thread, args=((3,),))
                            green_led_d.daemon = True
                            green_led_d.start()


                elif sett.lists.after_pin == ['*']:
                    sett.lists.b_list = []
                    sett.lists.after_pin = []
                    sett.switch.pin_correct = False
                    sett.switch.lock = False
                    sett.times.lock_t = 0
                    sett.switch.stop_check_mode = False
                    chm = Thread(target=check_mode, daemon=True)
                    chm.start()

                elif sett.lists.after_pin == ['-']:
                    sett.lists.b_list = []
                    sett.lists.after_pin = []
                    sett.switch.pin_correct = False
                    sett.switch.lock = False
                    sett.times.lock_t = 0
                    red_led_d = Thread(target=red_led_thread, args=((0.23, 0.23, 0.23, 0.23, 0.23, 0.66, 1.5),))
                    red_led_d.daemon = True
                    red_led_d.start()
                    green_led_d = Thread(target=green_led_thread, args=((0.0, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.43, 1.5),))
                    green_led_d.daemon = True
                    green_led_d.start()
                    sd = Thread(target=shutdown)
                    sd.daemon = True
                    sd.start()

                elif sett.lists.after_pin == ['+']:
                    sett.lists.b_list = []
                    sett.lists.after_pin = []
                    sett.switch.pin_correct = False
                    sett.switch.lock = False
                    sett.times.lock_t = 0
                    red_led_d = Thread(target=red_led_thread, args=((0.0, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.43, 0.5, 0.5, 0.5),))
                    red_led_d.daemon = True
                    red_led_d.start()
                    green_led_d = Thread(target=green_led_thread, args=((0.23, 0.23, 0.23, 0.23, 0.23, 0.66, 0.5, 0.5, 0.5),))
                    green_led_d.daemon = True
                    green_led_d.start()
                    rb = Thread(target=reboot)
                    rb.daemon = True
                    rb.start()

                elif sett.lists.after_pin == ['enter']:
                    sett.lists.b_list = []
                    sett.lists.after_pin = []
                    sett.switch.lock = False
                    sett.times.lock_t = 0
                    sett.switch.in_option = True
                    sett.switch.set_d = True

        # If pin is incorrect
        if sett.lists.b_list != sett.lists.pin[:len(sett.lists.b_list)]:
            pcrlt = Thread(target=red_led_thread, args=((0.3, 0.3),))
            pcrlt.daemon = True
            pcrlt.start()
            # Log in the clips folder a txt file when a disable attempt fails
            date_ = f"{sett.dates.yr}-{sett.dates.mo}-{sett.dates.da}  {sett.dates.hr}:{sett.dates.mi}:" \
                   f"{sett.dates.se}"
            sett.nums.fa_n += 1
            sett.nums.fa_num += 1
            fa = open(rc_dir + f"/Clips/failed_pin_logg.txt", "a")
            fa.write(f'PIN attempt failed in mode: {sett.nums.mode}, on run: {sett.dates._sdate}, at time: {date_}\n')
            fa.close()

            if sett.nums.fa_n >= sett.nums.allowable_pin_attempts:
                sett.times.lock_t = time.time() + sett.times.failed_pin_lock
                sett.switch.lock = True
                sett.nums.fa_n = 0

            sett.lists.b_list = []
            sett.lists.after_pin = []
            sett.switch.in_option = False
            sett.switch.pin_correct = False
            sett.dates.set_date_list = []
            sett.switch.set_d = False

    ############
    root = Tk()

    root.geometry("180x40+-8+-8")
    root.title("Key Listener")
    root.bind("<KeyRelease>", key_up)

    s = open(rc_dir + "/support/comm.txt", "r")       # taken out for windows testing
    sett.times.start = float(s.readline())
    s.close()
    m = 60

    ran = random.randint(10000, 99000)

    sett.dates._sdate = f"{sett.dates.yr:04}-{sett.dates.mo:02}-{sett.dates.da:02}-{sett.dates.hr:02}-{sett.dates.mi:02}-{sett.dates.se:02}"
    sett.dates.sdate = rc_dir + "/Clips/" + sett.dates._sdate + "_" + str(ran)
    run(['mkdir', sett.dates.sdate]) 

    # Action 1 pin is 12, Action 2 is 16, etc
    action1 = Thread(target=runAction, args=(a1h, a1o, 12))
    action2 = Thread(target=runAction, args=(a2h, a2o, 16))
    action3 = Thread(target=runAction, args=(a3h, a3o, 20))
    action4 = Thread(target=runAction, args=(a4h, a4o, 21))
    action5 = Thread(target=runAction, args=(a5h, a5o, 23))   # pins 0-8 are HIGH by default
    action6 = Thread(target=runAction, args=(a6h, a6o, 24))
    action7 = Thread(target=runAction, args=(a7h, a7o, 13))
    action8 = Thread(target=runAction, args=(a8h, a8o, 19))

    if sett.switch.play == True:
        t_audio = Thread(target=play_audio, args=(audio, delay_audio))

    fourcc = cv2.VideoWriter_fourcc(* "XVID")
    det = 0

    if use_pi_camera == False:

        ca = cv2.VideoCapture(camera_index)
        
        ca.set(cv2.CAP_PROP_FRAME_WIDTH, sett.lists.resolution[0])
        ca.set(cv2.CAP_PROP_FRAME_HEIGHT, sett.lists.resolution[1])
        
        try:
            real_width = int(ca.get(cv2.CAP_PROP_FRAME_WIDTH))
            real_height = int(ca.get(cv2.CAP_PROP_FRAME_HEIGHT))
        except:
            real_width = int(ca.get(cv2.cv.CAP_PROP_FRAME_WIDTH))
            real_height = int(ca.get(cv2.cv.CAP_PROP_FRAME_HEIGHT))
            
        text_w = int(real_width * 0.125)
        text_h = real_height - 20
    
        aoi_used = False
        p_list = []

        if len(pts) != 0:

            pts = list(map(float, pts))
            
            for idx, i in enumerate(pts):
                if idx % 4 == 0:
                    p_list.append([int(pts[idx] * real_height), int(pts[idx + 1] * real_height), int(pts[idx + 2] * real_width), int(pts[idx + 3] * real_width)])
            compiled_overlay = np.zeros(shape=(real_height, real_width, 1))  # gray img
            compiled_overlay = compiled_overlay + 255
            compiled_overlay = np.uint8(compiled_overlay)
            for i in p_list:
                compiled_overlay[i[0]:i[1], i[2]:i[3]] = 0

            aoi_used = True

        time.sleep(2)   # Camera sensor warm up
        # red led 30s to enabled warning
        for_t = int(sett.times.start_delay)
        expo = np.linspace(2, 0, for_t)
        surlt = Thread(target=red_led_thread, args=(expo,))
        surlt.daemon = True
        surlt.start()
        
        # Pause for start delay without causing buffer to build up
        tm = time.time()
        while time.time() < tm + sett.times.start_delay:
            root.update()
            _, frame1 = ca.read()
            _, frame2 = ca.read() 


        while True:
            root.update()

            # Date/time calculation, without using system time (may lose accuracy over time)
            root_sec = int(time.time() - sett.times.start)
            root_mi = root_sec // 60
            sett.dates.mi = root_mi % 60
            sett.dates.se = int(root_sec % 60)
            if root_mi >= m:
                sett.dates.hr += 1
                m += 60
                sett.dates.mi = 0
                if sett.dates.hr >= 24:
                    sett.dates.hr = 0
                    sett.dates.da += 1
                    if sett.dates.mo == 1 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 2 and sett.dates.da > 28:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 3 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 4 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 5 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 6 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 7 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 8 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 9 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 10 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 11 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 12 and sett.dates.da > 31:
                        sett.dates.mo = 1
                        sett.dates.da = 1
                        sett.dates.yr += 1


            if sett.switch.ex == True:
                break

            if sett.switch.is_disabled:
                _, f_ = ca.read()
                continue

            ret, frame1 = ca.read()          # ret is retrieve is a variable for to bool that .read() returns
            time.sleep(0.01)  #@ No need for all the copies using sleep has same effect
            ret, frame2 = ca.read()

            # xx This is night vision helps detect in low light, though kinda detects too much where there's big light diff
            # xx only helps a bit in the dark, no longer seems to cause false detects in high light diff
            # frame1[:, :, 1] = np.where(frame1[:, :, 1] < 20, cv2.multiply(frame1[:, :, 1], 2), frame1[:, :, 1])
            # frame2[:, :, 1] = np.where(frame2[:, :, 1] < 20, cv2.multiply(frame2[:, :, 1], 2), frame1[:, :, 1])
            
            # Make thres adjust to highest light pixel, stops false dets in hight light areas,
            # and enables better motion det at lower light.
            npmax = np.max(frame1)
            npmax = npmax / 255
            th = 22 * npmax + motion_sens   # or up to 4   # good
            # th = 12 * npmax + 1  # or up to 4
            th = round(th, 0)

            if ret == True:
                diff = cv2.absdiff(frame1, frame2)
                gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
                if aoi_used == True:
                    gray = cv2.subtract(gray, compiled_overlay)

                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)

                erode = cv2.erode(thresh, None, iterations=2)
                dilated = cv2.dilate(erode, None, iterations=2)  # imp threshold chooses what color value range to include
                contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    if cv2.contourArea(c) < motion_area:  # imp A smaller number here detects smaller objects moving, was orginally set at 5000, does it take moe processor power?
                        continue
                    det = 1

                if det == 1:
                    
                    det = 0

                    fdate = f"{sett.dates.yr:04}-{sett.dates.mo:02}-{sett.dates.da:02}-{sett.dates.hr:02}-{sett.dates.mi:02}-" \
                            f"{sett.dates.se:02}"

                    # Action 1 pin is 16, act 2 is 12
                    if sett.nums.mode != 1 and not action1.is_alive() and not action2.is_alive() and not action3.is_alive() \
                            and not action4.is_alive() and not action5.is_alive() and not action6.is_alive() and not \
                            action7.is_alive() and not action8.is_alive():
                        action1 = Thread(target=runAction, args=(a1h, a1o, 12))
                        action1.daemon = True
                        action1.start()
                        action2 = Thread(target=runAction, args=(a2h, a2o, 16))   
                        action2.daemon = True
                        action2.start()
                        action3 = Thread(target=runAction, args=(a3h, a3o, 20))    
                        action3.daemon = True
                        action3.start()
                        action4 = Thread(target=runAction, args=(a4h, a4o, 21))    
                        action4.daemon = True
                        action4.start()
                        action5 = Thread(target=runAction, args=(a5h, a5o, 23))    
                        action5.daemon = True
                        action5.start()
                        action6 = Thread(target=runAction, args=(a6h, a6o, 24))   
                        action6.daemon = True
                        action6.start()
                        action7 = Thread(target=runAction, args=(a7h, a7o, 13))   
                        action7.daemon = True
                        action7.start()
                        action8 = Thread(target=runAction, args=(a8h, a8o, 19))    
                        action8.daemon = True
                        action8.start()

                        if sett.switch.play == True and sett.switch.is_playing == False:
                            t_audio = Thread(target=play_audio, args=(audio, delay_audio))
                            t_audio.daemon = True
                            t_audio.start()

                    if sett.nums.mode != 3:
                        clip_tt = time.time() + clip_time    # when det records for this many seconds
                        sett.nums.out_num += 1

                        if clip_time > 3:
                            out = cv2.VideoWriter(sett.dates.sdate + "/" + str(sett.nums.out_num) + '_' + fdate + '.avi', fourcc,
                                                  fps, (real_width, real_height))
                        else:
                            ret, picture = ca.read()  # incase clip time is 0.9s gets 1st img instead of last

                        while True:

                            date = f"{sett.dates.yr:04}-{sett.dates.mo:02}-{sett.dates.da:02}  {sett.dates.hr:02}:{sett.dates.mi:02}:" \
                                   f"{sett.dates.se:02}"

                            if sett.switch.ex == True:
                                # exi()
                                break

                            # Date/time calculation, without using system time (may lose accuracy over time)
                            root_sec = int(time.time() - sett.times.start)
                            root_mi = root_sec // 60
                            sett.dates.mi = root_mi % 60
                            sett.dates.se = int(root_sec % 60)
                            if root_mi >= m:
                                sett.dates.hr += 1
                                m += 60
                                sett.dates.mi = 0
                                if sett.dates.hr >= 24:
                                    sett.dates.hr = 0
                                    sett.dates.da += 1
                                    if sett.dates.mo == 1 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 2 and sett.dates.da > 28:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 3 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 4 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 5 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 6 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 7 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 8 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 9 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 10 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 11 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 12 and sett.dates.da > 31:
                                        sett.dates.mo = 1
                                        sett.dates.da = 1
                                        sett.dates.yr += 1


                            root.update()
                            
                            if clip_time > 3:
                                ret, frame5 = ca.read()
                                if sett.switch.draw_aoi:
                                    for i in p_list:
                                        cv2.rectangle(frame1, (i[2], i[0]), (i[3], i[1]), (0, 255, 0), 1)
                                cv2.putText(frame5, date, (text_w, text_h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 230), 2)
                                out.write(frame5)
                                if sett.switch.is_disabled:

                                    out.release()
                                    break
                            else:
                                r_, f_ = ca.read()      # prevent frames from accumulating

                            if clip_tt < time.time():
                                if clip_time > 3:
                                    out.release()  # Stop the writting/saving
                                else:
                                    # Test aoi pts
                                    if sett.switch.draw_aoi:
                                        for i in p_list:
                                            cv2.rectangle(picture, (i[2], i[0]), (i[3], i[1]), (0, 255, 0), 1)
                                    cv2.putText(picture, f'{str(sett.nums.out_num)}   {date}', (text_w, text_h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 230), 2)
                                    cv2.imwrite(sett.dates.sdate + "/" + str(sett.nums.out_num) + '_' + fdate + '.jpg', picture)
                                break
            else:
                break



    else:
        # -- Pi Cam Start ---
        
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        
        # Working rec 6s clips when clip time set to 5s
        # Seems like still got same fram rate/ clip time issuse
        
        # Higher fps makes clip shorter
        # is close to various clip times if fps is low (10), maybe 1s shorter
        # even at 24 fps, but 45 fps messes up, try on zero with low fps
        
        camera = PiCamera()
        camera.resolution = sett.lists.resolution
        
        real_w = camera.resolution.pad().width
        real_h = camera.resolution.pad().height
        text_w = int(real_w * 0.125)
        text_h = real_h - 20
        
        camera.framerate = fps
        
        if sett.strings.exposure_mode != 'default':
            camera.exposure_mode = sett.strings.exposure_mode
        if sett.strings.sensor_mode != 'default':
            camera.sensor_mode = sett.strings.sensor_mode
        if sett.strings.awb_mode != 'default':
            camera.awb_mode = sett.strings.awb_mode
        if sett.nums.brightness != 'default':
            camera.brightness = sett.nums.brightness
        if sett.nums.contrast != 'default':
            camera.contrast = sett.nums.contrast
        if sett.nums.iso != 'default':
            camera.iso = sett.nums.iso
        if sett.nums.shutter_speed != 'default':
            camera.shutter_speed = sett.nums.shutter_speed
        
        rawCapture = PiRGBArray(camera, size=(real_w, real_h))
        
        aoi_used = False
        p_list = []
        if len(pts) != 0:

            pts = list(map(float, pts))
            
            for idx, i in enumerate(pts):
                if idx % 4 == 0:
                    p_list.append([int(pts[idx] * real_h), int(pts[idx + 1] * real_h), int(pts[idx + 2] * real_w), int(pts[idx + 3] * real_w)])
            compiled_overlay = np.zeros(shape=(real_h, real_w, 1))  # gray img
            compiled_overlay = compiled_overlay + 255
            compiled_overlay = np.uint8(compiled_overlay)
            for i in p_list:
                # maybe out of range if overlay is captured on different res
                compiled_overlay[i[0]:i[1], i[2]:i[3]] = 0 

            aoi_used = True

        time.sleep(2)   # Camera sensor warm up
        for_t = int(sett.times.start_delay)
        expo = np.linspace(2, 0, for_t)
        surlt = Thread(target=red_led_thread, args=(expo,))
        surlt.daemon = True
        surlt.start()

        tm = time.time()
        while time.time() < tm + sett.times.start_delay:
            root.update()

        cnt = 0
        
        pi_cap = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)

        for frame in pi_cap:
            
            root.update() 

            # Date/time calculation, without using system time (may lose accuracy over time)
            root_sec = int(time.time() - sett.times.start)
            root_mi = root_sec // 60
            sett.dates.mi = root_mi % 60
            sett.dates.se = int(root_sec % 60)
            if root_mi >= m:
                sett.dates.hr += 1
                m += 60
                sett.dates.mi = 0
                if sett.dates.hr >= 24:
                    sett.dates.hr = 0
                    sett.dates.da += 1
                    if sett.dates.mo == 1 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 2 and sett.dates.da > 28:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 3 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 4 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 5 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 6 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 7 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 8 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 9 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 10 and sett.dates.da > 31:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 11 and sett.dates.da > 30:
                        sett.dates.mo += 1
                        sett.dates.da = 1
                    if sett.dates.mo == 12 and sett.dates.da > 31:
                        sett.dates.mo = 1
                        sett.dates.da = 1
                        sett.dates.yr += 1

            if sett.switch.ex == True:
                break

            if sett.switch.is_disabled:         # todo test on pi   also put in 2nd loop as break
                rawCapture.truncate(0)
                continue

            frame1 = frame.array
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            # xx This is night vision helps detect in low light, though kinda detects too much where there's big light diff
            # xx only helps a bit in the dark, no longer seems to cause false detects in high light diff
            # frame1[:, :, 1] = np.where(frame1[:, :, 1] < 20, cv2.multiply(frame1[:, :, 1], 2), frame1[:, :, 1])
            # frame2[:, :, 1] = np.where(frame2[:, :, 1] < 20, cv2.multiply(frame2[:, :, 1], 2), frame1[:, :, 1])

            npmax = np.max(frame1)
            npmax = npmax / 255
            th = 22 * npmax + motion_sens   # or up to 4   # good
            # th = 12 * npmax + 1  # or up to 4
            th = round(th, 0)

            if cnt == 0:
                cnt = 1
                frame2 = frame1

            if cnt == 1:
                diff = cv2.absdiff(frame1, frame2)

                gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
                
                if aoi_used == True:
                    gray = cv2.subtract(gray, compiled_overlay)
                
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)

                # # --- Uncomment for Contours ----
                erode = cv2.erode(thresh, None, iterations=2)
                dilated = cv2.dilate(erode, None, iterations=2)
                contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    if cv2.contourArea(c) < motion_area:  # imp A smaller number here detects smaller objects moving
                        continue
                    det = 1
                    
                frame2 = frame1

                if det == 1:
                    det = 0

                    fdate = f"{sett.dates.yr:04}-{sett.dates.mo:02}-{sett.dates.da:02}-{sett.dates.hr:02}-{sett.dates.mi:02}-" \
                                   f"{sett.dates.se:02}"

                    if sett.nums.mode != 1 and not action1.is_alive() and not action2.is_alive() and not action3.is_alive() \
                            and not action4.is_alive() and not action5.is_alive() and not action6.is_alive() and not \
                            action7.is_alive() and not action8.is_alive():
                        action1 = Thread(target=runAction, args=(a1h, a1o, 12))
                        action1.daemon = True
                        action1.start()
                        action2 = Thread(target=runAction, args=(a2h, a2o, 16))   
                        action2.daemon = True
                        action2.start()
                        action3 = Thread(target=runAction, args=(a3h, a3o, 20))    
                        action3.daemon = True
                        action3.start()
                        action4 = Thread(target=runAction, args=(a4h, a4o, 21))    
                        action4.daemon = True
                        action4.start()
                        action5 = Thread(target=runAction, args=(a5h, a5o, 23))    
                        action5.daemon = True
                        action5.start()
                        action6 = Thread(target=runAction, args=(a6h, a6o, 24))   
                        action6.daemon = True
                        action6.start()
                        action7 = Thread(target=runAction, args=(a7h, a7o, 13))   
                        action7.daemon = True
                        action7.start()
                        action8 = Thread(target=runAction, args=(a8h, a8o, 19))    
                        action8.daemon = True
                        action8.start()

                        if sett.switch.play == True and sett.switch.is_playing == False:
                            t_audio = Thread(target=play_audio, args=(audio, delay_audio))
                            t_audio.daemon = True
                            t_audio.start()

                    if sett.nums.mode != 3:
                        clip_tt = time.time() + clip_time    # when det records for this many seconds
                        sett.nums.out_num += 1

                        if clip_time > 3:
                            out = cv2.VideoWriter(sett.dates.sdate + "/" + str(sett.nums.out_num) + '_' + fdate + '.avi', fourcc, fps, (real_w, real_h))

        #                 for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                        for frame in pi_cap:
                            frame5 = frame.array
                            rawCapture.truncate(0)
                            
                            date = f"{sett.dates.yr:04}-{sett.dates.mo:02}-{sett.dates.da:02}  {sett.dates.hr:02}:{sett.dates.mi:02}:" \
                                   f"{sett.dates.se:02}"
                            
                            if sett.switch.ex == True:
                                break

                            # Date/time calculation, without using system time (may lose accuracy over time)
                            root_sec = int(time.time() - sett.times.start)
                            root_mi = root_sec // 60
                            sett.dates.mi = root_mi % 60
                            sett.dates.se = int(root_sec % 60)
                            if root_mi >= m:
                                sett.dates.hr += 1
                                m += 60
                                sett.dates.mi = 0
                                if sett.dates.hr >= 24:
                                    sett.dates.hr = 0
                                    sett.dates.da += 1
                                    if sett.dates.mo == 1 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 2 and sett.dates.da > 28:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 3 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 4 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 5 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 6 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 7 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 8 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 9 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 10 and sett.dates.da > 31:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 11 and sett.dates.da > 30:
                                        sett.dates.mo += 1
                                        sett.dates.da = 1
                                    if sett.dates.mo == 12 and sett.dates.da > 31:
                                        sett.dates.mo = 1
                                        sett.dates.da = 1
                                        sett.dates.yr += 1

                            root.update() 

                            if clip_time > 3:
                                if sett.switch.draw_aoi:
                                    for i in p_list:
                                        cv2.rectangle(frame1, (i[2], i[0]), (i[3], i[1]), (0, 255, 0), 1)
                                cv2.putText(frame5, date, (text_w, text_h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 230), 2)
                                out.write(frame5)

                                if sett.switch.is_disabled:
                                    out.release()
                                    break
    #

                            if clip_tt < time.time():
                                cnt = 0
                                if clip_time > 3:
                                    out.release()  # Stop the writting/saving
                                else:
                                    cv2.putText(frame1, f'{str(sett.nums.out_num)}   {date}', (text_w, text_h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 230), 2)
                                    # Test aoi pts
                                    if sett.switch.draw_aoi:
                                        for i in p_list:
                                            cv2.rectangle(frame1, (i[2], i[0]), (i[3], i[1]), (0, 255, 0), 1)
                                    cv2.imwrite(sett.dates.sdate + "/" + str(sett.nums.out_num) + '_' + fdate + '.jpg', frame1)
                                break


    if not use_pi_camera:
        ca.release()
    time.sleep(5)
    GPIO.cleanup()
    root.destroy()
        

except Exception as e:
    er = open(rc_dir + f"/Clips/error_logg.txt", "a")
    er.write(f'Rover_Cam_KI/modes/run_modes.py has failed with exception: {e}\n')
    er.close()
    
    GPIO.cleanup()
