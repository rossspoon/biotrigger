# Code added from PsychoPy by Mihai Toma, 8 / 9 / 2023

############## code eyeLink setup section before experiment


########## Start section from the Before Experiment part of 
########## the eyelinkConnect code in the eyelinkSetup routine

import pylink
import time
import os
import platform
from PIL import Image  # for preparing the Host backdrop image
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from string import ascii_letters, digits
from psychopy import visual, core, event, monitors, gui
import sys

# Switch to the script folder
script_path = os.path.dirname(sys.argv[0])
if len(script_path) != 0:
    os.chdir(script_path)


# Set this variable to True if you use the built-in retina screen as your
# primary display device on macOS. If have an external monitor, set this
# variable True if you choose to "Optimize for Built-in Retina Display"
# in the Displays preference settings.
use_retina = False

# Set this variable to True to run the script in "Dummy Mode"
dummy_mode = True

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
dlg_title = 'Enter EDF File Name'
dlg_prompt = 'Please enter a file name with 8 or fewer characters\n' + \
             '[letters, numbers, and underscore].'


# Set up EDF data file name and local data folder
#
# The EDF data filename should not exceed 8 alphanumeric characters
# use ONLY number 0-9, letters, & _ (underscore) in the filename
edf_fname = 'TEST'

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
dlg_title = 'Enter EDF File Name'
dlg_prompt = 'Please enter a file name with 8 or fewer characters\n' + \
             '[letters, numbers, and underscore].'

# loop until we get a valid filename
while True:
    dlg = gui.Dlg(dlg_title)
    dlg.addText(dlg_prompt)
    dlg.addField('File Name:', edf_fname)
    # show dialog and wait for OK or Cancel
    ok_data = dlg.show()
    if dlg.OK:  # if ok_data is not None
        print('EDF data filename: {}'.format(ok_data[0]))
    else:
        print('user cancelled')
        core.quit()
        sys.exit()

    # get the string entered by the experimenter
    tmp_str = dlg.data[0]
    # strip trailing characters, ignore the ".edf" extension
    edf_fname = tmp_str.rstrip().split('.')[0]

    # check if the filename is valid (length <= 8 & no special char)
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        print('ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        print('ERROR: EDF filename should not exceed 8 characters')
    else:
        break
        
# Set up a folder to store the EDF data files and the associated resources
# e.g., files defining the interest areas used in each trial
results_folder = 'results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# We download EDF data file from the EyeLink Host PC to the local hard
# drive at the end of each testing session, here we rename the EDF to
# include session start date/time
time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_fname + time_str

# create a folder for the current testing session in the "results" folder
session_folder = os.path.join(results_folder, session_identifier)
if not os.path.exists(session_folder):
    os.makedirs(session_folder)
    
    
# Step 1: Connect to the EyeLink Host PC
#
# The Host IP address, by default, is "100.1.1.1".
# the "el_tracker" objected created here can be accessed through the Pylink
# Set the Host PC address to "None" (without quotes) to run the script
# in "Dummy Mode"
if dummy_mode:
    el_tracker = pylink.EyeLink(None)
else:
    try:
        el_tracker = pylink.EyeLink("100.1.1.1")
    except RuntimeError as error:
        print('ERROR:', error)
        core.quit()
        sys.exit()

# Step 2: Open an EDF data file on the Host PC
edf_file = edf_fname + ".EDF"
try:
    el_tracker.openDataFile(edf_file)
except RuntimeError as err:
    print('ERROR:', err)
    # close the link if we have one open
    if el_tracker.isConnected():
        el_tracker.close()
    core.quit()
    sys.exit()

# Add a header text to the EDF file to identify the current experiment name
# This is OPTIONAL. If your text starts with "RECORDED BY " it will be
# available in DataViewer's Inspector window by clicking
# the EDF session node in the top panel and looking for the "Recorded By:"
# field in the bottom panel of the Inspector.
preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

# Step 3: Configure the tracker
#
# Put the tracker in offline mode before we change tracking parameters
el_tracker.setOfflineMode()

# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
# 5-EyeLink 1000 Plus, 6-Portable DUO
eyelink_ver = 0  # set version to 0, in case running in Dummy mode
if not dummy_mode:
    vstr = el_tracker.getTrackerVersionString()
    eyelink_ver = int(vstr.split()[-1].split('.')[0])
    # print out some version info in the shell
    print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

# File and Link data control
# what eye events to save in the EDF file, include everything by default
file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
# what eye events to make available over the link, include everything by default
link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
# what sample data to save in the EDF data file and to make available
# over the link, include the 'HTARGET' flag to save head target sticker
# data for supported eye trackers
if eyelink_ver > 3:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
else:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
    #el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
#el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
#el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
#el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

# Optional tracking parameters
# Sample rate, 250, 500, 1000, or 2000, check your tracker specification
# if eyelink_ver > 2:
#     el_tracker.sendCommand("sample_rate 1000")
# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical),
el_tracker.sendCommand("calibration_type = HV9")
# Set a gamepad button to accept calibration/drift check target
# You need a supported gamepad/button box that is connected to the Host PC
el_tracker.sendCommand("button_function 5 'accept_target_fixation'")

    
########## End section from the Before Experiment part of 
########## the eyelinkConnect code in the eyelinkSetup routine


########## Start section from the Begin Experiment part of 
########## the eyelinkConnect code in the eyelinkSetup routine

# get the native screen resolution used by PsychoPy
scn_width, scn_height = win.size
# resolution fix for Mac retina displays
if 'Darwin' in platform.system():
    if use_retina:
        scn_width = int(scn_width/2.0)
        scn_height = int(scn_height/2.0)

# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# see the EyeLink Installation Guide, "Customizing Screen Settings"
el_coords = "screen_pixel_coords = 0 0 %d %d" % (scn_width - 1, scn_height - 1)
el_tracker.sendCommand(el_coords)

# Write a DISPLAY_COORDS message to the EDF file
# Data Viewer needs this piece of info for proper visualization, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (scn_width - 1, scn_height - 1)
el_tracker.sendMessage(dv_coords)  
    
########## End section from the Begin Experiment part of 
########## the eyelinkConnect code in the eyelinkSetup routine


########## Start section from the End Routine part of 
########## the eyelinkConnect code in the eyelinkSetup routine

# Configure a graphics environment (genv) for tracker calibration
genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win)
print(genv)  # print out the version number of the CoreGraphics library

