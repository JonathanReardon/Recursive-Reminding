from psychopy import visual, core, gui, event
from psychopy.data import getDateStr
import random, csv
import os

win = visual.Window([1200,800], color=("black"), colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', fullscr=True)
win.mouseVisible = False

WORD_LIST_ORDER = ["1. Pasta", "2. Coffee", "3. Prawns", "4. Paint", "5. Pre-prepared food delivery",
                   "6. Cake", "7. Tablet", "8. Vacuum cleaner", "9. Diamond ring", "10. Hair clipper",
                   "11. Dating Site", "12. Blender", "13. Phone", "14. Pizza", "15. Washing Machine",
                   "16. Headphones", "17. Sausages", "18. Fitness Watch", "19. Tea", "20. Chinese sauces",
                   "21. Indian curry sauces", "22. Beer", "23. Postal delivery service", "24. Bread", "25. Lasagne",
                   "26. Porridge", "27. Pie", "28. Chocolate", "29. Nappies", "30. Milk",
                   "31. Condom", "32. Oven", "33. Jigsaw puzzle", "34. Camera", "35. Suits",
                   "36. Toothbrush", "37. Greetings card", "38. Shoes", "39. Video game", "40. Boiler",
                   "41. Sofa", "42. Swimwear", "43. Pen", "44. Wetsuit", "45. Glasses", 
                   "46. Crisps", "47. Radio station", "48. Rucksack", "49. Car", "50. Dog food",
                   "51. Cider", "52. TV", "53. Business card printing", "54. Home security system", "55. Lipstick",
                   "56. Lamb", "57. Ice cream", "58. Fridge", "59. Wine", "60. Orange juice"]

word_list = ["1. Pasta", "2. Coffee", "3. Prawns", "4. Paint", "5. Pre-prepared food delivery",
             "6. Cake", "7. Tablet", "8. Vacuum cleaner", "9. Diamond ring", "10. Hair clipper",
             "11. Dating Site", "12. Blender", "13. Phone", "14. Pizza", "15. Washing Machine",
             "16. Headphones", "17. Sausages", "18. Fitness Watch", "19. Tea", "20. Chinese sauces",
             "21. Indian curry sauces", "22. Beer", "23. Postal delivery service", "24. Bread", "25. Lasagne",
             "26. Porridge", "27. Pie", "28. Chocolate", "29. Nappies", "30. Milk",
             "31. Condom", "32. Oven", "33. Jigsaw puzzle", "34. Camera", "35. Suits",
             "36. Toothbrush", "37. Greetings card", "38. Shoes", "39. Video game", "40. Boiler",
             "41. Sofa", "42. Swimwear", "43. Pen", "44. Wetsuit", "45. Glasses", 
             "46. Crisps", "47. Radio station", "48. Rucksack", "49. Car", "50. Dog food",
             "51. Cider", "52. TV", "53. Business card printing", "54. Home security system", "55. Lipstick",
             "56. Lamb", "57. Ice cream", "58. Fridge", "59. Wine", "60. Orange juice"]
random.shuffle(word_list)

def intro():
    
    intro_stim = visual.TextStim(win, text=r"PRESS SPACEBAR TO BEGIN", pos=(0,0), depth=0, wrapWidth=None, 
            color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=1, antialias=True)

    while not event.getKeys():
        event.Mouse(visible=False)
        intro_stim.draw()
        win.flip() 
        
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
                
                if stim.name in WORD_LIST_ORDER[0:40]:
                    keylog=1
                else:
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
                
                if stim.name in WORD_LIST_ORDER[0:40]:
                    keylog=0
                else:
                    keylog=1
                
                confirm=True
                event.clearEvents()
                while confirm==True: 
                    
                    spacebar_stim.color="red"
                    confirm_stim.draw()
                    spacebar_stim.draw()
                   
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
        
    dataFile.write('%s,%s,%s\n'%(stim.name, thisKey, keylog))
    print('%s,%s,%s\n'%(stim.name, thisKey, keylog))
    core.wait(0.001)
    
outro()

dataFile.close()
win.close()
core.quit()