#!/usr/bin/env python3

from psychopy import visual, core, gui, event
from psychopy.data import getDateStr
import random, csv
import os

clock = core.Clock()

recog_images_dir   = "/home/jon/experiments/Source_Memory/Recognition_Images/ad_images"
response_image_dir = "/home/jon/experiments/Source_Memory/Recognition_Images/response_image"

refresh_rate = 60.0
stim_dur = .1
block_wait = .1

stim_frame = stim_dur * refresh_rate
stim_frame = int(stim_frame) 

# create window and set mouse visibility
win = visual.Window([800,800], color=("black"), colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', fullscr=False)
win.mouseVisible = False

# Open a writeable data file for our output .csv
current_time = getDateStr()
dataFile = open(current_time +'.csv', 'w') 
writer = csv.writer(dataFile)
writer.writerow(["image", "ad time", "first key", "first key time", "recog image time", "second key", "second key time"])

recog_image_names = []
recog_image_list = sorted(os.listdir(recog_images_dir))

response_image_list = sorted(os.listdir(response_image_dir))

for file in recog_image_list:
    recog_image_names.append("ad_images/" + file)

recog_image_stims   = [visual.ImageStim(win, recog_images_dir + "/" + stim) for stim in recog_image_list[:]]
response_image_stim = [visual.ImageStim(win, response_image_dir + "/" + stim) for stim in response_image_list[:]]

for counter, stim in enumerate(recog_image_stims):
    stim.name = recog_image_names[counter]

# MAIN ROUTINE
for image in recog_image_stims:
    
    print(image.name)
    
    thisResp        = "-"
    keyTime         = "-"
    thisRecogResp   = "-"
    RecogkeyTime    = "-"
    stim_time       = "-"
    stim_time_Recog = "-"

    image.draw()
    win.flip()
    core.wait(block_wait)
    
    clock.reset()
    for frames in range(stim_frame):
       
        image.draw()
        win.flip()
        
        if frames == 0:
            stim_time = clock.getTime()
            print(stim_time)

        allKeys = event.getKeys(keyList = ('a','l','escape'))
        for thisKey in allKeys:

            if thisKey == 'a':
                keyTime=clock.getTime()  
                print("a: ", keyTime)
                thisResp = 1
            elif thisKey == 'l':
                keyTime=clock.getTime()
                print("l :", keyTime)
                thisResp = 0
            elif thisKey == 'escape':
                print("you quit")
                dataFile.close()
                win.close()
                core.quit()
                
        if thisResp == 1:
            print("keytime: ", keyTime)
            break
        elif thisResp == 0:
            print("ketime: ", keyTime)
            
            response_image_stim[0].draw()
            win.flip()
            core.wait(block_wait)
            
            clock.reset()
            for frame in range(stim_frame):
                
                response_image_stim[0].draw()
                win.flip()
                
                if frames == 0:
                    stim_time_Recog = clock.getTime()
                    print(stim_time_recog)
                    
                allKeys = event.getKeys(keyList = ('1','2','3', 'escape'))
                for thisKey in allKeys:

                    if thisKey == '1':
                        RecogkeyTime=clock.getTime()  
                        thisRecogResp = 1
                    elif thisKey == '2':
                        RecogkeyTime=clock.getTime()
                        thisRecogResp = 2
                    elif thisKey == '3':
                        RecogkeyTime=clock.getTime()
                        thisRecogResp = 3
                    elif thisKey == 'escape':
                        print("you quit")
                        dataFile.close()
                        win.close()
                        core.quit()
                        
                if thisRecogResp == '1' or thisRecogResp == '2' or thisRecogResp == '3':
                    print("recog key time: ", RecogKeyTime)
                    break
     
    dataFile.write('%s, %s, %s, %s, %s, %s, %s\n'%(image.name, stim_time, str(thisResp), keyTime, stim_time_Recog, str(thisRecogResp), RecogkeyTime)) #send results to datafile

dataFile.close()
win.close()
core.quit()

    
