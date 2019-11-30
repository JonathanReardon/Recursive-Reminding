#!/usr/bin/env python

# import libraries
from psychopy import visual, core, gui, event
from psychopy.data import getDateStr
import random, csv
import os

# create window and set mouse cursor visibililty off
win = visual.Window([1200,800], color=("black"), colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', fullscr=True)
win.mouseVisible = False

# minimizes window so that we can take participant information (through gui dialog)
win.fullscr = False
win.winHandle.set_fullscreen(False)
win.winHandle.minimize()
win.flip()

# Participant naming 
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo)
if dlg.OK == False:
    core.quit()
    
# maximise window again ready to begin
win.winHandle.maximize()
win.winHandle.activate()
win.fullscr=True
win.winHandle.set_fullscreen(True)
win.flip()

# create text lists
TARGETS = ["Pasta",               "Coffee",           "Prawns",                    "Paint",                    "Pre-prepared food delivery",
          "Cake",                "Tablet",           "Vacuum cleaner",            "Diamond ring",             "Hair clippers",
          "Dating Site",         "Blender",          "Phone",                     "Pizza",                    "Washing Machine",
          "Headphones",          "Sausages",         "Fitness Watch",             "Tea",                      "Chinese sauces",
          "Indian curry sauces", "Beer",             "Postal delivery service",   "Bread",                    "Lasagne",
          "Porridge",            "Pie",              "Chocolate",                 "Nappies",                  "Milk",
          "Condoms",             "Oven",             "Jigsaw puzzle",             "Camera",                   "Suits",
          "Toothbrush",          "Greetings card",   "Shoes",                     "Video game",               "Boiler"]
                   
CONTROLS = ["Sofa",                "Swimwear",         "Pen",                       "Wetsuit",                  "Glasses", 
            "Crisps",              "Radio station",    "Rucksack",                  "Car",                      "Dog food",
            "Cider",               "TV",               "Business card printing",    "Home security system",     "Lipstick",
            "Lamb",                "Ice cream",        "Fridge",                    "Wine",                     "Orange juice",
            "Conservatory",        "Bleach",           "BBQ",                       "Chicken Breast",           "Search Engine",
            "Kebab",               "Conditioner",      "Streaming service",         "High heels",               "Film",
            "Fan",                 "Deodorant",        "Fabric softener",           "Instant noodle",           "Tissues",
            "Smoking patches",     "Peanut Butter",    "Cereal bar",                "Bottled water",            "Fish fingers"]

word_list = ["Pasta",               "Coffee",           "Prawns",                    "Paint",                    "Pre-prepared food delivery",
             "Cake",                "Tablet",           "Vacuum cleaner",            "Diamond ring",             "Hair clippers",
             "Dating Site",         "Blender",          "Phone",                     "Pizza",                    "Washing Machine",
             "Headphones",          "Sausages",         "Fitness Watch",             "Tea",                      "Chinese sauces",
             "Indian curry sauces", "Beer",             "Postal delivery service",   "Bread",                    "Lasagne",
             "Porridge",            "Pie",              "Chocolate",                 "Nappies",                  "Milk",
             "Condoms",             "Oven",             "Jigsaw puzzle",             "Camera",                   "Suits",
             "Toothbrush",          "Greetings card",   "Shoes",                     "Video game",               "Boiler",
             "Sofa",                "Swimwear",         "Pen",                       "Wetsuit",                  "Glasses", 
             "Crisps",              "Radio station",    "Rucksack",                  "Car",                      "Dog food",
             "Cider",               "TV",               "Business card printing",    "Home security system",     "Lipstick",
             "Lamb",                "Ice cream",        "Fridge",                    "Wine",                     "Orange juice",
             "Conservatory",        "Bleach",           "BBQ",                       "Chicken Breast",           "Search Engine",
             "Kebab",               "Conditioner",      "Streaming service",         "High heels",               "Film",
             "Fan",                 "Deodorant",        "Fabric softener",           "Instant noodle",           "Tissues",
             "Smoking patches",     "Peanut Butter",    "Cereal bar",                "Bottled water",            "Fish fingers"]

