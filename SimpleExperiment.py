#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Simplistic psychophysical experiment sample 
# The protocole used here is 'Method of constant stimuli'
# Copyright Matthieu Perreira Da Silva, October 2017

# Import the PsychoPy libraries that you want to use
from psychopy import core, visual, gui, monitors, event, data
import numpy as np

# Give informations about our monitor
mon = monitors.Monitor(name='myMonitor')
mon.setWidth(50)        # Here we use a monitor with a width of 50cm and height of 30cm
mon.setGamma(2.2)       # By default use standard gamma value of 2.2
mon.setDistance(3*30)    # By default place observer a 3X the height of the screen
mon.setSizePix((1920,1080)) # Resolution of the screen used
maxScreenLuminance=150;     # In cd/m2  => you should get this value when performing display calibration

# Ask for partiticpant name
dlg = gui.Dlg()
dlg.addField("Subject Name:")
dlg.show()
infos = {'observerName': dlg.data[0]}

# parameters linked to the protocol
infos['stimuliRepetition']=10;   # we will randomly show each stimuli 'stimuliRepetition' times (should be > 20)

# parameters of the stimuli
infos['stimuliType']='gabor'                        # can also be 'sin'
infos['stimulusSize']=5                             #in visual angle degrees
infos['stimulusContrastStep']=0.05
infos['stimulusConstrastRange']=np.arange(0.0,0.25+infos['stimulusContrastStep'],infos['stimulusContrastStep'])   # value between 0 (no constrast) to 1 (full contrast)
infos['stimulusFreqRange']=[0.25,1,5,10,20]         # in cycles per degree
infos['stimulusOrientation']=90                     # in degrees
infos['stimulusPhase']=0                            # also in degrees

# parameters of the background
infos['backgroundMeanLuminance']=75;     # in cd/m2
backgroundValue=-1+2*infos['backgroundMeanLuminance']/maxScreenLuminance # because background value lies in [-1,1] interval

# precompute the list of stimuli that will be shown to the user
conditions = []
for c in infos['stimulusConstrastRange']:
    for f in infos['stimulusFreqRange']:
        conditions.append({'contrast': c, 'freq': f})
handler=data.TrialHandler(conditions, infos['stimuliRepetition'], extraInfo=infos)

# Create a Psychopy window
win = visual.Window([1920,1080], fullscr=True, units='deg', monitor=mon, color=[backgroundValue, backgroundValue, backgroundValue])

# Display instructions on screen
text = visual.TextStim( win=win, 
    text='Instructions :\n\nYou will be shown different stimuli\n\nPress Y if you see something, N if not.\n\n Strike a key when ready to start !',
    color=[-1, -1, -1])
text.draw()
win.flip()
event.waitKeys()

# Loop on all the constrast values that we want to display
for trial in handler:
    # warn user that we will display a new stimuli soon
    text = visual.TextStim( win=win, 
        text='Trial '+ str(handler.thisN) + ' / ' + str(handler.nTotal),
        color=[-1, -1, -1])
    text.draw()
    win.flip()
    core.wait(0.5)
    
    # generate a sin or a gabor patch
    grating = visual.GratingStim( win=win, units="deg", size=[infos['stimulusSize'], infos['stimulusSize']], blendmode = 'add' )
    grating.sf = trial['freq']
    grating.phase = infos['stimulusPhase']
    grating.ori = infos['stimulusOrientation']
    grating.contrast = trial['contrast']
    
    # if we need to generate a gabor patch
    if infos['stimuliType'] == 'gabor':
        grating.mask = 'gauss'
    
    # Display the grating
    grating.draw()
    win.flip()
    core.wait(.5)
    
    text = visual.TextStim( win=win, 
        text='Have you seen something ? (y/n)',
        color=[-1, -1, -1])
    text.draw()
    win.flip()
    
    # Wait for the answer
    key=event.waitKeys(keyList=["y", "n", "q"])
    if key[0] == 'y': 
        answer = 1 
    elif key[0] == 'n':
        answer = 0
    else:
        break
    
    handler.addData('answer',answer)

# Save the answersMatrix
handler.saveAsPickle(infos['observerName']+'-results')

# End of the experiment
# Close window
win.close()
# Close PsychoPy
core.quit()

