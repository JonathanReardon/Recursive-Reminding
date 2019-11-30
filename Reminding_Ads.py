#!/usr/bin/env python

#import psychopy
from psychopy import core, visual, gui, event, sound
#from psychopy.visual import vlc
from psychopy import tools
from psychopy.data import getDateStr
from psychopy import info
import random, csv
import os
import time
from psychopy.constants import (PLAYING, PAUSED) 

# create window and set mouse visibility
win = visual.Window([1920, 1080], color=("black"), colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', screen=1)
win.mouseVisible = True

# Open a writeable data file for our output .csv
current_time = getDateStr()
dataFile = open(current_time +'.csv', 'w') 
writer = csv.writer(dataFile)
writer.writerow(["participant number", "video name"])

# minimise window in order to take user info
win.fullscr = False #not sure if this is necessary
win.winHandle.set_fullscreen(False)
win.winHandle.minimize()
win.flip()

# take user info
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo)
if dlg.OK == False:
    core.quit()
    
# maximise window to continue
win.winHandle.maximize()
win.winHandle.activate()
win.fullscr=True
win.winHandle.set_fullscreen(True)
win.flip()

# set ad video directory
ads   = r"C:\Users\Channel 4 Project\Documents\C4_pilot\Reminding\Trialfolders\Advert"
ad_videos = sorted(os.listdir(ads))
#random.shuffle(ad_videos)

# write participant code and video stim order to file before we begin exp
for counter in range(len(ad_videos)):
    dataFile.write('%s, %s\n'%(expInfo.get('participant'), ad_videos[counter]))
dataFile.close()

# function to make and display intro stimuli and wait for user keypress to continue
def intro():
    intro_stim = visual.TextStim(win, text=r"Watch as you would at home", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)

    while not event.getKeys():
        event.Mouse(visible=False)
        intro_stim.draw()
        win.flip()
        
# create experiment stimuli
question_stim = visual.TextStim(win, text=r"Did the object repeat? 'A' key = no, 'L' key = yes", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)
verbal = visual.TextStim(win, text=r"Tell the experimenter what ad, spacebar to continue", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)
 
 # function to make and display outro stimuli and wait for keypress to continue
def outro():
    outro_stim = visual.TextStim(win, text=r"Thank you", pos=(0,0), depth=0, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True, wrapWidth=None)

    while not event.getKeys():
        event.Mouse(visible=False)
        outro_stim.draw()
        win.flip() 
        
# display outro stim
intro()

for counter in range(len(ad_videos)):
    # create current video to display
    display = [visual.MovieStim3(win, ads + "/" + stim, size=[1920, 1080]) for stim in ad_videos[counter:counter + 1]]

    print(ad_videos[counter])
    
    win.flip()
    core.wait(1)

    shouldflip = display[0].play()
        
    # while video is not finished, play it
    while display[0].status != visual.FINISHED:
        shouldflip = display[0].draw()
        win.flip()
    # check for keypress to quit 
    allKeys = event.getKeys(keyList = ('q'))
    for thisKey in allKeys:
        if thisKey == 'q':
            dataFile.close()
            win.close()
            core.quit()

# display outro stim         
outro()
        
win.close()
core.quit()
