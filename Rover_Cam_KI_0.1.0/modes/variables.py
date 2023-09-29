
# Copyright (C) 2023 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam KI project.
# Please see the LICENSE file that should have been included as part of this package.

# Make the variables more organized, and global


class Dates:
    def __init__(self, sdate='date not set', _sdate='_sdate not set', yr=1000, mo=1, da=1,
                 hr=1, mi=1, se=1, set_date_list=[]):
        self.sdate = sdate         # from config and active settable down to se
        self.yr = yr
        self.mo = mo
        self.da = da
        self.hr = hr
        self.mi = mi
        self.se = se
        self.set_date_list = set_date_list

class Strings:
    def __init__(self, final_key="", exposure_mode="default", sensor_mode="default",
                 awb_mode="default"):
        self.final_key = final_key
        self.exposure_mode = exposure_mode     # from config
        self.sensor_mode = sensor_mode     # from config
        self.awb_mode = awb_mode     # from config

class Nums:
    def __init__(self, mode=1, fa_num=0, fa_n=0, out_num=0, allowable_pin_attempts=1,
                 brightness='default', iso='default', shutter_speed='default',
                 contrast='default'):
        self.mode = mode     # from config and active settable
        self.fa_num = fa_num
        self.fa_n = fa_n
        self.out_num = out_num
        self.allowable_pin_attempts = allowable_pin_attempts     # from config
        self.brightness = brightness     # from config
        self.iso = iso     # from config
        self.shutter_speed = shutter_speed     # from config
        self.contrast = contrast     # from config

class Lists:
    def __init__(self, b_list=[], after_pin=[], after_after=[], pin=[], resolution=()):
        self.b_list = b_list
        self.after_pin = after_pin
        self.after_after = after_after
        self.pin = pin     # from config
        self.resolution = resolution     # from config

class Times:
    def __init__(self, lock_t=0, start=0, pin_time_frame=30, pin_timer=0, failed_pin_lock=0,
                 start_delay=0):
        self.lock_t = lock_t
        self.start = start
        self.pin_time_frame = pin_time_frame  # 
        self.pin_timer = pin_timer
        self.failed_pin_lock = failed_pin_lock   # from config
        self.start_delay = start_delay   # from config
        
class Swithes:
    def __init__(self, pin_correct=False, lock=False, in_option=False, set_d=False, ex=False, stop_check_mode=False,
                 play=False, is_playing=False, is_disabled=False, select_mode=False, draw_aoi=False):
        self.pin_correct = pin_correct
        self.lock = lock
        self.in_option = in_option
        self.set_d = set_d
        self.ex = ex
        self.stop_check_mode = stop_check_mode
        self.play = play
        self.is_playing = is_playing
        self.is_disabled = is_disabled
        self.select_mode = select_mode
        self.draw_aoi = draw_aoi   # from config


dates = Dates()
strings = Strings()
nums = Nums()
lists = Lists()
times = Times()
switch = Swithes()
