########## Start section from the End Routine part of
########## the eyelinkTrialCode code in the trial routine

# clear the screen
clear_screen(win)
el_tracker.sendMessage('blank_screen')
# send a message to clear the Data Viewer screen as well
el_tracker.sendMessage('!V CLEAR 128 128 128')

# calculate the difference between the current time and the time of the
# fixation onset. This offset value will be sent at the beginning of the message
# and will automatically be subtracted by Data Viewer from the timestamp
# of the message to position the message at the correct point in time
# then send a message marking the event
offsetValue = int(round((core.getTime() - fixation.tStartRefresh) * 1000))
el_tracker.sendMessage('%i FIXATION_ONSET' % offsetValue)

# send some Data Viewer drawing commands so that you can see a representation
# of the fixation cross in Data Viewer's various visualizations
# For more information on this, see section "Protocol for EyeLink Data to
# Viewer Integration" section of the Data Viewer User Manual (Help -> Contents)
el_tracker.sendMessage('%i !V CLEAR 128 128 128' % offsetValue)
el_tracker.sendMessage('%i !V DRAWLINE 255 255 255 %i %i %i %i' % \
                       (offsetValue, scn_width / 2 - 50, scn_height / 2, scn_width / 2 + 50, \
                        scn_height / 2))
el_tracker.sendMessage('%i !V DRAWLINE 255 255 255 %i %i %i %i' % \
                       (offsetValue, scn_width / 2, scn_height / 2 - 50, scn_width / 2, \
                        scn_height / 2 + 50))

# calculate the difference between the current time and the time of the
# image onset. This offset value will be sent at the beginning of the message
# and will automatically be subtracted by Data Viewer from the timestamp
# of the message to position the message at the correct point in time
# then send a message marking the event
offsetValue = int(round((core.getTime() - imageBigNeg2.tStartRefresh) * 1000))  # here we need the stimulus start
el_tracker.sendMessage('%i IMAGE_ONSET' % offsetValue)

# send some Data Viewer drawing commands so that you can see the trial image
# in Data Viewer's various visualizations
# For more information on this, see section "Protocol for EyeLink Data to
# Viewer Integration" section of the Data Viewer User Manual (Help -> Contents)
el_tracker.sendMessage('%i !V CLEAR 128 128 128' % offsetValue)
el_tracker.sendMessage('%i !V IMGLOAD CENTER ../../%s %i %i' % \
                       (offsetValue, animal, scn_width / 2, scn_height / 2))

# if a key was presssed, calculate the difference between the current time
# and the time of the key press onset.
# This offset value will be sent at the beginning of the message
# and will automatically be subtracted by Data Viewer from the timestamp
# of the message to position the message at the correct point in time
# then send a message marking the event
ratingChoiceNeg = sliderChoiceNegative2.getRating()

if not isinstance(sliderChoiceNegative2.rt, list):
    offsetValue = int(round((core.getTime() - \
                             (imageBigNeg2.tStartRefresh + sliderChoiceNegative2.rt)) * 1000))
    el_tracker.sendMessage('%i SLIDER_CLICKED' % offsetValue)

# stop recording; add 100 msec to catch final events before stopping
pylink.pumpDelay(100)
el_tracker.stopRecording()

# record trial variables to the EDF data file, for details, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
#el_tracker.sendMessage('!V TRIAL_VAR image %s' % animal)
el_tracker.sendMessage('!V TRIAL_VAR image %s' % imageBigNeg2)
#el_tracker.sendMessage('!V TRIAL_VAR image %s' % sectionBimage1)
#el_tracker.sendMessage('!V TRIAL_VAR image %s' % sectionBimage1)
pylink.pumpDelay(1)
#el_tracker.sendMessage('!V TRIAL_VAR accuracy %i' % mouseNext.corr)
#el_tracker.sendMessage('!V TRIAL_VAR keyPressed %s' % mouseNext.keys)
#print(str(mouseNext.rt))
#if isinstance(mouseNext.rt,list):
#    el_tracker.sendMessage('!V TRIAL_VAR RT -1')
#else:
#    el_tracker.sendMessage('!V TRIAL_VAR RT %i' % int(round(mouseNext.rt * 1000)))

# send a 'TRIAL_RESULT' message to mark the end of trial, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
el_tracker.sendMessage('TRIAL_RESULT %d' % 0)

# update the trial counter for the next trial
trial_index = trial_index + 1

########## End section from the End Routine part of
########## the eyelinkTrialCode code in the trial routine