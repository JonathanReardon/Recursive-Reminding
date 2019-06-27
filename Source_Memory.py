# import necessary libraries
from psychopy import visual, core, gui, event
from psychopy.data import getDateStr
import random, csv
import os

''' for testing purposes '''
# randomise blocks/vids 
shuffle_blocks = "yes"
# set number of blocks to display 
blocks = (10)
# display image labels?
image_labels = "yes"

''' set stimulus directories '''
# target videos
target_prog_dir   = "../Target Group/prog"
target_ad_dir     = "../Target Group/ad"
# advert videos
control_prog_dir  = "../Control Group/prog"
control_ad_dir    = "../Control Group/ad"

# create window and set mouse visibility
win = visual.Window([900,900], color=("black"), colorSpace='rgb', allowGUI=True, monitor='testMonitor', units='deg', fullscr=False)
win.mouseVisible = False

# Open a writeable data file for our output .csv
current_time = getDateStr()
dataFile = open(current_time +'.csv', 'w') 
writer = csv.writer(dataFile)
writer.writerow(["block", "video name"])

# a class that enables us to create index elements (slices) before they contain objects
class Slicemaker(object):
    def __getitem__(self, item):
        return item
    
# text to display image name on screen (for testing)
video_name = visual.TextStim(win, text="TEST", pos=(0,-10), depth=0, color=("white"), opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=3, antialias=True, wrapWidth=None)
    
def stimulus_indexing():
    
    '''This function indexeslists for target and control clips, and randomise these lists with a block list to keep 
    them in allignment. Note we use the make_slice class in order to set index elements before they contain objects'''
    
    global block_index, target_index, control_index

    make_slice = Slicemaker()
    target_index = [make_slice[0:3], make_slice[0:3], make_slice[0:3], make_slice[0:3], make_slice[0:3],
                    make_slice[0:4], make_slice[0:4], make_slice[0:4], make_slice[0:4], make_slice[0:4]]  

    control_index = [make_slice[0:4], make_slice[0:4], make_slice[0:4], make_slice[0:4], make_slice[0:4], 
                     make_slice[0:3], make_slice[0:3], make_slice[0:3], make_slice[0:3], make_slice[0:3]]
                   
    block_index = [1,2,3,4,5,6,7,8,9,10]
                   
    if shuffle_blocks == "yes":
        temp = list(zip(target_index, control_index, block_index))
        random.shuffle(temp)
        target_index, control_index, block_index = map(list, zip(*temp))
    else:
        pass

def get_files(directory1, directory2, directory3, directory4):
    
    '''This function accepts four directories (target (1) prog & (2) ad + control (3) prog & (4) ad),
    sorts them and assigns them to their respective lists. It then randomises both target lists in 
    alignment, followed by randomising the control lists in alignment'''
    
    global all_prog_targets, all_ad_targets, all_prog_controls, all_ad_controls
    
    all_prog_targets = sorted(os.listdir(directory1))
    all_ad_targets   = sorted(os.listdir(directory2))
    all_prog_controls = sorted(os.listdir(directory3))
    all_ad_controls   = sorted(os.listdir(directory4))

    # randomly shuffle target stimuli lists in allignment
    temp = list(zip(all_prog_targets, all_ad_targets))
    random.shuffle(temp)
    all_prog_targets, all_ad_targets = map(list, zip(*temp))
    
    # randomly shuffle control simuli lists in alignment
    temp = list(zip(all_prog_controls, all_ad_controls))
    random.shuffle(temp)
    all_prog_controls, all_ad_controls = map(list, zip(*temp))
    
