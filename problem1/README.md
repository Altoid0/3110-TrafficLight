# Traffic Light Controller System
The system will control traffic flow at an intersection, manage the transition between Red, Yellow, 
and Green states, and include priority handling for emergency vehicles. When an emergency vehicle is 
detected, the system should override the normal operation, immediately giving the green light to the
direction where the emergency vehicle is approaching.

## Requirements
* [Python] 3.11 and above

## Instructions to Run it
1. Download the project file `3110-TrafficLight-main`
1. Open the Terminal of your operating System
1. Locate and navigate to the directory where files are located
    - e.g. `cd downloads/3110-TrafficLight-main`
1. Run the project using `python TrafficLight.py`

## Running the Project
1. After executing users will be asked to create strings by combining: `t e c s` 
```bash
Enter a string of inputs using ['t', 'e', 'c' and 's'] (or type 'exit' to quit): tts
  Transition error: 's'. This input string leads to an undefined state.
  The DFA does not accept the string 'tts'.
```
2. The program will check the user's input until `exit` is entered
```bash
Enter a string of inputs using ['t', 'e', 'c' and 's'] (or type 'exit' to quit): exit
  Exiting the program.
```