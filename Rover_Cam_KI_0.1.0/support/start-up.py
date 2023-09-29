
# Copyright (C) 2023 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam KI project.
# Please see the LICENSE file that should have been included as part of this package.


try:
    import time
    time.sleep(2)    # it sleeps for 40s in crontab

    import sys
    import os
    from subprocess import run, call
    from threading import Thread
    
    starr = time.time()   # Clock in mode files is based on this

    # To allow this start up app to run a UI key listener
    os.environ["DISPLAY"] = ":0"

    rc_dir = os.path.abspath(__file__)
    if "Run-at-start" in rc_dir:
        rc_dir = rc_dir[:-len(os.path.basename(__file__)) - 16]
    else:
        rc_dir = rc_dir[:-len(os.path.basename(__file__)) - 9]

    f = open(rc_dir + "/support/RC_config.txt", "r")
    prog = f.read().splitlines()   # gets ride of the \n at end of each element

    for i in prog:
        if i != "" and i[0:10] == "set_time =":
            st = i[10:].split()
            yr = int(st[0])  # retrieved
            mo = int(st[1])
            da = int(st[2])
            hr = int(st[3])
            mi = int(st[4])
            se = int(st[5])
    f.close()

    start = starr - (mi * 60) - se   # For Clock

    s = open(rc_dir + "/support/comm.txt", "a")
    s.truncate(0)
    s.write(str(start))
    s.close()

    def launch_file():
        run(['python3', f'{rc_dir}/modes/run_modes.py'])

    t = Thread(target=launch_file)
    t.daemon = True
    t.start()
    time.sleep(8)  # make sure launch_file() finnishs first


except:
    fa = open(rc_dir + "/FAILED-start-up.txt", "a")
    fa.write("This file was created to inform you that" +
    " in Rover Cam directory /Run-at-startup/start-up.py has failed to run.\n" +
    "Delete this file and try again. If the problem presists, try increasing the\n" +
    "the number passed into the first occurence of 'time.sleep()'\n" +
    "in the file mentioned.")
    fa.close()