# shuffle word list in alignment with index order list
list_index = range(1,len(word_list), 1)
temp = list(zip(word_list, list_index))
random.shuffle(temp)
word_list, list_index = map(list, zip(*temp))

# function to make intro text stim and wait for user keypress before moving on
def intro():
    
    intro_stim = visual.TextStim(win, text=r"PRESS SPACEBAR TO BEGIN", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)

    while not event.getKeys():
        event.Mouse(visible=False)
        intro_stim.draw()
        win.flip() 
        
# function to make outro text stim and wait for user keypress before moving on
def outro():
    
    outro_stim = visual.TextStim(win, text=r"THANK YOU", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
            
    outro_stim.draw()
    win.flip()
    core.wait(3)
    
    event.clearEvents()

    while not event.getKeys():
        event.Mouse(visible=False)
        outro_stim.draw()
        win.flip() 
    
# make various text stimuli
recall_stim = visual.TextStim(win, text=r"WAS THIS OBJECT IN AN", pos=(-2.3, 2.0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
advert_word = visual.TextStim(win, text=r"ADVERT?", pos=(6.1, 2.0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
a_key = visual.TextStim(win, text=r"A=NO", pos=(-7,-2), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
l_key = visual.TextStim(win, text=r"L=YES", pos=(7,-2), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
confirm_stim = visual.TextStim(win, text=r'WHAT ADVERT?', pos=(0.0, 3.0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)
spacebar_stim = visual.TextStim(win, text=r'SPACEBAR TO CONTINUE', pos=(0.0, 0.0), depth=0, wrapWidth=None, 
            color=("red"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)

# Open a writeable data file for our output .csv
current_time = getDateStr()
dataFile = open(current_time +'.csv', 'w') 
writer = csv.writer(dataFile)
writer.writerow(["word name", "keypress", "accuracy"])

# display intro 
intro()

for word in word_list:
    
    stim = visual.TextStim(win,units='norm', height = 0.1, color="white",
                           pos=(0.0, 0.0), text=word , name=str(word))
                           
    stim.draw()
    win.flip()
    core.wait(4)
    
    event.clearEvents()

    display=True
    while display==True:
        
        recall_stim.draw()
        advert_word.draw()
        
        a_key.color="white"
        l_key.color="white"
        a_key.draw()
        l_key.draw()

        allKeys = event.getKeys(keyList = ("a","l","escape"))
        for thisKey in allKeys:
            if thisKey == "a":
                a_key.color="green"
                a_key.draw()
                l_key.draw()
                recall_stim.draw()
                advert_word.draw()
                win.flip()
                core.wait(1)
                
                if stim.name in TARGETS:
                    keylog=1
                elif stim.name in CONTROLS:
                    keylog=0
                display=False
                
            elif thisKey == "l":
                l_key.color="green"
                l_key.draw()
                a_key.draw()
                recall_stim.draw()
                advert_word.draw()
                win.flip()
                core.wait(1)
                
                if stim.name in TARGETS:
                    keylog=0
                elif stim.name in CONTROLS:
                    keylog=1
                
                confirm=True
                event.clearEvents()
                while confirm==True: 
                    
                    spacebar_stim.color="red"
                    confirm_stim.draw()
                    spacebar_stim.draw()
                    number.draw()
                   
                    confirm_keys = event.getKeys("space")
                    if "space" in confirm_keys:
                        spacebar_stim.color="green"
                        spacebar_stim.draw()
                        win.flip()
                        core.wait(.5)
                        confirm=False
                    win.flip()
                    
                display=False
                
            elif thisKey == "escape":
                dataFile.close()
                win.close()
                core.quit()

        win.flip()
      
    event.clearEvents()
        
    dataFile.write('%s,%s,%s,%s,%s,%s\n'%(expInfo.get('participant'), stim.name, list_index[counter], thisKey, keylog))
    print('%s,%s,%s,%s,%s\n'%(expInfo.get('participant'), stim.name, list.index[counter], thisKey, keylog))
    core.wait(0.001)
    
outro()

dataFile.close()
win.close()
core.quit()