def get_block(index1, index2):
    
    '''This function accepts both slice indexes (target/control) and uses them to insert the appropriate
    amount of videos into target/control + prog/ad lists. It also creates stimulus name lists with respect
    to each sub-list ready to assign to each video later'''
    
    global target_prog_subset, target_ad_subset, control_prog_subset, control_ad_subset
    global target_prog_names, target_ad_names, control_prog_names, control_ad_names
    
    target_prog_subset = []
    target_ad_subset   = []
    
    target_prog_subset   = all_prog_targets[index1]
    target_ad_subset     = all_ad_targets[index1]
    
    control_prog_subset  = all_prog_controls[index2]
    control_ad_subset    = all_ad_controls[index2]

    # set stim names
    target_prog_names   = []
    target_ad_names     = []
    
    control_prog_names  = []
    control_ad_names    = []
    
    # create stimulus name lists
    for file in target_prog_subset:
        target_prog_names.append("Target Group/prog/" + file)
    for file in target_ad_subset:
        target_ad_names.append("Target Group/ad/" + file)
    for file in control_prog_subset:
        control_prog_names.append("Control Group/prog/" + file)
    for file in control_ad_subset:
        control_ad_names.append("Control Group/ad/" + file)
        
def make_stims():
    
    '''This function creates our video stim objects and assigns to respective video lists. 
    It then assigned each video a name (directory and filename)'''
    
    global control_prog_stims, control_advert_stims, target_prog_stims, target_advert_stims
    
    # create video stimuli and assign to respective lists
    target_prog_stims   = [visual.MovieStim3(win, target_prog_dir + "/" + stim) for stim in target_prog_subset[:]]
    target_advert_stims = [visual.MovieStim3(win, target_ad_dir + "/" + stim) for stim in target_ad_subset[:]]
    
    control_prog_stims   = [visual.MovieStim3(win, control_prog_dir + "/" + stim) for stim in control_prog_subset[:]]
    control_advert_stims = [visual.MovieStim3(win, control_ad_dir + "/" + stim) for stim in control_ad_subset[:]]

    # assign each video stim a name
    for counter, stim in enumerate(target_prog_stims):
        stim.name = target_prog_names[counter]
    for counter, stim in enumerate(target_advert_stims):
        stim.name = target_ad_names[counter]
    for counter, stim in enumerate(control_prog_stims):
        stim.name = control_prog_names[counter]
    for counter, stim in enumerate(control_advert_stims):
        stim.name = control_ad_names[counter]

    # returns 4 video stim lists
    return target_prog_stims, target_advert_stims, control_prog_stims, control_advert_stims
    
''' refactor this function '''
def display_order(block):
    
    '''This function appends our video display_list with the appropriate videos with respect
    to each block. Each block has a different set of video lags corresponding to the order 
    in which the videos are displayed'''
    
    global display_list
    
    print(str(block))
    display_list = []
    
    if block == 1:
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        display_list.append(control_advert_stims[3])
        
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[0])
        
        display_list.append(target_prog_stims[0])
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[2])
        display_list.append(control_prog_stims[3])
        
    elif block == 2:
        display_list.append(control_advert_stims[0])
        
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        display_list.append(control_advert_stims[3])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[2])
        
        display_list.append(target_prog_stims[0])
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        
        display_list.append(control_prog_stims[3])
        
    elif block == 3:
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        display_list.append(control_advert_stims[3])
        
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[2])
        
        display_list.append(target_prog_stims[2])
        display_list.append(target_prog_stims[1])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[2])
        display_list.append(control_prog_stims[3])
        
        display_list.append(target_prog_stims[0])
        
    elif block == 4:
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[2])
        display_list.append(control_advert_stims[3])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        
        display_list.append(target_prog_stims[0])
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        
        display_list.append(control_prog_stims[2])
        display_list.append(control_prog_stims[3])
        
    elif block == 5:
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        display_list.append(control_advert_stims[3])
        
        display_list.append(target_advert_stims[0])
        
        display_list.append(target_prog_stims[0])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[2])
        display_list.append(control_prog_stims[3])
        
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        
    elif block == 6:
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        
        display_list.append(target_advert_stims[3])
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[2])
        
        display_list.append(control_prog_stims[0])
        
        display_list.append(target_prog_stims[0])
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        display_list.append(target_prog_stims[3])
        
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[2])
        
    elif block == 7:
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        
        display_list.append(target_advert_stims[3])
        display_list.append(target_advert_stims[2])
        
        display_list.append(target_prog_stims[2])
        display_list.append(target_prog_stims[3])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[2])
        
        display_list.append(target_prog_stims[0])
        display_list.append(target_prog_stims[1])
        
    elif block == 8:
        display_list.append(control_advert_stims[0])
        
        display_list.append(target_advert_stims[3])
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        
        display_list.append(target_prog_stims[0])
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        display_list.append(target_prog_stims[3])
        
        display_list.append(control_prog_stims[2])
        
    elif block == 9:
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        
        display_list.append(target_advert_stims[3])
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        display_list.append(target_prog_stims[3])
        
        display_list.append(control_prog_stims[0])
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[2])
        
        display_list.append(target_prog_stims[0])
        
    elif block == 10:
        display_list.append(target_advert_stims[3])
        display_list.append(target_advert_stims[2])
        display_list.append(target_advert_stims[1])
        display_list.append(target_advert_stims[0])
        
        display_list.append(control_advert_stims[0])
        display_list.append(control_advert_stims[1])
        display_list.append(control_advert_stims[2])
        
        display_list.append(control_prog_stims[2])
        display_list.append(control_prog_stims[1])
        display_list.append(control_prog_stims[0])
        
        display_list.append(target_prog_stims[0])
        display_list.append(target_prog_stims[1])
        display_list.append(target_prog_stims[2])
        display_list.append(target_prog_stims[3])
        
    # print stimuli name (for testing purposes)
    for stim in display_list:
        print("display stim name: ", stim.name)
        
