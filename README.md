# Faderport_Integration
The purpose of this program is to integrate my Presonus Faderport Classic into FL Studio's API. The project has been much more daunting than I expected it to be, as, I started it as a complete novice to python or really any programming whatsoever. With a lot of trial, error, and chatGPT, I have been able to write scripts that initialize the Faderport in MCU mode (a process that isn't covered in Presonus's documentation, and where it is, does not work). At the end of this process, I hope to make the Faderport as useful in FL studio as it is in any other DAW where it is natively supported. If not more so.

                                            *** Technologies***

    1. Presonus Faderport Classic on firmware version 1.0
    2. Visual Studio Code
    3. Fl Studio (most recent update)

*** Versions

Current Version (01/26/2024) - V 0.y.z
    Using Semantic Versioning, API is not yet stable.
    Functionalities - 
        1. Start // Stop transport buttons are functional
        2. Arm Daw Record transport button is functional
            - LED does not yet light up when the button is pressed / when daw is recording
        3. Jump FWD // Jump Back transport buttons are functional
            - Jumps are an arbitrary Value, would like to make it jump a certain number of bars
        4. MIX // PROJ // TRNS buttons are functional and show mixer, project, and sample rack windows respectivelly
            - Windows aren't focused when they come up, need to add focusing
            - probably other bugs with this at the moment
        5. BANK R // L buttons are functional select mixer tracks to the right or left of selected mixer track
            - Buttons are only functional when the bank button is selected and glowing red, otherwise they output ascending/descending midi notes. I'm sure I can integrate this feature into the script and utilize the bank select for something else
        6. FADER is functional at sending and recieving information corresponding to the selected mixer track
            - Known issue with the aftertouch button sending a note on message that will play the selected channel in the channel rack.
    External Modules - 
        1. associations.py
            - this is a list of the buttons and their associated midi note numbers, useful for being able to type out variable names rather than tracking down the note number each time I want to create a new mapping
        2. fp_init_protocol
            - This is it's own program that is utlized on FL initialization. I had some serious difficulties getting the Faderport in the proper mode (MCU, I think, or HUI) to send/recieve midi messages in a way that is conducive to being used as a midi controller. After extensive searching, I downloaded LUNA (Univeral Audio's DAW) and used a virtual midi monitor to spy on the output from LUNA to the Faderport when it is initialized. I took this string of note off, CC, Pitch Wheel, and sysex messages and translated them to FL's API and then fiddled with the timing until I was able to boot up the Faderport in the proper protocol. This is the most important section of the code as without it the rest of my script is useless.

