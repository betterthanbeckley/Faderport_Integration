# name=Faderport

#Modes declaration

#Imports
import transport
import associations
import general
import ui
import mixer
import device
import fp_init_protocol
import time

#Initialization, Using Mackie Protocol, see module
def OnInit():
    fp_init_protocol.OnInitial()



#Variables Block
touch_mode = False
read_mode = False



# Functions Block
def start_playback():
    print ('play button pressed')
    transport.start()

def stop_playback():
    print('stop button pressed')
    transport.stop()

def arm_daw_record():
    print ('DAW record button pressed')
    transport.record()

def Get_song_pos():
    current_position = transport.getSongPos()
    return current_position

def jump_forward():
    current_position = Get_song_pos()
    fwd_position = (current_position + .075)  #Change this later, just getting it working now
    transport.setSongPos(fwd_position)

def jump_backward():
    current_position = Get_song_pos()
    bckwd_position = (current_position - .075)  #Change this later, just getting it working now
    transport.setSongPos(bckwd_position)

def show_mixer():
    visible = ui.getVisible(0)
    if visible == 0:
        ui.showWindow(0)
    elif visible == 1:
        ui.hideWindow(0)

def show_playlist():
    visible = ui.getVisible(2)
    if visible == 0:
        ui.showWindow(2)
    elif visible == 1:
        ui.hideWindow(2)

def show_channel_rack():
    visible = ui.getVisible(1)
    if visible == 0:
        ui.showWindow(1)
    elif visible == 1:
        ui.hideWindow(1) 

def select_r_mixer_track():  
    selected_track = mixer.trackNumber()
    next_track = selected_track + 1

    max_track = 125
    min_track = 1
    if next_track > max_track:
            mixer.setTrackNumber(min_track)
            ui.scrollWindow(0, min_track, 1)
    else:
        mixer.setTrackNumber(next_track)
        ui.scrollWindow(0, next_track, 1)

    update_fader_position()

def select_l_mixer_track():
    selected_track = mixer.trackNumber()
    next_track = selected_track - 1

    max_track = 124
    min_track = 0
    if next_track < min_track:
            mixer.setTrackNumber(max_track)
            ui.scrollWindow(0, max_track, 1)
    elif next_track > max_track:
        mixer.setTrackNumber(min_track)
        ui.scrollWindow(0, min_track, 1)
    else:
        mixer.setTrackNumber(next_track)
        ui.scrollWindow(0, next_track, 1)
    
    update_fader_position()

def track_mute():
    selected_track = mixer.trackNumber()
    tmute = mixer.isTrackMuted(selected_track)
    mixer.muteTrack(selected_track)

def track_solo():
    selected_track = mixer.trackNumber()
    tmute = mixer.isTrackSolo(selected_track)
    mixer.soloTrack(selected_track)

def track_arm_record():
    selected_track = mixer.trackNumber()
    tmute = mixer.isTrackArmed(selected_track)
    mixer.armTrack(selected_track)

def pan_right(track_index):
    pan_value = mixer.getTrackPan(track_index)
    new_value = float(pan_value) + 0.1
    mixer.setTrackPan(track_index,new_value)

def pan_left(track_index):
    pan_value = mixer.getTrackPan(track_index)
    new_value = float(pan_value) - 0.1
    mixer.setTrackPan(track_index,new_value)

def faderport_control_volume(track_index, pitch_value):

    selected_track = mixer.trackNumber()
    normalized_value = (pitch_value+8192) / (8192 + 8176)
    mixer.setTrackVolume(selected_track, normalized_value)

def Fl_control_faderport(pitch_value):

    pitch_value = max(-8192, min(pitch_value, 8176))

    data1 = (pitch_value + 8192) & 0x7f
    data2 = ((pitch_value + 8192) >> 7) & 0x7F

    status_byte = 0xE0
    channel = 0
    midiId = (status_byte + channel)

    device.midiOutMsg(midiId, channel, data1, data2)

