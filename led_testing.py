import mido

output_port_name = 'FaderPort'  # Replace with your actual FaderPort output port name

def Rec_led_on():

    with mido.open_output(output_port_name) as port:
        # REC LED ON
        note_number = 0  # C-1 corresponds to MIDI note number 0
        velocity_on = 127  # Velocity value that turned the LED on
        on_message = mido.Message('note_on', note=note_number, velocity=velocity_on, channel=0)  # Channels are 0-indexed in mido
        port.send(on_message)


def Mute_led_on():

    with mido.open_output(output_port_name) as port:
        # REC LED ON
        note_number = 16  # C-1 corresponds to MIDI note number 0
        velocity_on = 127  # Velocity value that turned the LED on
        on_message = mido.Message('note_on', note=note_number, velocity=velocity_on, channel=0)  # Channels are 0-indexed in mido
        port.send(on_message)

def Solo_led_on():

    with mido.open_output(output_port_name) as port:
        # REC LED ON
        note_number = 8  # C-1 corresponds to MIDI note number 0
        velocity_on = 127  # Velocity value that turned the LED on
        on_message = mido.Message('note_on', note=note_number, velocity=velocity_on, channel=0)  # Channels are 0-indexed in mido
        port.send(on_message)

def Loop_led_on():

    with mido.open_output(output_port_name) as port:
        # REC LED ON
        note_number = 86  # C-1 corresponds to MIDI note number 0
        velocity_on = 127  # Velocity value that turned the LED on
        on_message = mido.Message('note_on', note=note_number, velocity=velocity_on, channel=0)  # Channels are 0-indexed in mido
        port.send(on_message)


def Stop_led_off():

    with mido.open_output(output_port_name) as port:
        # REC LED ON
        note_number = 94  # C-1 corresponds to MIDI note number 0
        velocity_on = 0  # Velocity value that turned the LED on
        on_message = mido.Message('note_off', note=note_number, velocity=velocity_on, channel=0)  # Channels are 0-indexed in mido
        port.send(on_message)


Stop_led_off()