def video_display():
    
    '''This function displays each video in the current block (display_list); the first
    and second half of the block (advert/programme) is split with a 2 second gap. It also saves
    a data file on each iteration containing the block number and video name. If "image_labels"
    is set to "yes" then the image name is displayed under the video (for testing purposes).
    The "escape" button quits the display and closes, saving the datafile upon exit'''
    
    inter_block_counter=1
    inter_block_pause=2
    for video in display_list:
        
        video_name.text=video.name
        
        if inter_block_counter==8:
            win.flip()
            core.wait(inter_block_pause)
            
        dataFile.write('%s, %s\n'%(block_index[0], video.name))
        shouldflip = video.play()
        while video.status != visual.FINISHED:
            shouldflip = video.draw()
            
            if image_labels=="yes":
                video_name.draw()
                
            check_exit_keypress()
            win.flip()
        
        print(inter_block_counter)
        inter_block_counter+=1
       
    win.flip()
    core.wait(.1)
        
def remove():
    
    '''This function removes the "already seen" videos from their respective lists using
    the appropriate slice indexes, or "pop" for single item removal'''
    
    del all_prog_targets[target_index[0]]
    del all_ad_targets[target_index[0]]
    del all_prog_controls[control_index[0]]
    del all_ad_controls[control_index[0]]
    
    target_index.pop(0)
    control_index.pop(0)
    block_index.pop(0)
    
def check_exit_keypress():
    
    '''This function stops the experiment with 'escape' key and saves a dataFile
    upon exit'''
    
    keys = event.getKeys('escape')
    if keys and keys[0] == 'escape':
        dataFile.close()
        win.close()
        core.quit()
        
# GET INITIAL FILE LIST AND PERFORM STIMULUS INDEXING (RUN ONCE ONLY)
get_files(target_prog_dir, target_ad_dir, control_prog_dir, control_ad_dir)
stimulus_indexing()

#========================================================#
#===================== MAIN ROUTINE =====================#
#========================================================#

for i in range(blocks): # number of blocks
    
    # perform stimulus indexing using appropriate 
    # number of control and target videos
    get_block(target_index[0], control_index[0])
    
    # make video stimuli objects 
    make_stims()
    
    # assign videos to correct lag position based 
    # on block number
    display_order(block_index[0])
    
    # display the current block video list
    video_display()

    # remove previously displayd videos from sub-lists
    remove()

# save datafile, close and exit
dataFile.close()
win.close()
core.quit()