def update_fader_position():
    selected_track = mixer.trackNumber()
    track_volume = mixer.getTrackVolume(selected_track)

    pitch_value = int((track_volume * (8176 + 8192)) - 8192)

    Fl_control_faderport(pitch_value)
 

    global last_wobble_time
    current_time = time.time()
    Wobble_amount = 10
    Wobble_messages = 5
    
    if current_time - last_wobble_time > min_interval_between_wobbles:
        for i in range(Wobble_messages):
            # Alternate the direction of the wobble
            wobble_direction = 1 if i % 2 == 0 else -1
            wobble_pitch_value = base_pitch_value + (wobble_direction * Wobble_amount)
            Fl_control_faderport(wobble_pitch_value)
            time.sleep(0.02)  # Small delay between messages to make the wobble noticeable but quick
        
        last_wobble_time = current_time

def monitor_and_update_faderport(track_index):
    print("monitoring new mixer position")
    selected_track = mixer.trackNumber()
    track_volume = mixer.getTrackVolume(selected_track)
    pitch_value = int((track_volume * (8176 + 8192)) - 8192)
    pitch_value = max(-8192, min(pitch_value, 8176))

    data1 = (pitch_value + 8192) & 0x7f
    data2 = ((pitch_value + 8192) >> 7) & 0x7F

    status_byte = 0xE0
    channel = 0
    midiId = (status_byte + channel)

    # Sending the MIDI message to update the FaderPort's fader position
    device.midiOutMsg(status_byte, channel, data1, data2)

def toggle_touch_mode():
    global touch_mode
    if touch_mode:
        touch_mode = False
    else:
        touch_mode = True
def toggle_read_mode():
    global read_mode
    if read_mode:
        read_mode = False
    else:
        read_mode = True
        track_index = mixer.trackNumber()
        monitor_and_update_faderport(track_index)

def OnDirtyMixerTrack(track_index):
    if read_mode:
        monitor_and_update_faderport(track_index)
    elif read_mode == False:
        pass






def handle_midi_control(event_data):
    print ("recieved control number: {control number}")
    midi_control_actions = {
        associations.play_button: start_playback,
        associations.stop_button: stop_playback,
        associations.arm_record_button: arm_daw_record,
        associations.fwd_button: jump_forward,
        associations.rewind_button: jump_backward,
        associations.mix_button: show_mixer,
        associations.proj_button: show_playlist,
        associations.transport_button: show_channel_rack,
        associations.bank_channel_select_right_button: select_r_mixer_track,
        associations.bank_channel_select_left_button: select_l_mixer_track,
        associations.track_mute_button: track_mute,
        associations.track_solo_button: track_solo,
        associations.track_arm_record_button: track_arm_record,
        associations.fader_mode_touch_button: toggle_touch_mode,
        associations.fader_mode_read_button: toggle_read_mode
    }
    action = midi_control_actions.get(event_data)
    if action:
        action()
        return True
    return False

def OnMidiMsg(event):
    #print(f"status: {event.status}, Data1: {event.data1}, Data2: {event.data2}")
    status_byte = event.status & 0xF0
    midi_channel = event.status & 0x0F

    if status_byte == 0xE0 or (status_byte >= 0xE0 and status_byte <= 0xEF):
        # Extract the pitch value, consider the MIDI channel if necessary
        pitch_value = (event.data2 << 7) + event.data1 - 8192  # Adjust based on how your device sends pitch bend
        track_index = mixer.trackNumber()  # Implement this function based on your needs
        faderport_control_volume(track_index, pitch_value)
        event.handled = True


    if status_byte == 0x90 or (status_byte >= 0x90 and status_byte <= 0x9F):
        if event.data1 == associations.fader_touch:
            if touch_mode == False:
                print(f"ignoring note {event.data1}")
                event.handled = True
                return
        if event.data2 > 0:
            handled = handle_midi_control(event.data1)
            if handled:
                event.handled = True
                return
    
    if status_byte == 0xB0 or (status_byte >= 0xB0 and status_byte <=0xBF):
        track_index = mixer.trackNumber()
        if event.data2 == 1:
            pan_right(track_index)
        if event.data2 == 65:
            pan_left(track_index)

        


    #event.handled = event.data2 > 0 and handle_midi_control(event.data1)