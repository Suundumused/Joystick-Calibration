# Joystick-drifting-fix
**A project to correct, via software, game controller analog sticks that pull to the sides.**
 - The software captures analog inputs from the faulty physical controller and applies user-defined filter correction and then creates a virtual joystick with modified analog inputs to be used in the game.

![Alt text](https://raw.githubusercontent.com/Suundumused/Joystick-drifting-fix/main/README_ASSETS/5.png)
---
### Development usage
    pip install -r requirements.txt

   run from `main.py`

### Requirements
   min `Windows 8.1 64 bits`

### Usage
 - If the game supports choosing the default joystick, check all the options for using analog and button replication, it will copy all the buttons on the physical joystick to a new virtual joystick "fake XBOX 360 CONTROLLER". Otherwise, select only the analogue option, the program will overwrite only that input to avoid duplicate inputs in games that do not support multiple joysticks.
 
 - Set the joystick ID to 1 "In the future I will add a list of options to choose from."
 - Within the game, the virtual joystick will appear as "XBOX 360 CONTROLLER" set as default.
 - To activate the self-calibration option, press any joystick button

### Support
**BTC**: `bc1qa0xzyhcmcsuvppttmylzygwwfaken5jturhgek`
**ETH**: `0x2fA70716D1Ae2f4994Be8e249b609056D72Ce80a`
