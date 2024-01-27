import mido
import time
import os

#Variables Block
output_port_name = "FaderPort"
input_port_name = "FaderPort"


#Functions Block
"""
# Previous script for recieving all MIDI Messages and printing them out

def display_midi_message(message):
    print (f"Recieved MIDI Message: {message}")

def recieve_midi_message():
    try:
        with mido.open_input(input_port_name, callback=display_midi_message) as port:
            print ("Monitoring MIDI messages on port: {input_port_name}")
            input("press Enter to stop monitoring...")
    
    except mido.MidiError as e:
        print (f"Error: {e}")

if __name__ == "__main__":
    recieve_midi_message()
"""


# Script for prompting user to input variable names and associating with midi note input
current_variable_name = ""


    #Function prompts user to input the variable name
def get_variable_name():
    global current_variable_name
    current_variable_name = input ("Enter a variable name:" )
    return current_variable_name


    #get_midi_note_value function prompts user to input a midi message on the device
def get_midi_note_value():

    with mido.open_input(input_port_name) as port:
        print(f"Press the -- {current_variable_name} -- on -- {input_port_name} --")
        for msg in port:
            if msg.type == 'note_on' and msg.velocity > 0:
                return msg.note

    #function creates a dictionary to store variable-note associations
variable_note_dict = {}

def update_variable_note_dict(current_variable_name,note_value):
    variable_note_dict[current_variable_name] = note_value
    association_string = f"{current_variable_name} = {note_value}\n"

        #File Writing section
    with open("associations.txt", "a") as file:
        file.write(association_string)

    print(f"Association created: -- {current_variable_name} -- with MIDI Note --{note_value}")

    #Function to handle variable association
def associate_variable_with_midi():
    variable_name = get_variable_name()
    note_value = get_midi_note_value()
    update_variable_note_dict(current_variable_name, note_value)

    #Function to clear the terminal
def clear_terminal_vscode():
    os.system('cls' if os.name == 'nt' else 'clear')


    #Loop for user input, program testing
while True:
    associate_variable_with_midi()
    user_input = input("Do you want to associate another variable?: (Y/N)")
    clear_terminal_vscode()
    if user_input.lower() != "y":
        break