# Set background and foreground colors for the calibration target
# in PsychoPy, (-1, -1, -1)=black, (1, 1, 1)=white, (0, 0, 0)=mid-gray
foreground_color = (-1, -1, -1)
background_color = win.color
genv.setCalibrationColors(foreground_color, background_color)

# Set up the calibration target
#
# The target could be a "circle" (default), a "picture", a "movie" clip,
# or a rotating "spiral". To configure the type of calibration target, set
# genv.setTargetType to "circle", "picture", "movie", or "spiral", e.g.,
# genv.setTargetType('picture')
#
# Use gen.setPictureTarget() to set a "picture" target
# genv.setPictureTarget(os.path.join('images', 'fixTarget.bmp'))
#
# Use genv.setMovieTarget() to set a "movie" target
# genv.setMovieTarget(os.path.join('videos', 'calibVid.mov'))

# Use a picture as the calibration target
genv.setTargetType('picture')
genv.setPictureTarget(os.path.join('sns', 'fixTarget.bmp'))

# Configure the size of the calibration target (in pixels)
# this option applies only to "circle" and "spiral" targets
# genv.setTargetSize(24)

# Beeps to play during calibration, validation and drift correction
# parameters: target, good, error
#     target -- sound to play when target moves
#     good -- sound to play on successful operation
#     error -- sound to play on failure or interruption
# Each parameter could be ''--default sound, 'off'--no sound, or a wav file
genv.setCalibrationSounds('', '', '')

# resolution fix for macOS retina display issues
if use_retina:
    genv.fixMacRetinaDisplay()

# Request Pylink to use the PsychoPy window we opened above for calibration
pylink.openGraphicsEx(genv)



def clear_screen(win):
    """ clear up the PsychoPy window"""

    win.fillColor = genv.getBackgroundColor()
    win.flip()


def show_msg(win, text, wait_for_keypress=True):
    """ Show task instructions on screen"""

    msg = visual.TextStim(win, text,
                          color=genv.getForegroundColor(),
                          wrapWidth=scn_width/2)
    clear_screen(win)
    msg.draw()
    win.flip()

    # wait indefinitely, terminates upon any key press
    if wait_for_keypress:
        event.waitKeys()
        clear_screen(win)


def terminate_task():
    """ Terminate the task gracefully and retrieve the EDF data file

    file_to_retrieve: The EDF on the Host that we would like to download
    win: the current window used by the experimental script
    """

    el_tracker = pylink.getEYELINK()

    if el_tracker.isConnected():
        # Terminate the current trial first if the task terminated prematurely
        error = el_tracker.isRecording()
        if error == pylink.TRIAL_OK:
            abort_trial()

        # Put tracker in Offline mode
        el_tracker.setOfflineMode()

        # Clear the Host PC screen and wait for 500 ms
        el_tracker.sendCommand('clear_screen 0')
        pylink.msecDelay(500)

        # Close the edf data file on the Host
        el_tracker.closeDataFile()

        # Show a file transfer message on the screen
        msg = 'EDF data is transferring from EyeLink Host PC...'
        show_msg(win, msg, wait_for_keypress=False)

        # Download the EDF data file from the Host PC to a local data folder
        # parameters: source_file_on_the_host, destination_file_on_local_drive
        local_edf = os.path.join(session_folder, session_identifier + '.EDF')
        try:
            el_tracker.receiveDataFile(edf_file, local_edf)
        except RuntimeError as error:
            print('ERROR:', error)

        # Close the link to the tracker.
        el_tracker.close()

    # close the PsychoPy window
    win.close()

    # quit PsychoPy
    core.quit()
    sys.exit()


