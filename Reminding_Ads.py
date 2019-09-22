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

win.fullscr = False           #not sure if this is necessary
win.winHandle.set_fullscreen(False)
win.winHandle.minimize()
win.flip()

# Participant naming 
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo)
if dlg.OK == False:
    core.quit()
    
win.winHandle.maximize()
win.winHandle.activate()
win.fullscr=True
win.winHandle.set_fullscreen(True)
win.flip()

ads   = r"C:\Users\Channel 4 Project\Documents\C4_pilot\Reminding\Trialfolders\Advert"
ad_videos = sorted(os.listdir(ads))
#random.shuffle(ad_videos)

for counter in range(len(ad_videos)):
    dataFile.write('%s, %s\n'%(expInfo.get('participant'), ad_videos[counter]))
dataFile.close()

def intro():
    
    intro_stim = visual.TextStim(win, text=r"Watch as you would at home", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)

    while not event.getKeys():
        event.Mouse(visible=False)
        intro_stim.draw()
        win.flip()
        
question_stim = visual.TextStim(win, text=r"Did the object repeat? 'A' key = no, 'L' key = yes", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)
verbal = visual.TextStim(win, text=r"Tell the experimenter what ad, spacebar to continue", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)
 
def outro():
    outro_stim = visual.TextStim(win, text=r"Thank you", pos=(0,0), depth=0, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True, wrapWidth=None)

    while not event.getKeys():
        event.Mouse(visible=False)
        outro_stim.draw()
        win.flip() 
        
intro()


for counter in range(len(ad_videos)):
    
    display = [visual.MovieStim3(win, ads + "/" + stim, size=[1920, 1080]) for stim in ad_videos[counter:counter + 1]]

    print(ad_videos[counter])
    
    win.flip()
    core.wait(1)

    shouldflip = display[0].play()
        
    while display[0].status != visual.FINISHED:
        shouldflip = display[0].draw()
        win.flip()
    
    allKeys = event.getKeys(keyList = ('q'))
    for thisKey in allKeys:
        if thisKey == 'q':
            dataFile.close()
            win.close()
            core.quit()
                
outro()
        
win.close()
core.quit()
