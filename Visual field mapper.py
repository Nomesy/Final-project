# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 19:43:46 2022

@author: Morsr
"""
# This experiment is called the 'Visual Field Mapper.'
# By Kyle S.

## What does it do? What does the paricipant do? and whats the stimulus?
# Normally the dots would cover the entire screen but for the sake of convenience and time I adjusted it so they only appear on the side the blind spot should be for each eye. This allows for less dots to be needed.
# 1.  The participant covers one of their eyes and with the other stares at the fixation cross without looking away or moving their head. 
# 2. A series of blinking dots will appear in random positions on the window. 
# 3. When they see a dot they hit the space bar. Each dot is present for only 0.5 seconds but the participants response can be recorded for a total of 1 second after the stimulus appears so there is a 0.5 second buffer.
# 4. After all of the dots are presented for an eye it will present all of the dots simultaneously creating a map of dots. Red means you missed that dot and green means you detected it.
# 5. After viewing the map this process is repeated for the other eye.

## Why?
# This experiment can be used to map the visual field for blind spots and detect where the blind spot might be in each eye. This can be useful for deminstrating the blind spot to those that are not aware of it already or for collelcting data about it, such size or location. 
# if the dots were allowed to extend to the entire screen (which can be done with a simple edit) it could be useful in checking for new blind spots that could of been created through a stroke, brain injury or surgery.

## File output/ response collection
# A file that outputs three important outputs for every trial/stimuli in the experiment: the eye used, coordinates of the stimuli, whether it was detected or not.
# coordniates are saved as (x,y), and eyes are either 'left' or 'right'.
# detection of each trial is the actual dependant variable of this experiment. If the particpant sees the stimulus of that trial it is recorded as a 1. However if they did not see the stimulus it is record as a 0. 
# This file is named "Visual field Coordinates for subject('subject_nr')-('date').csv." The example file provided was called "Visual field Coordinates for subject1-7-15-12-2022"

#=====================
#IMPORT MODULES
#=====================

#this imports the necessay modules for the experiments.
from psychopy import gui, core, visual, monitors, event
from datetime import datetime
import os
import numpy as np
import random
import pandas as pd
import csv

#=====================
#PATH SETTINGS
#=====================

#this defines the paths/directories and creates a folder for storing the collected data files if it does not exist already.
main_dir = os.getcwd()
sub_dir = os.path.join(main_dir,'sub_info')
if not os.path.exists(sub_dir):
    os.makedirs(sub_dir)
print(sub_dir)

#=====================
#COLLECT PARTICIPANT INFO
#=====================

# This collects info from the participant. trial number is useful because the larger it is the more effective the map will be but the longer the experiment will take. because this experiment relies on field of view its important that the resolution is correct.
exp_info = { 'subject_nr':0,
            'age':0,
            'gender': ('male','female','other'),
            'trials per eye (recommend >100)': 100,
            'monitor width resolution': 1920,
            'monitor height resolution': 1080}

#this will be used in the while loop so that the participant will be prompted with the gui until they give a valid subject number or quit
subjectCollect = 0
while subjectCollect == 0:
    my_dlg = gui.DlgFromDict(dictionary=exp_info, title="subject info",order=['subject_nr','age', 'gender','trials per eye (recommend >100)','monitor width resolution','monitor height resolution'])
    
    #make sure subject can consent to taking part in the experiment        
    if exp_info['age'] < 18:
        err_dlg = gui.Dlg(title='error message')
        err_dlg.addText('%d year olds cannot give consent!' % (exp_info['age']))
        err_dlg.show()
        core.quit() 
    
    #If the subject number is invalid it will prompt a error message saying such and that they need ot enter a vlid one
    if exp_info['subject_nr'] ==0: 
        err_dlg = gui.Dlg(title='error message') 
        err_dlg.addText('Enter a valid subject number!') 
        err_dlg.show() 
    # because the subject number doesnt have a core.quit() the while loop will allow for the gui to be reprompted to collect a proper one.
    
    #if the subject number is valid it will change the Subject collect to 1 and effectivly end the loop.
    elif exp_info['subject_nr'] != 0:
        subjectCollect = 1



#this will get the date and time
date=datetime.now()
print(date)
exp_info['date'] = (str(date.hour) + '-' +
                    str(date.day) + '-' +
                    str(date.month) + '-' +
                    str(date.year))
print(exp_info['date'])


#-create a unique filename for the collected data 
filename = 'Visual field Coordinates for subject' + str(exp_info['subject_nr']) + '-' + str(exp_info['date']) + '.csv'



#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
# this code defines the blocks and trials. trials is defined as the input from the gui so its customizable.
nTrials = exp_info['trials per eye (recommend >100)']
nBlocks = 2
totalTrials = nTrials*nBlocks

#this creates empty lists that will be used later to generate the stim position
R_width = [0]*nTrials
R_height = [0]*nTrials
L_width = [0]*nTrials
L_height = [0]*nTrials

#this assigns random variables that fall on the right or left of the screen into the empty lists created above. to generate the value that will be used as position Coordinates for the stim. there are two of them so that half od the variables are on the right side of the screen and the other half is on the left.
for i in range(nTrials):
    
    R_width[i] = random.randint(0,round((exp_info['monitor width resolution']*2)/5)) 
    R_height[i] = random.randint(round(-exp_info['monitor height resolution']/3), round(exp_info['monitor height resolution']/3))

for i in range(nTrials):
    L_width[i] = random.randint(round((-exp_info['monitor width resolution']*2)/5), 0) 
    L_height[i] = random.randint(round(-exp_info['monitor height resolution']/3), round(exp_info['monitor height resolution']/3))
    
#=====================
#PREPARE CONDITION LISTS
#=====================
#this creates zipped lists of the right and left coordinates, then randomizes them. then they are combined. this order allows for the lists to be randomized and makes it so that the first haft of the list is for the right eye and the latter half for the left.
R_stimLoc = list(zip(R_width,R_height))
L_stimLoc = list(zip(L_width,L_height))
np.random.shuffle(R_stimLoc)
np.random.shuffle(L_stimLoc)
stimLoc = R_stimLoc + L_stimLoc

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
#this creates empty lists of the info we want to collect. eye, position and detection being important outputs for the identifcation of blind spots, where they are and for which eye.
positions = [0]*totalTrials
detections = [0]*totalTrials
trialNumb = [0]*totalTrials
blockNumb = [0]*totalTrials
eyes = [0]*totalTrials


#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
#this defines the monitor. it also defines and creates the window to 
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([exp_info['monitor width resolution'],exp_info['monitor height resolution']])
win = visual.Window(monitor=mon, units='pix', size=(exp_info['monitor width resolution'],exp_info['monitor height resolution']), color=[-1,-1,-1])

stimCircle = visual.Circle(win, size=(7,7)) 
fixation = visual.TextStim(win, text='+', height = 40, color='white')
#=====================
#START EXPERIMENT
#=====================
# This creates the introduction and block instructions for the experiment. 
instructions_text = visual.TextStim(win, height = 30, text='For each block you will close one eye and with the other one you will keep your gaze focused on the fixation cross for the entire block. if you need to blink do it quickly. While looking at the cross, hit the space key everytime a dot appears in view. If you do not see one do not click anything. Hit space to continue')
block_R_text = visual.TextStim(win, height = 30, text='Please close your left eye and focus on the fixation cross with your right eye. Then the distance between your head and monitor should be about the width of your monitor. Make sure your head is comfortable and right eye is centered on the fixation cross. Press space when your ready!')
block_L_text = visual.TextStim(win, height = 30, text='Please close your right eye and focus on the fixation cross with your left eye. Then the distance between your head and monitor should be about the width of your monitor. Make sure your head is comfortable and left eye is centered on the fixation cross. Press space when your ready!')
instructions_text.draw()
win.flip()
event.waitKeys()
#=====================
#BLOCK SEQUENCE
#=====================
for iblock in range(nBlocks):
    #this checks what block the loop is on and displays instructions to close a certain eye, the depending on the block it is on.
    if iblock == 0:
        block_R_text.pos = (0,200)
        block_R_text.draw()
        
    elif iblock == 1:
        block_L_text.pos = (0,200)
        block_L_text.draw()
        
    fixation.draw()
    win.flip()
    event.waitKeys()
    #=====================
    #TRIAL SEQUENCE
    #===================== 
    for itrial in range(nTrials):
        # creates a variable that increases for every trial and block its on. This will allow us to automatically retreive the index positions of the collection lists for each trial.
        overallTrial = iblock*nTrials+itrial
        # using overallTrial it updates and saves the trial's block number, trial number and stim position to what its supposed to be so that when the file is saved at the end the these values are properly assigned for each trial.
        blockNumb[overallTrial] = iblock+1
        trialNumb[overallTrial] = itrial+1
        positions[overallTrial] = (stimLoc[overallTrial][0], stimLoc[overallTrial][1])
        # this serves a simular function to the code above but checks for the block its on and assigns the proper eye (right or left) that was used to observe this trials stimulus.
        if iblock == 0:
            eyes[overallTrial] = 'Right'
                
        elif iblock == 1:
            eyes[overallTrial] = 'Left'
        # the following code access the position that the stimulus for the trial is supposed to be presented at. and assignes the stimulus the colour grey-ish white, and also finally drawing it.
        
        stimCircle.pos = (stimLoc[overallTrial][0],stimLoc[overallTrial][1])
        stimCircle.color = (0.5,0.5,0.5)
        stimCircle.draw() 
        fixation.draw()
        # this clears key presses before this point
        event.clearEvents()
        # this will persent the fixation cross and the stim. however the stim is only presented for 0.5 seconds, but the fixation cross will remain.
        win.flip()
        
        fixation.draw()
        core.wait(0.5)
        win.flip()
        core.wait(0.5)
        # this checks if a key was pressed during the trial and assigns a value to "detection" for that trial. 1 if a key was pressed (i.e., detected) or a 0 if no key was pressed (i.e., not detected).
        keys = event.getKeys(keyList=['space'])
        if keys:
            detections[overallTrial] = 1
        else:
            detections[overallTrial] = 0
     # this codes informs the participant that they have completed the block and informs them how the visual field map will be displayed and what keys to press to move foward with the experiment.     
    Block_end_text = visual.TextStim(win, height = 30, text='You have finished the block! Your visual field map will be displayed after this message. Green dots are ones you detected and red dots are ones you missed. To move on from this message and the visual field map press the "w" key.')
    Block_end_text.draw()
    win.flip()
    event.waitKeys(keyList=['w'])
    
    # this follow bit of code will run through all of the previous trials in the current block and will display them all at once. it colours each dot as red if it was missed and green if it was detected.
    for itrial in range(nTrials):
        overallTrial = iblock*nTrials+itrial
        stimCircle.pos = (stimLoc[overallTrial][0],stimLoc[overallTrial][1])
        if detections[overallTrial] == 1:
            stimCircle.color = 'green'
        elif detections[overallTrial] == 0:
            stimCircle.color = 'red'
        stimCircle.draw() 
    fixation.draw()
    win.flip()
    event.waitKeys(keyList=['w'])
    
    
#======================
# END OF EXPERIMENT
#====================== 
# this tells the participant the experiment is over and thanks them for participating. closes the window after they press any key.
end_text = visual.TextStim(win, height = 30, text='The experiment is complete. Thank you for participating! press any key to close the window')
end_text.draw()
win.flip()
event.waitKeys()
win.close()


# formats the data and saves it as a csv file.
df = pd.DataFrame(data={
  "Block Number": blockNumb, 
  "Trial Number": trialNumb, 
  "Eye": eyes, 
  "Position": positions, 
  "Detection": detections
})

df.to_csv(os.path.join(sub_dir, filename), sep=',', index=False)

# this processes the collected data to locate missed points and the percentage of the points that were detected. Mostly for fun but could have use in finding specific spots on the monitor/field of view that you missed.
print('Possible blind spot(s) in right eye:', (df['Position'][(df['Detection'] == 0) & (df['Eye'] == 'Right')]))
print('Possible blind spot(s) in left eye:', (df['Position'][(df['Detection'] == 0) & (df['Eye'] == 'Left')]))
print('Right eye: percentage of dots seen:', (df['Detection'][df['Eye'] == 'Right']).mean() * 100,'%')
print('Left eye: percentage of dots seen:', (df['Detection'][df['Eye'] == 'Left']).mean() * 100,'%')


