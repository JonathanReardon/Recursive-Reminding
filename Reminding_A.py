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

# set programme video directories
progs = r"C:\Users\Channel 4 Project\Documents\C4_pilot\Reminding\Trialfolders\A"
prog_videos = sorted(os.listdir(progs))
random.shuffle(prog_videos)

# minimise main window to take user info (separate gui)
win.fullscr = False         
win.winHandle.set_fullscreen(False)
win.winHandle.minimize()
win.flip()

# take user info
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo)
if dlg.OK == False:
    core.quit()
    
# maximise main window to continue
win.winHandle.maximize()
win.winHandle.activate()
win.fullscr=True
win.winHandle.set_fullscreen(True)
win.flip()

# a function to make and display intro stim, user keypress to continue
def intro():
    intro_stim = visual.TextStim(win, text=r"Watch as you would at home", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True)

    while not event.getKeys():
        event.Mouse(visible=False)
        intro_stim.draw()
        win.flip() 
        
# create question stimuli
question_stim = visual.TextStim(win, text=r"WAS THE PRODUCT CATEGORY IN THIS CLIP REPEATED IN A PREVIOUS ADVERT?", pos=(0,2), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
A = visual.TextStim(win, text=r"A=NO", pos=(-10,-2), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
L = visual.TextStim(win, text=r"L=YES", pos=(10, -2), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
verbal = visual.TextStim(win, text=r"Please note down the number (shown in red) and what advert the object was repeated in.", pos=(0,4), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
spacebar = visual.TextStim(win, text=r"SPACEBAR TO CONTINUE", pos=(0, -2), depth=0, wrapWidth=None, 
            color=("green"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
number = visual.TextStim(win, text=r"", pos=(0,-5), depth=0, wrapWidth=None, 
            color=("red"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=2, antialias=True)  
 
# a function to make and display outro stim, user keypress to continue   
def outro():
    outro_stim = visual.TextStim(win, text=r"Thank you", pos=(0,0), depth=0, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True, wrapWidth=None)

    while not event.getKeys():
        event.Mouse(visible=False)
        outro_stim.draw()
        win.flip() 

# display intro stim  
intro()

for counter in range(len(prog_videos)):
    # create current video stim to display
    display = [visual.MovieStim3(win, progs + "/" + stim, size=[1920, 1080]) for stim in prog_videos[counter:counter + 1]]

    print(prog_videos[counter])
    # set current video name
    display[0].name = prog_videos[counter]

    shouldflip = display[0].play()
    # while video is not finished, play it
    while display[0].status != visual.FINISHED:
        shouldflip = display[0].draw()
        win.flip()
    
    # brief pause
    time.sleep(0.001)
    # set stim name
    name = display[0].name
    #print(name)
    
    # clear keyboard events
    event.clearEvents()

    # display question stimuli
    question=True
    while question==True:
        
        # display question
        question_stim.draw()
        A.draw()
        L.draw()
        win.flip()
        
        # keyboard presses to check for
        question_keys = event.getKeys(keyList = ('a','l', 'escape'))
        
        for thisKey in question_keys:
            # if 'escape' key is pressed, close datafile (to save it) and quit
            if thisKey == "escape":
                dataFile.close()
                win.close()
                core.quit()
            # take keypress and set accuracy accordingly (keylog)
            if thisKey == "a":
                if display[0].name == "T":
                    keylog = str(0)
                elif display[0].name != "T":
                    keylog = str(1)
                
                question=False
            if thisKey == "l":
                response = True
                
                # take keypress and set accuracy accordingly (keylog)
                if display[0].name == "T":
                    keylog = str(1)
                elif display[0].name != "T":
                    keylog = str(0)

                numer.text=str(list_index[counter])
                event.clearEvents()
                
                while response == True:
                    number.draw()
                    verbal.draw()
                    spacebar.draw()
                    win.flip()
                    
                    # keyboard presses to check for
                    verbal_keys = event.getKeys(keyList = ('space', 'escape'))
                    if "escape" in verbal_keys:
                        dataFile.close()
                        win.close()
                        core.quit()
                    elif "space" in verbal_keys:
                        question=False
                        response=False

    dataFile.write('%s,%s,%s,%s,%s\n'%(expInfo.get('participant'), list_index[counter], display[0], prog_videos[counter], keylog))
    #print('%s,%s,%s,%s,%s\n'%(expInfo.get('participant'), list_index[counter], display[0], prog_videos[counter], keylog))
                                   
    event.clearEvents()
    win.flip()
    core.wait(1)

# display outro stim      
outro()
        
win.close()
core.quit()
