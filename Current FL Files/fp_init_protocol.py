#name=peesonus


#THIS PROGRAM IS INTENDED TO INITIALIZE THE PRESONUS FADERPORT CLASSIC UTILIZING THE SAME PROTOCOL WITHIN UNIVERSAL AUDIO'S LUNA   
def OnInitial():

    import device
    import time
    import fp_init_sysex

    Note_off = 0x80
    Note_on = 0x90
    Aftertouch_all = 0xA0
    Control_change = 0xB0
    Aftertouch_one = 0xD0
    Pitch_bend = 0xE0

    print("Initializing Faderport Protocol")
    time.sleep(1)

    #******** Sends initial values inluding a series of note off commands, CC messages, Aftertouch Messages, and Pitch Wheel Messages
    def Send_int_values():
        Note_off = 0x80
        Note_on = 0x90
        Aftertouch_all = 0xA0
        Control_change = 0xB0
        Aftertouch_one = 0xD0
        Pitch_bend = 0xE0

        
        first_note = 0
        first_msg = (Note_off, 0, first_note, 0,)
        device.midiOutMsg(*first_msg)
        time.sleep(0.004)

        #Sending Note Off messages to the FaderPort
        notes = [
            1, 10, 100, 11, 113, 114, 
            12, 13, 14, 15, 16, 17, 
            18, 19, 2, 20, 21, 22, 
            23, 24, 25, 26, 27, 28, 
            29, 3, 30, 31, 4, 40,  
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
            msg = (Note_off, 0, n, 0,)
            combined_messages.append(msg)
        print ("    Sent Int Notes")

        # Add control change messages to the combined list
        for ctrl, val in cmessages:
            msg = (Control_change, 0, ctrl, val)
            combined_messages.append(msg)
        print ("        Sent Int CC")

        #Add channel pressure messages to the combined list
        for afval in aftertouch:
            msg = (Aftertouch_one, 0, afval)
            combined_messages.append(msg)
        print ("            Sent Int Aftertouch")

        for chanval in pitch_values:
            msg = (Pitch_bend, chanval, 0)
            combined_messages.append(msg)
        print ("                sent Int Pitch Messages")



        for msg in combined_messages:
            device.midiOutMsg(*msg)
        print ("Protocol Notes Block One Delivered to Device")
        time.sleep(0.112)

    #******** Sends Initial sysex message, obtained from using a midi monitor and watching UA's LUNA (DAW) startup protocols        
    def Send_sysex1():
        from fp_init_sysex import sysex_message1
        device.midiOutSysex(bytes(sysex_message1))
        print("Sent Init System Exclusive Message 1")


    #******** Sends more initial values, specifically a note on, then some pitch wheel (fader) info
    def Send_int_values2():
        combined_msgs = []

        pw_vals = [
            (3952, 8),
            (3952, 0),
            (3952, 1),
            (3776, 0)
        ]

        for val, chnl in pw_vals:
            val = val +8192
            val = max(0, min(val, 16383))
            val_lsb = val % 128
            val_msb = val // 128

            pwmsg = (Pitch_bend, chnl, val_lsb, val_msb)
            combined_msgs.append(pwmsg)
        print ("        Sent Init PW Values")
        


        msg = (Note_on, 0, 93, 127)
        combined_msgs.append(msg)
        print ("            Sent Int Note On Msgs")

        for msg in combined_msgs:
            device.midiOutMsg(*msg)

    #Sends Final sysex message, followed by one more note-on command
    def Send_sysex2():
        combined_msg = []
        from fp_init_sysex import sysex_message2
        device.midiOutSysex(bytes(sysex_message2))
        print("Sent Init System Exclusive Message 2")
        
        msg = (Note_on, 0, 24, 127)
        combined_msg.append(msg)

        for msg in combined_msg:
            device.midiOutMsg(*msg)
        print("                 Final Note-On Message Delivered")
        time.sleep(1)
        print("Faderport Protocol Loaded")

    #Runs program in proper order, timing values are within above functions.
    Send_int_values()
    Send_sysex1()
    Send_int_values2()
    Send_sysex2()