def abort_trial():
    """Ends recording """

    el_tracker = pylink.getEYELINK()

    # Stop recording
    if el_tracker.isRecording():
        # add 100 ms to catch final trial events
        pylink.pumpDelay(100)
        el_tracker.stopRecording()

    # clear the screen
    clear_screen(win)
    # Send a message to clear the Data Viewer screen
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # send a message to mark trial end
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)

    return pylink.TRIAL_ERROR    
    

# skip this step if running the script in Dummy Mode
if not dummy_mode:
    try:
        el_tracker.doTrackerSetup()
    except RuntimeError as err:
        print('ERROR:', err)
        el_tracker.exitCalibration()

print("FINISHED CAL")



#clear the screen before we begin Camera Setup mode
clear_screen(win)


########## End section from the End Routine part of 
########## the eyelinkConnect code in the eyelinkSetup routine



########################### code for each trial


################################################################### begin Routine
########## Start section from the Begin Routine part of 
########## the eyelinkTrialCode code in the trial routine

########## IMPORTANT NOTE:
########## TIMING IN TRIAL COMPONENTS MUST BE
########## HANDLED VIA FRAME UNITS RATHER
########## THAN TIME UNITS
########## OTHERWISE, TIMING WILL NOT BE CORRECT

win.mouseVisible = True


# get a reference to the currently active EyeLink connection
el_tracker = pylink.getEYELINK()

# put the tracker in the offline mode first
el_tracker.setOfflineMode()

# clear the host screen before we draw the backdrop
el_tracker.sendCommand('clear_screen 0')

    # show a backdrop image on the Host screen, imageBackdrop() the recommended
    # function, if you do not need to scale the image on the Host
    # parameters: image_file, crop_x, crop_y, crop_width, crop_height,
    #             x, y on the Host, drawing options
##    el_tracker.imageBackdrop(os.path.join('images', pic),
##                             0, 0, scn_width, scn_height, 0, 0,
##                             pylink.BX_MAXCONTRAST)

# If you need to scale the backdrop image on the Host, use the old Pylink
# bitmapBackdrop(), which requires an additional step of converting the
# image pixels into a recognizable format by the Host PC.
# pixels = [line1, ...lineH], line = [pix1,...pixW], pix=(R,G,B)
#
# the bitmapBackdrop() command takes time to return, not recommended
# for tasks where the ITI matters, e.g., in an event-related fMRI task
# parameters: width, height, pixel, crop_x, crop_y,
#             crop_width, crop_height, x, y on the Host, drawing options
#
# Use the code commented below to convert the image and send the backdrop
#im = Image.open(script_path + "/" + trialImage)  # read image with PIL
#im = im.resize((scn_width, scn_height))
#img_pixels = im.load()  # access the pixel data of the image
#pixels = [[img_pixels[i, j] for i in range(scn_width)]
#          for j in range(scn_height)]
#el_tracker.bitmapBackdrop(scn_width, scn_height, pixels,\
#    0, 0, scn_width, scn_height,0, 0, pylink.BX_MAXCONTRAST)

# OPTIONAL: draw landmarks and texts on the Host screen
# In addition to backdrop image, You may draw simples on the Host PC to use
# as landmarks. For illustration purpose, here we draw some texts and a box
# For a list of supported draw commands, see the "COMMANDS.INI" file on the
# Host PC (under /elcl/exe)
left = int(scn_width/2.0) #- 60
top = int(scn_height/2.0) #- 60
right = int(scn_width/2.0) #+ 60
bottom = int(scn_height/2.0) #+ 60
draw_cmd = 'draw_filled_box %d %d %d %d 1' % (left, top, right, bottom)
el_tracker.sendCommand(draw_cmd)

# send a "TRIALID" message to mark the start of a trial, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
el_tracker.sendMessage('TRIALID %d' % trial_index)

# record_status_message : show some info on the Host PC
# here we show how many trial has been tested
status_msg = 'TRIAL number %d' % trial_index
el_tracker.sendCommand("record_status_message '%s'" % status_msg)

