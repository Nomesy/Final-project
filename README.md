# Final-project
This experiment is called the ['Visual Field Mapper.'](https://github.com/Nomesy/Final-project/blob/main/Visual%20field%20mapper.py)

By Kyle S.


## What does it do? What does the paricipant do? and whats the stimulus?
Normally the dots would cover the entire screen but for the sake of convenience and time I adjusted it so they only appear on the side the blind spot should be for each eye. This allows for less dots to be needed.
1. The participant covers one of their eyes and with the other stares at the fixation cross without looking away or moving their head. 
2. A series of blinking dots will appear in random positions on the window. 
3. When they see a dot they hit the space bar. Each dot is present for only 0.5 seconds but the participants response can be recorded for a total of 1 second after the stimulus appears so there is a 0.5 second buffer.
4. After all of the dots are presented for an eye it will present all of the dots simultaneously creating a map of dots. Red means you missed that dot and green means you detected it.
5. After viewing the map this process is repeated for the other eye.

## Why?
This experiment can be used to map the visual field for blind spots and detect where the blind spot might be in each eye. This can be useful for deminstrating the blind spot to those that are not aware of it already or for collelcting data about it, such size or location. 
Additionally, if the dots were allowed to extend to the entire screen (which can be done with a simple edit) it could be useful in checking for new blind spots that could of been created through a stroke, brain injury or surgery.

## File output/ response collection
A file that outputs three important outputs for every trial/stimuli in the experiment: the eye used, coordinates of the stimuli, whether it was detected or not.
coordniates are saved as (x,y), and eyes are either 'left' or 'right'.
detection of each trial is the actual dependant variable of this experiment. If the particpant sees the stimulus of that trial it is recorded as a 1. However if they did not see the stimulus it is record as a 0. 
This file is named "Visual field Coordinates for subject('subject_nr')-('date').csv." The example file provided was called ["Visual field Coordinates for subject1-7-15-12-2022."](https://github.com/Nomesy/Final-project/blob/main/Visual%20field%20Coordinates%20for%20subject1-7-15-12-2022.csv)

At the end of the code it runs some simple data analysis code that tells you the coordinates that were missed and the percentage of dots detected. This is more of a fun and interesting output than anything really that useful.
