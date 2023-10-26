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