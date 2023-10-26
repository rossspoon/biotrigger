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

