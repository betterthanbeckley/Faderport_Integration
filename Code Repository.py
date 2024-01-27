# at 55

try:
    with mido.open_output(output_port_name) as output_port:
        print("Controlling the motorized fader on the FaderPort...")

        # Move the fader up
        for pitch_value in range(-8192, 8192, 100):
            send_pitch_wheel_message(output_port, pitch_value)
                    # Monitor fader value while moving up
            print(pitch_value)
            time.sleep(0.1)


except IOError:
    print(f"MIDI output port '{output_port_name}' not found.")

# @ 21
    def monitor_fader_value(input_port_name):
    try:
        with mido.open_input(input_port_name) as input_port:
            print(f"Monitoring MIDI input from {input_port_name}. Press Ctrl+C to exit.")
            for message in input_port:
                if message.type == 'pitchwheel' and message.channel == 0:
                    
                    # Extract only the necessary bytes for pitch wheel (typically two bytes)
                    lsb, msb = message.bytes()[:2]
                    
                    #Combine the LSB and MSB to get the 14-bit midi pitch wheel value
                    pitch_wheel_value = (msb <<7) +lsb
                    
                   # Print the raw 14-bit MIDI pitch wheel value
                    print(f"Raw 14-bit MIDI Pitch Wheel Value: {pitch_wheel_value}")
                    
    except IOError:
        print(f"MIDI input port '{input_port_name}' not found.")



with mido.open_output(output_port_name) as output_port:
        print("Controlling the motorized fader on the FaderPort...")
        for pitch_value in range(8191):
            send_pitch_wheel_message(output_port, pitch_value)
            time.sleep(0.1)



def OnMidiMsg(event):
    event.handled = False
    if event.data2 >0:
        print('Any Key Pressed')
    if event.data1 == play_button:
        print ('play key pressed')
        