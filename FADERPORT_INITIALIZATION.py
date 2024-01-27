#FADERPORT_INITIALIZATION


#THIS PROGRAM IS INTENDED TO INITIALIZE THE PRESONUS FADERPORT CLASSIC UTILIZING THE SAME PROTOCOL WITHIN UNIVERSAL AUDIO'S LUNA

import mido
import time
import FADERPORT_INIT_SYSEX_DATA

#Port name specification
port_name = 'FaderPort'



#******** Sends initial values inluding a series of note off commands, CC messages, Aftertouch Messages, and Pitch Wheel Messages
def Send_int_values():

    with mido.open_output(port_name) as port:
        first_note = 0
        first_msg=mido.Message('note_off', note=first_note, velocity=0, channel=0)
        port.send(first_msg)
        print(f"Sent: {first_msg}")
        time.sleep(0.004)

        #Sending Note Off messages to the FaderPort
        notes = [
            1, 10, 100, 11, 113, 114, 
            12, 13, 14, 15, 16, 17, 
            18, 19, 2, 8, 9, 10, 
            11, 24, 25, 26, 27, 28, 
            29, 3, 30, 31, 28, 40,  
            41, 42, 43, 44, 45, 46, 
            47, 48, 49, 5, 50, 54, 
            55, 6, 7, 70, 71, 72, 
            73, 74, 75, 76, 77, 78, 
            79, 8, 81, 82, 83, 86, 
            89, 9, 90, 91, 92, 93, 
            94, 95, 96, 97, 98, 99
    ]

        cmessages = [
            (48, 0),
            (49, 0),
            (50, 0),
            (51, 0),
            (52, 0),
            (53, 0),
            (54, 0),
            (55, 0),
            (64, 32),
            (65, 32),
            (66, 32),
            (67, 32),
            (68, 32),
            (69, 32),
            (70, 32),
            (71, 32),
            (72, 32),
            (73, 32),
        ]

        aftertouch = [
            0, 15, 16, 31, 32, 47, 
            48, 63, 64, 79, 80, 95,
            96, 111, 112, 127
        ]

        pitch_values = [
            0, 1, 2, 3, 4, 5, 
            6, 7, 8
        ]

        combined_messages = []

        # Add note-off messages to the combined list
        for n in notes:
            msg = mido.Message('note_off', note=n, velocity=0, channel=0)
            combined_messages.append(msg)

        # Add control change messages to the combined list
        for ctrl, val in cmessages:
            msg = mido.Message('control_change', control=ctrl, value=val, channel=0)
            combined_messages.append(msg)

        #Add channel pressure messages to the combined list
        for afval in aftertouch:
            msg = mido.Message('aftertouch', value=afval, channel=0)
            combined_messages.append(msg)

        for chanval in pitch_values:
            msg = mido.Message('pitchwheel', pitch=-8192, channel=chanval)
            combined_messages.append(msg)


        with mido.open_output(port_name) as port:
            for msg in combined_messages:
                port.send(msg)
        time.sleep(0.012)

#******** Sends Initial sysex message, obtained from using a midi monitor and watching UA's LUNA (DAW) startup protocols        
def Send_sysex1():
    from FADERPORT_INIT_SYSEX_DATA import sysex_message1
    with mido.open_output(port_name) as port:
        msg = mido.Message('sysex', data=sysex_message1)
        port.send(msg)

#******** Sends more initial values, specifically a note on, then some pitch wheel (fader) info
def Send_int_values2():
    combined_msgs = []

    pw_vals = [
        (3952, 8),
        (3952, 0),
        (3952, 1),
        (3776, 0)
    ]

    msg = mido.Message('note_on', note=93, velocity=127, channel=0)
    combined_msgs.append(msg)

    for val, chnl in pw_vals:
        pwmsg = mido.Message('pitchwheel', pitch=val, channel=chnl)
        combined_msgs.append(pwmsg)

    with mido.open_output(port_name) as port:
        for msg in combined_msgs:
            port.send(msg)

#Sends Final sysex message, followed by one more note-on command
def Send_sysex2():
    combined_msg = []
    from FADERPORT_INIT_SYSEX_DATA import sysex_message2
    
    msg = mido.Message('sysex', data=sysex_message2)
    combined_msg.append(msg)
    
    msg = mido.Message('note_on', note=24, velocity=127, channel=0)
    combined_msg.append(msg)

    with mido.open_output(port_name) as port:
        for msg in combined_msg:
            port.send(msg)

#Runs program in proper order, timing values are within above functions.
def Faderport_init():
    Send_int_values()
    Send_sysex1()
    Send_int_values2()
    Send_sysex2()



Faderport_init()