# drift check
# we recommend drift-check at the beginning of each trial
# the doDriftCorrect() function requires target position in integers
# the last two arguments:
# draw_target (1-default, 0-draw the target then call doDriftCorrect)
# allow_setup (1-press ESCAPE to recalibrate, 0-not allowed)
#
# Skip drift-check if running the script in Dummy Mode
#while not dummy_mode:
    # terminate the task if no longer connected to the tracker or
    # user pressed Ctrl-C to terminate the task
#    if (not el_tracker.isConnected()) or el_tracker.breakPressed():
#        terminate_task()
    # drift-check and re-do camera setup if ESCAPE is pressed
#    try:
#        error = el_tracker.doDriftCorrect(int(scn_width/2.0),
#                                          int(scn_height/2.0), 1, 1)
        # break following a success drift-check
#        if error is not pylink.ESC_KEY:
#            break
#    except:
#        pass

# put tracker in idle/offline mode before recording
el_tracker.setOfflineMode()

# Start recording
# arguments: sample_to_file, events_to_file, sample_over_link,
# event_over_link (1-yes, 0-no)
try:
    el_tracker.startRecording(1, 1, 1, 1)
except RuntimeError as error:
    print("ERROR:", error)
    abort_trial()

# Allocate some time for the tracker to cache some samples
pylink.pumpDelay(100)

########## End section from the Begin Routine part of 
########## the eyelinkTrialCode code in the trial routine

################################################################### each Frame
# abort the current trial if the tracker is no longer recording
win.mouseVisible = True

error = el_tracker.isRecording()
if error is not pylink.TRIAL_OK:
    el_tracker.sendMessage('tracker_disconnected')
    abort_trial()


# check keyboard events
for keycode, modifier in event.getKeys(modifiers=True):

# Abort a trial if "ESCAPE" is pressed
    if keycode == 'escape':
        el_tracker.sendMessage('trial_skipped_by_user')
        # clear the screen
        clear_screen(win)
        # abort trial
        abort_trial()
        

    # Terminate the task if Ctrl-c
    if keycode == 'c' and (modifier['ctrl'] is True):
        el_tracker.sendMessage('terminated_by_user')
        terminate_task()
        

###################################################################### end Routine
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
offsetValue = int(round((core.getTime() - fixation.tStartRefresh)*1000))
el_tracker.sendMessage('%i FIXATION_ONSET' % offsetValue)

# send some Data Viewer drawing commands so that you can see a representation
# of the fixation cross in Data Viewer's various visualizations
# For more information on this, see section "Protocol for EyeLink Data to 
# Viewer Integration" section of the Data Viewer User Manual (Help -> Contents)
el_tracker.sendMessage('%i !V CLEAR 128 128 128' % offsetValue)
el_tracker.sendMessage('%i !V DRAWLINE 255 255 255 %i %i %i %i' % \
    (offsetValue,scn_width/2 - 50,scn_height/2,scn_width/2 + 50,\
    scn_height/2))
el_tracker.sendMessage('%i !V DRAWLINE 255 255 255 %i %i %i %i' % \
    (offsetValue,scn_width/2,scn_height/2 - 50,scn_width/2,\
    scn_height/2 + 50))

# calculate the difference between the current time and the time of the 
# image onset. This offset value will be sent at the beginning of the message
# and will automatically be subtracted by Data Viewer from the timestamp
# of the message to position the message at the correct point in time
# then send a message marking the event
offsetValue = int(round((core.getTime() - imageBigNeg2.tStartRefresh)*1000)) # here we need the stimulus start
el_tracker.sendMessage('%i IMAGE_ONSET' % offsetValue)

# send some Data Viewer drawing commands so that you can see the trial image
# in Data Viewer's various visualizations
# For more information on this, see section "Protocol for EyeLink Data to 
# Viewer Integration" section of the Data Viewer User Manual (Help -> Contents)
el_tracker.sendMessage('%i !V CLEAR 128 128 128' % offsetValue)
el_tracker.sendMessage('%i !V IMGLOAD CENTER ../../%s %i %i' % \
    (offsetValue,animal,scn_width/2,scn_height/2)) 

# if a key was presssed, calculate the difference between the current time 
# and the time of the key press onset. 
# This offset value will be sent at the beginning of the message
# and will automatically be subtracted by Data Viewer from the timestamp
# of the message to position the message at the correct point in time
# then send a message marking the event
ratingChoiceNeg = sliderChoiceNegative2.getRating()

if not isinstance(sliderChoiceNegative2.rt,list):
    offsetValue = int(round((core.getTime() - \
        (imageBigNeg2.tStartRefresh + sliderChoiceNegative2.rt))*1000))
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