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
win = visual.Window([1920, 1080], color=("black"), colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', fullscr=True)
win.mouseVisible = True

# Open a writeable data file for our output .csv
current_time = getDateStr()
dataFile = open(current_time +'.csv', 'w') 
writer = csv.writer(dataFile)
writer.writerow(["participant number", "video name", "keypress"])

progs = r"C:\Users\Channel 4 Project\Documents\C4_pilot\Reminding\Trialfolders\A"
prog_videos   = sorted(os.listdir(progs))
random.shuffle(prog_videos)

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

def intro():
    
    intro_stim = visual.TextStim(win, text=r"Watch as you would at home", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)

    while not event.getKeys():
        event.Mouse(visible=False)
        intro_stim.draw()
        win.flip() 
        
question_stim = visual.TextStim(win, text=r"Did the object repeat? 'A' = no, 'L' = yes", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
verbal = visual.TextStim(win, text=r"Tell the experimenter what ad, spacebar to continue", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
 
        
def outro():
    outro_stim = visual.TextStim(win, text=r"Thank you", pos=(0,0), depth=0, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True, wrapWidth=None)

    while not event.getKeys():
        event.Mouse(visible=False)
        outro_stim.draw()
        win.flip() 
        
intro()

for counter in range(len(prog_videos)):
    
    display = [visual.MovieStim3(win, progs + "/" + stim, size=[1920, 1080]) for stim in prog_videos[counter:counter + 1]]

    print(prog_videos[counter])
    display[0].name = prog_videos[counter]

    shouldflip = display[0].play()
        
    while display[0].status != visual.FINISHED:
        shouldflip = display[0].draw()
        win.flip()
        
    time.sleep(0.001)
    
    event.clearEvents()

    question=True
    while question==True:
        
        question_stim.draw()
        win.flip()
        
        question_keys = event.getKeys(keyList = ('a','l', 'escape'))
        
        for thisKey in question_keys:
            if thisKey == "escape":
                dataFile.close()
                win.close()
                core.quit()
            if thisKey == "a":
                
                if display[0].name == "T":
                    keylog = str(0)
                elif display[0].name != "T":
                    keylog = str(1)
                
                question=False
            if thisKey == "l":
                response = True
                
                if display[0].name == "T":
                    keylog = str(1)
                elif display[0].name != "T":
                    keylog = str(0)
                
                while response == True:
                    verbal.draw()
                    win.flip()
                    
                    verbal_keys = event.getKeys()
                    if len(verbal_keys) > 0:
                        question=False
                        response=False

    dataFile.write('%s,%s,%s\n'%(expInfo.get('participant'), prog_videos[counter], keylog))
                        
                        
    event.clearEvents()
    win.flip()
    core.wait(1)
            
outro()
        
win.close()
core.quit()
