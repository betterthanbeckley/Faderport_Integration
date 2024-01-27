import mido
import time


def send_pitch_wheel_message(output_port, pitch_value):
    # Ensure the pitch value is within the valid range for MIDI pitchwheel messages, not Mido library standard of 0..16383
    pitch_value = max(-8192, min(pitch_value, 8191))

    # Create and send the pitch wheel message directly
    pitch_message = mido.Message('pitchwheel', channel=0, pitch=pitch_value)
    output_port.send(pitch_message)


# Replace 'FaderPort_Input' with the name of your FaderPort MIDI input port
input_port_name = 'FaderPort'

# Replace 'FaderPort_Output' with the name of your FaderPort MIDI output port
output_port_name = 'FaderPort'

def on_pitch_wheel(message):
    if message.type == 'pitchwheel':
        print(f'Pitch Wheel Value: {message.pitch}')

def monitor_pitch_wheel(input_port_name):
    with mido.open_input(input_port_name) as input_port:
        print(f"Monitoring pitch wheel on {input_port_name}. Press Ctrl+C to exit.")
        
        try:
            for message in input_port:
                on_pitch_wheel(message)
        except KeyboardInterrupt:
            print("Monitoring stopped.")


with mido.open_output(output_port_name) as output_port:
        print("Controlling the motorized fader on the FaderPort...")
        for pitch_value in range(-8192, 8191, 50):
            send_pitch_wheel_message(output_port, pitch_value)
            time.sleep(0.015)

        for pitch_value in range(8192, -8191, -50): 
            send_pitch_wheel_message(output_port, pitch_value)
            time.sleep(0.015)


#monitor_pitch_wheel(input_port_name)




